from datetime import datetime
import unittest
from typing import List
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Role, User
from src.repository.users import (activate_user, ban_user, change_password,
                                  change_role, confirmed_email, create_user,
                                  edit_my_profile, get_all_users,
                                  get_user_by_email, get_user_profile,
                                  get_user_username, invalidate_token,
                                  is_validate_token, update_token)
from src.schemas.users import UserModel, UserProfile


class TestRepositoryPictures(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.mock_user = self._create_mock_user()

    def tearDown(self):
        del self.session

    def _create_mock_user(self):
        user = User()
        user.id = 1
        user.username = "username_test"
        user.email = "email_test@gmail.com"
        user.confirmed = False
        user.password = "password_test"
        user.avatar = "https://www.gravatar.com/avatar/test"
        user.roles = Role.user
        user.is_active = True
        return user

    async def test_get_user_by_email_exist(self):
        search_email = "email_test@gmail.com"
        
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = self.mock_user
        self.session.execute.return_value = mock_result
        
        search_user = await get_user_by_email(search_email, self.session)
        
        self.assertEqual(search_user.username, self.mock_user.username)
        self.assertEqual(search_user.email, self.mock_user.email)
        self.assertEqual(search_user.id, self.mock_user.id)
        
    async def test_get_user_by_email_none(self):
        search_email = "not_exist_email_test@gmail.com"
        
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = None
        self.session.execute.return_value = mock_result
        
        search_user = await get_user_by_email(search_email, self.session)
        
        self.assertEqual(search_user, None)
        
    async def test_create_user(self):
        body = UserModel(username="username_test", email="email_test@gmail.com", password="password_test")

        mock_result = MagicMock()
        mock_result.scalar.return_value = self.mock_user
        self.session.execute.return_value = mock_result
        
        new_user = await create_user(body, self.session)

        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, "username_test")
        
    async def test_create_user_admin(self):
        body = UserModel(username="username_test", email="email_test@gmail.com", password="password_test")

        mock_result = MagicMock()
        mock_result.scalar.return_value = None
        self.session.execute.return_value = mock_result
        
        new_user = await create_user(body, self.session)

        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, "username_test")
        self.assertEqual(new_user.roles, "admin")

    async def test_update_token(self):
        refresh_token = "refresh_token_test"
        
        self.assertIsNone(self.mock_user.refresh_token) 
        await update_token(self.mock_user, refresh_token, self.session)

        self.assertEqual(self.mock_user.refresh_token, refresh_token)
        
    async def test_confirmed_email(self):
        self.assertFalse(self.mock_user.confirmed)
        
        get_user_by_email_mock = AsyncMock(return_value=self.mock_user)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            await confirmed_email(self.mock_user.email, self.session)
            
        self.assertTrue(self.mock_user.confirmed) 
            
    async def test_edit_my_profile(self):
        pass
    
    async def test_change_password(self):
        password_mock = "new_password"
        
        self.assertEqual(self.mock_user.password, "password_test")
        
        await change_password(self.mock_user, password_mock, self.session)
        
        self.assertEqual(self.mock_user.password, "new_password")
        
    async def test_get_user_username(self):
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.mock_user
        self.session.execute.return_value = mock_result
        
        user = await get_user_username(self.mock_user.username, self.session)
        
        self.assertEqual(user.username, self.mock_user.username)
        
    async def test_get_user_username_none(self):
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mock_result
        
        user = await get_user_username(self.mock_user.username, self.session)
        
        self.assertEqual(user, None)
            
    async def test_get_all_users(self):
        users_mock = [self.mock_user, User(id=2), User(id=3)]
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = users_mock
        self.session.execute.return_value = mock_result
        
        users = await get_all_users(0, 10, self.session)
        
        self.assertIsInstance(users, List)
        self.assertEqual(users[0].username, self.mock_user.username)
        
    async def test_get_user_profile(self):
        mock_result = MagicMock()
        mock_result.scalar.return_value = 5
        self.session.execute.return_value = mock_result
        with patch("src.schemas.users.UserProfile") as user_profile_mock:
            profile_mock =  user_profile = UserProfile(
                                                    id=self.mock_user.id,
                                                    roles=self.mock_user.roles,
                                                    username=self.mock_user.username,
                                                    email=self.mock_user.email,
                                                    avatar=self.mock_user.avatar,
                                                    is_active=self.mock_user.is_active,
                                                    pictures_count=4,
                                                    comments_count=10,
                                                    confirmed=self.mock_user.confirmed,
                                                    created_at=datetime(2023, 1, 1),
                                                    updated_at=datetime(2023, 1, 1),
                                                )
            user_profile_mock.return_value = profile_mock
            
            user_profile = await get_user_profile(self.mock_user, self.session)
            
        self.assertEqual(user_profile.id, self.mock_user.id)
        self.assertEqual(user_profile.pictures_count, 5)
        self.assertEqual(user_profile.comments_count, 5)
        
        
    async def test_get_user_profile_none(self):
            
        user_profile = await get_user_profile(None, self.session)
            
        self.assertEqual(user_profile, None)
        
        
    async def test_ban_user(self):
        self.assertTrue(self.mock_user.is_active)
        
        get_user_by_email_mock = AsyncMock(return_value=self.mock_user)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            await ban_user(self.mock_user.email, self.session)
            
        self.assertFalse(self.mock_user.is_active) 
        
        
    async def test_ban_user_none(self):
        self.assertTrue(self.mock_user.is_active)
        
        get_user_by_email_mock = AsyncMock(return_value=None)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            user = await ban_user(self.mock_user.email, self.session)
            
        self.assertFalse(user)
        
    async def test_activate_user(self):
        self.assertTrue(self.mock_user.is_active)
        
        get_user_by_email_mock = AsyncMock(return_value=self.mock_user)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            await ban_user(self.mock_user.email, self.session)
        
        self.assertFalse(self.mock_user.is_active) 
        
        get_user_by_email_mock = AsyncMock(return_value=self.mock_user)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            await activate_user(self.mock_user.email, self.session)
            
        self.assertTrue(self.mock_user.is_active)
    
    async def test_activate_user_none(self):
        
        get_user_by_email_mock = AsyncMock(return_value=None)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            user = await activate_user(self.mock_user.email, self.session)
            
        self.assertFalse(user)
        
    async def test_invalidate_token(self):
        token = "test_token"

        await invalidate_token(token, self.session)

    async def test_is_validate_token(self):
        token = "test_token"
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = token 
        self.session.execute.return_value = mock_result
            
        result = await is_validate_token(token, self.session)
            
        self.assertTrue(result)
        
    async def test_is_validate_token_not_exist(self):
        token = "test_token"
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None 
        self.session.execute.return_value = mock_result
            
        result = await is_validate_token(token, self.session)
            
        self.assertFalse(result)
        
    async def test_change_role(self):
        get_user_by_email_mock = AsyncMock(return_value=self.mock_user)
        role = Role.admin
        self.assertEqual(self.mock_user.roles, Role.user)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            user = await change_role(self.mock_user.email, role, self.session)

        self.assertEqual(user.roles, role)
        
    async def test_change_role_user_none(self):
        get_user_by_email_mock = AsyncMock(return_value=None)
        role = Role.admin
        self.assertEqual(self.mock_user.roles, Role.user)
        
        with patch("src.repository.users.get_user_by_email", get_user_by_email_mock):
            user = await change_role(self.mock_user.email, role, self.session)

        self.assertEqual(user, None)
        
                
if __name__ == "__main__":
    unittest.main()