from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import init_async_redis
from src.conf.constant import ACCESS_TOKEN_TTL, REFRESH_TOKEN_TTL
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas.users import RequestEmail, TokenModel, UserModel, UserResponse
from src.services.auth import auth_service
from src.services.email import send_email
from src.conf.messages import messages

router = APIRouter(tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: UserModel, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    The signup function creates a new user in the database.
        It takes a UserModel object as input, which contains the username and email of the new user.
        The function then checks if an account with that email already exists, and if it does not,
        creates a new account using create_user from repository_users.py.

    :param body: UserModel: Validate the request body
    :param background_tasks: BackgroundTasks: Add a task to the background queue
    :param request: Request: Get the base_url of the server
    :param db: AsyncSession: Get the database connection
    :return: A dict with the user and a detail message
    """
    exist_user_username = await repository_users.get_user_username(body.username, db)

    if exist_user_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.get_message("USER_WITH_USERNAME_ALREADY_EXISTS"))

    exist_user_email = await repository_users.get_user_by_email(body.email, db)

    if exist_user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.get_message("ACCOUNT_ALREADY_EXISTS"))

    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    subject = "Confirm your email! "
    template = "email_template.html"
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url), subject, template)

    return {"user": new_user, "detail": messages.get_message("USER_SUCCESSFULLY_CREATED")}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> dict:
    """
    The login function is used to authenticate a user.

    :param body: OAuth2PasswordRequestForm: Validate the request body
    :param db: AsyncSession: Get the database connection
    :return: A dict with the access_token, refresh_token and token_type
    """

    user: User | None = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("INVALID_EMAIL"))

    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("EMAIL_NOT_CONFIRMED"))

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("USER_IS_ON_BAN_LIST"))

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("INVALID_PASSWORD"))

    access_token: str = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token: str = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def user_logout(
    credentials: HTTPAuthorizationCredentials = Security(security),
    current_user: User = Depends(auth_service.get_current_user),
    redis_client: Redis = Depends(init_async_redis),
    db: AsyncSession = Depends(get_db),
):
    access_token = credentials.credentials
    refresh_token = current_user.refresh_token

    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("TOKEN_NOT_PROVIDED"))

    await redis_client.set(f"access_token:{access_token}", "valid", ex=ACCESS_TOKEN_TTL)
    await redis_client.set(f"refresh_token:{refresh_token}", "valid", ex=REFRESH_TOKEN_TTL)

    await repository_users.invalidate_token(access_token, db)
    await repository_users.invalidate_token(refresh_token, db)

    return {"message": "Token revoked"}


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(get_db)
) -> dict:
    """
    The refresh_token function is used to refresh the access token.
    It takes in a refresh token and returns an access token, a new refresh
    token, and the type of bearer authorization.

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: AsyncSession: Get the database session
    :return: A dict with the access_token, refresh_token and token type
    """

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user:
        if user.refresh_token != token:
            await repository_users.update_token(user, None, db)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("INVALID_REFRESH_TOKEN"))

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    if user:
        await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)) -> dict:
    """
    The confirmed_email function takes a token and db as parameters.
    It returns a dict with the message "Email confirmed" if the email is already confirmed, or it will return
    a dict with the message "Your email is already confirmed" if it isn't.

    :param token: str: Get the email from the token
    :param db: AsyncSession: Pass the database session to the function
    :return: A message if the email is already confirmed or a new one if it has not yet been confirmed
    """

    email = auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("VERIFICATION_ERROR"))
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    The request_email function is used to send an email to the user with a link that they can click on
    to confirm their email address. The function takes in a RequestEmail object, which contains the
    email of the user who wants to confirm their account. It then checks if there is already an account
    with that email address and whether or not it has been confirmed yet. If there isn't already an account,
    or if it has been confirmed, then we return a message saying so; otherwise we send them an email with a link.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add the send_email task to the background tasks queue
    :param request: Request: Get the base_url of the application
    :param db: AsyncSession: Create a database session
    :return: A message to the user
    """

    user = await repository_users.get_user_by_email(body.email, db)

    if user and not user.confirmed:
        subject = "Confirm your email! "
        template = "email_template.html"
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url), subject, template)
        return {"message": "Check your email for confirmation."}
    else:
        return {"message": "Your email is already confirmed."}


@router.post("/forgot_password")
async def forgot_password(
    body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    The forgot_password function is used to send an email to the user with a link that will allow them
    to reset their password. The function takes in a RequestEmail object, which contains the user's email address.
    The function then checks if there is a user associated with that email address and sends an email containing
    a link for resetting their password.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the application
    :param db: AsyncSession: Pass in the database session
    :return: A message to the user
    """

    user = await repository_users.get_user_by_email(body.email, db)

    if user:
        subject = "Password Reset Request"
        template = "password_template.html"

        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url), subject, template)
        return {"message": "Password reset request sent. We've emailed you with instructions on how to reset your password."}

    return {"message": "No user found with the provided email."}


@router.get("/reset_password", response_model=UserResponse)
async def reset_password(new_password: str, token: str, db: AsyncSession = Depends(get_db)) -> dict:
    """
    The reset_password function takes in a new password and token, then returns a dict with the user's information and
    a detail message. The function first gets the email from the token using auth_service.get_email_from_token(). Then it
    gets that user from repository users using get_user by email. If there is no such user, an HTTPException is raised with
    the status code 400 (bad request) and detail "Verification error". Otherwise, we hash the new password using
    auth service get password hash(), then change that user's password to this hashed version of their new one in repository
    users'

    :param new_password: str: Get the new password from the request body
    :param token: str: Get the email from the token
    :param db: AsyncSession: Pass the database connection to the function
    :return: A dict with the user and a detail message
    """

    email = auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("VERIFICATION_ERROR"))

    confirm_password = auth_service.get_password_hash(new_password)
    user = await repository_users.change_password(user, confirm_password, db)

    return {"user": user, "detail": messages.get_message("PASSWORD_RESET_COMPLETE")}
