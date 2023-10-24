

select_language = "ua"

class Message:

    messages = {
        # UKRAINIAN
        "UA": {
            # USER
            "USER_IS_ON_BAN_LIST": "Користувач знаходиться в бан списку",
            "USER_SUCCESSFULLY_CREATED": "Користувач успішно створений. Перевірте свою електронну пошту для підтвердження",
            "USER_WITH_USERNAME_ALREADY_EXISTS": "Користувач із таким нікнеймом вже існує",
            "USER_WITH_THIS_NAME_ALREADY_EXISTS": "Користувач із таким іменем вже існує",
            "ACCOUNT_ALREADY_EXISTS": "Обліковий запис вже існує",
            "INVALID_PASSWORD": "Недійсний пароль",
            "VERIFICATION_ERROR": "Помилка веріфікаціі",
            "PASSWORD_RESET_SEND_REQUEST": "Запит на скидання пароля відправлено. Ми надіслали вам електронний лист з інструкціями щодо скидання пароля.",
            "USER_NOT_FOUND_PROVIDED_EMAIL": "Не знайдено жодного користувача з указаною електронною поштою",
            "PASSWORD_RESET_COMPLETE": "Скидання пароля завершено",
            "MY_PROFILE_WAS_SUCCESSFULLY_EDITED": "Мій профіль успішно відредаговано",
            "USER_NOT_FOUND": "Користувач не знайдений",
            "YOU_CANT_BAN_YOURSELF": "Ви не можете себе заборонити",
            "USER_HAS_ALREADY_BANNED": "Користувача вже забанили",
            "USER_HAS_BEEN_BANNED": "було забанено",
            "USER_HAS_BEEN_ACTIVATED": "був активован",
            "USERS_ROLE_HAS_BEEN_CHANGED": "Роль користувача змінено",
            "YOU_CANT_CHANGE_YOUR_ROLE": "Ви не можете змінити свою роль",
            "YOU_CANT_CHANGE_ROLE_OF_BANNED_NOT_CONFIRMED_USER": "Ви не можете змінити роль забаненого або непідтвердженого користувача",
            "YOU_DONT_HAVE_PERMISSION_TO_BAN_USERS": "У вас немає дозволу банити інших користувачів",
            "USER_ALREADY_ACTIVATED": "Користувача вже активовано",
            "YOU_DONT_HAVE_PERMISSION_FOR_ACTIVATE_USERS": "У вас немає дозволу активувати інших користувачів",
            "NEW_ROLE_MUST_BE_SPECIFIED_FOR_CHANGING_ROLE": "Для зміни ролі необхідно вказати нову роль.",
            "USERS_ROLE_HAS_BEEN_CHANGED_TO": "Роль користувача змінено на",
            "YOU_DONT_HAVE_PERMISSION_FOR_CHANGE_USER_ROLES": "Ви не маєте дозволу змінювати ролі користувачів.",
            "INVALID_ACTION_SPECIFIED": "Вказана недійсна дія. Підтримувані дії: бан, активація, зміна ролі.",

            # TOKEN
            "TOKEN_NOT_PROVIDED": "Токен не надано",
            "INVALID_REFRESH_TOKEN": "Недійсний рефреш токен",
            "TOKEN_REVOKED": "Токен відкликано",

            # EMAIL
            "INVALID_EMAIL": "Недійсна електронна адреса",
            "EMAIL_CONFIRMED": "Електронна адреса підтверджена",
            "EMAIL_NOT_CONFIRMED": "Електронна пошта не підтверджена",
            "EMAIL_ALREADY_CONFIRMED": "Ваша електронна адреса вже підтверджена",
            "CHECK_EMAIL_CONFIRMATION": "Перевірте свою електронну пошту для підтвердження",

            # COMMENTS
            "COMMENT_NOT_CREATED": "Коментар не створено",
            "COMMENTS_NOT_FOUND": "Коментарі не знайдено",
            "COMMENT_NOT_FOUND": "Коментар не знайдено",
            "COMMENT_CANT_BE_EMPTY": "Коментар не може бути порожнім",
            "COMMENT_HAS_NOT_BEEN_UPDATED": "Коментар не оновлено",
            
            # PICTURES
            "PICTURE_WAS_UPLOADED_TO_SERVER": "Світлина була завантажена на сервер",
            "PICTURE_NOT_FOUND": "Світлина не знайдено",
            "PICTURES_NOT_FOUND": "Жодної світлини не знайдено",
            "PICTURES_OF_USER_NOT_FOUND": "Світлини цього користувача не знайдено",
            "NAME_OF_PICTURE_CANT_BE_EMPTY": "Назва світлини не може бути пустою",
            "DESCRIPTION_OF_PICTURE_CANT_BE_EMPTY": "Опис світлини не може бути порожнім",
            "DESCRIPTION_HAS_NOT_BEEN_UPDATED": "Опис не оновлено",
            "THE_NUMBER_OF_TAGS_SHOULD_NOT_EXCEED_5": "Кількість тегів не повинна перевищувати 5",
            "THE_NUMBER_OF_TAGS_SHOULD_NOT_EXCEED_25": "Довжина тегів не повинна перевищувати 25",

            # RATING
            "RATING_MUST_BE_1_TO_5": "Рейтинг має бути від 1 до 5",
            "RATING_SUCCESSFULLY_ADDED": "Рейтинг успішно додано",
            "UNABLE_DELETE_RATING": "Не вдалося видалити оцінку",
            "YOU_CANT_RATE_YOUR_OWN_PICTURE": "Ви не можете оцінити власне зображення",
            "YOU_HAVE_ALREADY_RATED_THIS_PICTURE": "Ви вже оцінили це зображення",

            # TAGS
            "TAGNAME_NOT_FOUND": "тег не знайдено",
            "TAGNAME_ALREADY_EXIST": "тег вже існує",
        },
        # ENGLISH
        "EN": {
            # USER
            "USER_IS_ON_BAN_LIST": "The user is on the ban list",
            "USER_SUCCESSFULLY_CREATED": "User successfully created. Check your email for confirmation",
            "USER_WITH_USERNAME_ALREADY_EXISTS": "User with this username already exists",
            "USER_WITH_THIS_NAME_ALREADY_EXISTS": "User with this name already exists!",
            "ACCOUNT_ALREADY_EXISTS": "Account already exists",
            "INVALID_PASSWORD": "Invalid password",
            "VERIFICATION_ERROR": "Verification error",
            "PASSWORD_RESET_SEND_REQUEST": "Password reset request sent. We've emailed you with instructions on how to reset your password.",
            "USER_NOT_FOUND_PROVIDED_EMAIL": "No user found with the provided email",
            "PASSWORD_RESET_COMPLETE": "Password reset complete",
            "MY_PROFILE_WAS_SUCCESSFULLY_EDITED": "My profile was successfully edited",
            "USER_NOT_FOUND": "User not found",
            "YOU_CANT_BAN_YOURSELF": "You can't ban yourself",
            "USER_HAS_ALREADY_BANNED": "User has already been banned",
            "USER_HAS_BEEN_BANNED": "has been banned",
            "USER_HAS_BEEN_ACTIVATED": "has been activated",
            "USERS_ROLE_HAS_BEEN_CHANGED": "The user's role has been changed",
            "YOU_CANT_CHANGE_YOUR_ROLE": "You can't change your role",
            "YOU_CANT_CHANGE_ROLE_OF_BANNED_NOT_CONFIRMED_USER": "You can't change the role of a banned user or not confirmed",
            "YOU_DONT_HAVE_PERMISSION_TO_BAN_USERS": "You don't have permission to ban users.",
            "USER_ALREADY_ACTIVATED": "User is already activated",
            "YOU_DONT_HAVE_PERMISSION_FOR_ACTIVATE_USERS": "You don't have permission to activate users.",
            "NEW_ROLE_MUST_BE_SPECIFIED_FOR_CHANGING_ROLE": "New role must be specified for changing the role.",
            "USERS_ROLE_HAS_BEEN_CHANGED_TO": "The user's role has been changed to",
            "YOU_DONT_HAVE_PERMISSION_FOR_CHANGE_USER_ROLES": "You don't have permission to change user roles.",
            "INVALID_ACTION_SPECIFIED": "Invalid action specified. Supported actions: ban, activate, change_role.",

            # TOKEN
            "TOKEN_NOT_PROVIDED": "Token not provided",
            "INVALID_REFRESH_TOKEN": "Invalid refresh token",
            "TOKEN_REVOKED": "Token revoked",

            # EMAIL
            "INVALID_EMAIL": "Invalid email",
            "EMAIL_CONFIRMED": "Email confirmed",
            "EMAIL_NOT_CONFIRMED": "Email not confirmed",
            "EMAIL_ALREADY_CONFIRMED": "Your email is already confirmed",
            "CHECK_EMAIL_CONFIRMATION": "Check your email for confirmation",

            # COMMENTS
            "COMMENT_NOT_CREATED": "Comment not created",
            "COMMENTS_NOT_FOUND": "Comments not found",
            "COMMENT_NOT_FOUND": "Comment is not found",
            "COMMENT_CANT_BE_EMPTY": "Comment can't be empty",
            "COMMENT_HAS_NOT_BEEN_UPDATED": "Comment has been not updated",
            
            # PICTURES
            "PICTURE_WAS_UPLOADED_TO_SERVER": "The picture was uploaded to the server",
            "PICTURE_NOT_FOUND": "Picture not found",
            "PICTURES_NOT_FOUND": "Pictures not found",
            "PICTURES_OF_USER_NOT_FOUND": "Pictures of this user not found",
            "NAME_OF_PICTURE_CANT_BE_EMPTY": "Name of picture can't be empty",
            "DESCRIPTION_OF_PICTURE_CANT_BE_EMPTY": "Description of picture can't be empty",
            "DESCRIPTION_HAS_NOT_BEEN_UPDATED": "Description has been not updated",
            "THE_NUMBER_OF_TAGS_SHOULD_NOT_EXCEED_5": "The number of tags should not exceed 5",
            "THE_LENGTH_OF_TAGS_SHOULD_NOT_EXCEED_25": "The length of tags should not exceed 25",

            # RATING
            "RATING_MUST_BE_1_TO_5": "Rating must be between 1 and 5",
            "RATING_SUCCESSFULLY_ADDED": "Rating successfully added",
            "UNABLE_DELETE_RATING": "Unable to delete rating",
            "YOU_CANT_RATE_YOUR_OWN_PICTURE": "You cannot rate your own picture",
            "YOU_HAVE_ALREADY_RATED_THIS_PICTURE": "You have already rated this picture",

            # TAGS
            "TAGNAME_NOT_FOUND": "tagname not found",
            "TAGNAME_ALREADY_EXIST": "tagname already exist",
        },
    }

    def __init__(self, language="EN"):
        self.language = language.upper()

    def get_message(self, message: str):
        return self.messages.get(self.language, {}).get(message, "This is not correct key for message")


messages = Message(language=select_language)

if __name__ == "__main__":
    print(messages.get_message("USER_WITH_USERNAME_ALREADY_EXISTS"))