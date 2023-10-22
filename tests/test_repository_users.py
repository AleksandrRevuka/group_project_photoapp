import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Picture, Role, Tag, User
from src.repository.users import (activate_user, ban_user, change_password,
                                  change_role, confirmed_email, create_user,
                                  edit_my_profile, get_all_users,
                                  get_user_by_email, get_user_profile,
                                  get_user_username, invalidate_token,
                                  is_validate_token, update_token)
from src.schemas.pictures import (PictureDescrUpdate, PictureNameUpdate,
                                  PictureUpload)


class TestRepositoryPictures(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.mock_user, self.mock_tags = self._create_mock_user()

    def tearDown(self):
        del self.session

    def _create_mock_user(self):
        user = User()
        user.id = 1
        user.username = "username_test"
        user.email = "email_test@gmail.com"
        user.confirmed = True
        user.password = "password_test"
        user.refresh_token = "refresh_token_test"
        user.avatar = "https://www.gravatar.com/avatar/test"
        user.roles = Role.admin
        user.is_active = True

        # user.pictures =
        # user.comments_user =
        # user.ratings =

        # tag1 = Picture(tagname='tag1')
        # tag2 = Picture(tagname='tag2')
        # tag3 = Tag(tagname='tag3')

        # picture.tags_picture.extend([tag1.id, tag2.id, tag3.id])

        return user
