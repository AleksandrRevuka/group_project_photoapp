import unittest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.comments import CommentCreate, CommentUpdate
from src.database.models import Comment, User
from src.repository.comments import (
    create_comment,
    update_comment,
    delete_comment,
    get_comments_of_user,
    get_comments_to_foto
)

class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1)
        
    async def test_create_comment(self):
        comment = CommentCreate(user_id=4, text='test comment', picture_id='1')
        result = await create_comment(body=comment, db=self.session)
        self.assertEqual(result.text, comment.text)
        
    async def test_update_comment(self):
        comment = CommentUpdate(text='New comment')
        result = await update_comment(comment_id=2, body=comment, db=self.session)

        
        
