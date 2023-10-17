import pickle
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings, init_async_redis
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    
    def __init__(self):
        self._redis_cache = None
    
    @property
    async def redis_cache(self):

        if self._redis_cache is None:
            self._redis_cache = await init_async_redis()
        return self._redis_cache

    def verify_password(self, plain_password, hashed_password) -> bool:
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. It then uses the CryptContext instance to verify that
        the plain-text password matches the hashed password.

        :param self: Represent the instance of the class
        :param plain_password: Get the password that was entered by the user
        :param hashed_password: Store the hashed password in the database
        :return: True if the plain_password is equal to the hashed_password
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        The get_password_hash function takes a password and returns the hashed version of it.
        The hashing algorithm is defined in the config file, which is passed to CryptContext.

        :param self: Refer to the current instance of a class
        :param password: str: Pass in the password that we want to hash
        :return: A hash of the password
        """
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        The create_access_token function creates a new access token.


        :param self: Refer to the current instance of a class
        :param data: dict: Pass the data that will be encoded into the jwt
        :param expires_delta: Optional[float]: Set the expiration time of the access token
        :return: An encoded access token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        The create_refresh_token function creates a refresh token for the user.
            The function takes in two parameters: data and expires_delta.
            Data is a dictionary containing the user's id, username, email address, and password hash.
            Expires_delta is an optional parameter that sets how long the refresh token will be valid for.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data that will be encoded in the jwt
        :param expires_delta: Optional[float]: Set the time until the refresh token expires
        :return: An encoded refresh token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str) -> str:
        """
        The decode_refresh_token function is used to decode the refresh token.
            The function takes in a refresh_token as an argument and returns the email of the user if successful.
            If unsuccessful, it raises an HTTPException with status code 401 (Unauthorized) and detail 'Invalid scope for token'
            or 'Could not validate credentials'.

        :param self: Represent the instance of a class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The email address of the user
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "refresh_token":
                email: str = payload["sub"]
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ) -> Union[User, None]:
        """
        The get_current_user function is a dependency that can be used to get the current user.
        It will check if the token is valid and return an object of type User or None.

        :param self: Access the class attributes
        :param token: str: Get the token from the authorization header
        :param db: AsyncSession: Get the database session
        :return: The user object if the token is valid
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        user_banned = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is on the ban list")

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception

            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        invalid_token = await repository_users.is_validate_token(token, db)
        if invalid_token:
            raise credentials_exception

        user_r = await (await self.redis_cache).get(f"user:{email}")
        if user_r is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            
            if not user.is_active:
                raise user_banned
            
            user_r = pickle.dumps(user)
            await (await self.redis_cache).set(f"user:{email}", user_r)
            await (await self.redis_cache).expire(f"user:{email}", 900)
            
        user_clean: User = pickle.loads(user_r)
        if not user_clean.is_active:
            raise user_banned

        return user_clean

    def get_email_from_token(self, token: str) -> str:
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function first tries to decode the token using jwt.decode, which raises a JWTError if it fails to decode the token.
        If this happens, we raise an HTTPException with status code 422 (Unprocessable Entity) and detail "Invalid Token for
        Email Verification". Otherwise, we return the email address from payload["sub"].

        :param self: Represent the instance of the class
        :param token: str: Pass in the token that was sent to the user's email address
        :return: The email from the token
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid token for email verification")
        email = payload["sub"]
        return email

    def create_email_token(self, data: dict) -> str:
        """
        The create_email_token function creates a token that is used to verify the user's email address.
        The function takes in a dictionary of data, and returns an encoded string.

        :param self: Represent the instance of a class
        :param data: dict: Pass in the data that will be encoded into the token
        :return: A token that is used to verify the user's email address
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


auth_service = Auth()
