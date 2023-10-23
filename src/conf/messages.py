from pydantic_settings import BaseSettings


class Messages(BaseSettings):
    # Users
    USER_NOT_FOUND: str = "User not found"
    USER_SUCCESSFULLY_CREATED: str = "User successfully created. Check your email for confirmation"
    ACCOUNT_ALREADY_EXIST: str = "Account already exists"
    USER_NAME_ALREADY_EXIST: str = "User with this username already exists"
    USER_IN_BAN: str = "The user is on the ban list"
    USER_ALREADY_BANNED: str = "User has already been banned"
    YOU_CANT_CHANGE_YOUR_ROLE: str = "You can't change your role"
    USER_ROLE_HAS_BEEN_CHANGED: str = "The user's role has been changed"
    MY_PROFILE_SUCCESSFULLY_EDITED: str = "My profile was successfully edited"
    YOU_CANT_BAN_YOURSELF: str = "You can't ban yourself"
    USER_WITH_NAME_ALREADY_EXIST: str = "User with this name already exists!"
    # Credentials
    INVALID_EMAIL: str = "Invalid email"
    INVALID_PASSWORD: str = "Invalid password"
    RESET_PASSWORD_COMPLETE: str = "Password reset complete"

    # Email
    EMAIL_CONFIRMED: str = "Email confirmed"
    EMAIL_NOT_CONFIRMED: str = "Email not confirmed"
    EMAIL_IS_ALREADY_CONFIRMED: str = "Your email is already confirmed"
    USER_NOT_FOUND_WITH_THE_PROVIDED_EMAIL: str = "No user found with the provided email"
    PASSWORD_RESET_SENT_REQUEST: str = "Password reset request sent. We've emailed you with instructions on how to reset your password"
    
    # Token
    TOKEN_REVOKED: str = "Token revoked"
    TOKEN_NOT_PROVIDED: str = "Token not provided"
    INVALID_REFRESH_TOKEN: str = "Invalid refresh token"

    # Comments
    COMMENT_NOT_CREATED: str = "Comment not created"
    COMMENTS_NOT_FOUND: str = "Comments not found"

    # Pictures
    PICTURE_NOT_FOUND: str = "Picture not found"
    PICTURES_NOT_FOUND: str = "Pictures not found"
    PICTURES_OF_USER_NOT_FOUND: str = "Pictures of this user not found"
    COMMENT_HAS_NOT_BEEN_UPDATED : str = "Comment has been not updated"
    DESCRIPTION_HAS_NOT_BEEN_UPDATED : str = "Description has been not updated"

    # Errors
    VERIFICATION_ERROR: str = "Verification error"


    


messages = Messages()


if __name__ == "__main__":
    print(messages.ACCOUNT_ALREADY_EXIST)
