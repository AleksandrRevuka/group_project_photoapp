import unittest
from unittest.mock import AsyncMock, MagicMock
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
        comment = CommentCreate(user_id=4, text='test comment', picture_id='1')
        result = await create_comment(body=comment, db=self.session)
        self.assertEqual(result.text, comment.text)
        
    async def test_update_comment(self):
        comment_id = 1
        mock_body = CommentUpdate(text="Updated comment text")
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        updated_comment = await update_comment(comment_id=comment_id, body=mock_body, db=self.session)
        self.assertNotEqual(updated_comment.text, self._create_mock_comment().text)
        self.assertEqual(updated_comment.text, "Updated comment text")  
    

    async def test_delete_comment(self):
        comment_id = 2
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await delete_comment(comment_id=comment_id, db=self.session)

    async def test_get_comments_of_user(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await get_comments_of_user(skip=0, limit=10, user_id=1, db=self.session)
        
    async def test_get_comments_to_foto(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_comment))
        result = await get_comments_to_foto(skip=0, limit=10, picture_id=2, db=self.session)


if __name__ == "__main__":
    unittest.main()           
        
