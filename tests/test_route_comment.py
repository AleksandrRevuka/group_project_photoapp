import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Comment, User
from src.routes.comments import (comments_of_user, comments_to_picture,
                                 create_comment, remove_comment,
                                 update_comment)
from src.schemas.comments import CommentCreate, CommentUpdate


class TestRoutComment(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1)
        self.mock_comment = self._create_mock_comment()
        
    def tearDown(self):
        del self.session
        
    def _create_mock_comment(self):
        comment = Comment()
        comment.id = 1
        comment.text = "comment text"
        comment.picture_id = 1
        return comment
        
    async def test_create_comment(self):
        comment = CommentCreate(user_id=1, text=self.mock_comment.text, picture_id=self.mock_comment.picture_id)
        result = await create_comment(current_user=self.user, picture_id=self.mock_comment.picture_id, body=comment, db=self.session)
        self.assertEqual(result.text, comment.text)
        
    async def test_update_comment(self):
        comment_id = self.mock_comment.id
        mock_body = CommentUpdate(text="Updated comment text")
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await update_comment(comment_id=comment_id, body=mock_body, current_user=self.user, db=self.session)
        self.assertNotEqual(result.text, self._create_mock_comment().text)
        self.assertEqual(result.text, "Updated comment text")  
    

    async def test_remove_comment(self):
        comment_id = self.mock_comment.id
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await remove_comment(comment_id=comment_id, db=self.session)


    async def test_comments_of_user(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await comments_of_user(skip=0, limit=10, user_id=1, db=self.session)
        self.assertTrue(result)
        
    async def test_comments_to_picture(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await comments_to_picture(skip=0, limit=10, picture_id=2, db=self.session)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()           
        
