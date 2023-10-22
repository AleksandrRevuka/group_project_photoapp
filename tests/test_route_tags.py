import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Tag, Picture
from src.routes.tags import delete_tag, get_tag, get_tags, tags_of_picture
from src.schemas.tags import TagModel, TagResponse


class TestRouteTags(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.mock_tag = self._create_mock_tag()
        self.mock_tag_response = self._create_tag_response
        self.mock_picture = self._create_mock_picture()
        
    def tearDown(self):
        del self.session
        
    def _create_mock_tag(self):
        tag = Tag()
        tag.id = 1
        tag.tagname = "alex"
        return tag
    
    def _create_tag_response(self):
        tag_response = TagResponse()
        tag_response.id=1,
        tag_response.tagname="old",
        tag_response.created_at=datetime.time,
        tag_response.updated_at=datetime.time
        
    def _create_mock_picture(self):
        picture = Picture()
        picture.id = 1
        picture.user_id = 1
        picture.name = "picture_name_test"
        picture.description = "picture_description_test"
        picture.picture_url = "https://example.com/test.jpg"

        tag1 = Tag(tagname='tag1')
        tag2 = Tag(tagname='tag2')
        tag3 = Tag(tagname='tag3')

        picture.tags_picture.extend([tag1.id, tag2.id, tag3.id])

        return picture
        
    async def test_get_tags(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_tag))
        result = await get_tags(db=self.session)
        self.assertTrue(result)
        
    async def test_get_tag(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_tag))
        result = await get_tag(tag_id=self._create_mock_tag().id, db=self.session)
        self.assertEqual(result.id, self._create_mock_tag().id)
        

    async def test_delete_tag(self):
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_tag))
        result = await delete_tag(tag_id=self._create_mock_tag().id, db=self.session)
        self.assertIsNone(result)
      
   
    async def test_tags_of_picture(self):
        retrieve_tags_for_picture = AsyncMock(return_value=self.mock_picture.tags_picture)
        with patch("src.repository.tags.retrieve_tags_for_picture", retrieve_tags_for_picture):
            result = await tags_of_picture(picture_id=1, db=self.session)

        self.assertTrue(result)
        
    

if __name__ == "__main__":
    unittest.main()           
        
