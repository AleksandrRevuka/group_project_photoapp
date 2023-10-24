import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Picture, Role, Tag, User
from src.repository.pictures import (get_all_pictures,
                                     get_all_pictures_of_user,
                                     get_or_create_tag, get_picture_by_id,
                                     get_qrcode, remove_picture,
                                     save_data_of_picture_to_db,
                                     update_picture_description,
                                     update_picture_name)
from src.schemas.pictures import (PictureDescrUpdate, PictureNameUpdate,
                                  PictureUpload)
from src.conf.messages import messages

class TestRepositoryPictures(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1)
        self.mock_picture, self.mock_tags = self._create_mock_picture()

    def tearDown(self):
        del self.session

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

        return picture, [tag1, tag2, tag3]

    async def test_save_data_of_picture_to_db(self):
        test_picture_data = self.mock_picture
        mock_tags = self.mock_tags

        get_or_create_tag_mock = AsyncMock(return_value=mock_tags[0])
        body_mock = PictureUpload(tags=['tag1', 'tag2', 'tag3'], name="picture_name_test", description="picture_description_test")

        with patch('src.repository.pictures.get_or_create_tag', get_or_create_tag_mock):
            result = await save_data_of_picture_to_db(
                    body=body_mock,
                    picture_url="https://example.com/test.jpg",
                    tag_names=['tag1', 'tag2', 'tag3'],
                    user=self.user,
                    db=self.session
                )

        self.assertEqual(result.name, test_picture_data.name)
        self.assertEqual(result.description, test_picture_data.description)
        self.assertEqual(result.tags_picture[0], mock_tags[0])
        self.assertEqual(result.picture_url, test_picture_data.picture_url)
        self.assertEqual(result.user_id, 1)

    # ---------------------------------------------------------------testing of 'get_or_create_tag' function

    async def test_get_or_create_tag_existing_tag(self):

        tag_name = "TestTag"
        result = await get_or_create_tag(self.session, tag_name)
        self.assertIsNotNone(result)

    async def test_get_or_create_tag_new_tag(self):

        await get_or_create_tag(self.session, 'tag1')

        query = select(Tag).where(Tag.tagname == 'tag1')
        new_tag = await self.session.execute(query)
        new_tag = new_tag.scalar_one_or_none()

        self.assertIsNotNone(new_tag)

    # ---------------------------------------------------------------testing of 'update_picture_name' function
    async def test_update_picture_name_existing_name(self):

        # Picture to update name is found in database and new name - is not empty
        picture_id = self.mock_picture.id
        mock_body = PictureNameUpdate(name="Test name of picture")
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        result = await update_picture_name(id=picture_id, body=mock_body, current_user=self.user.id, db=self.session)

        self.assertEqual(result.name, "Test name of picture")
        self.session.add.assert_called_with(result)
        self.session.commit.assert_awaited_once()
        self.session.refresh.assert_awaited_once_with(result)

    async def test_update_picture_name_not_exist(self):

        # Picture to update name is not found in database
        mock_body = PictureNameUpdate(name="New Name")
        picture_id = self.mock_picture.id

        existing_picture = Mock()
        existing_picture.scalar.return_value = None
        self.session.execute.return_value = existing_picture

        with self.assertRaises(HTTPException):
            await update_picture_name(picture_id, mock_body, self.user.id, self.session)

        existing_picture.scalar.assert_called_once()
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    async def test_update_picture_name_empty_name(self):

        # The new name is an empty string
        picture_id = self.mock_picture.id
        mock_body = PictureNameUpdate(name="")

        # Call a function with an empty name
        with self.assertRaises(HTTPException) as context:
            await update_picture_name(picture_id, mock_body, self.user.id, self.session)

        self.assertEqual(context.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(context.exception.detail, messages.get_message("NAME_OF_PICTURE_CANT_BE_EMPTY"))
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    # ---------------------------------------------------------------testing of 'update_picture_description' function

    async def test_update_picture_description_valid_data(self):

        # Picture to update is found in database and new description is not empty
        mock_body = PictureDescrUpdate(description="New description")
        picture_id = self.mock_picture.id
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        result = await update_picture_description(id=picture_id, body=mock_body, current_user=self.user.id, db=self.session)

        self.assertEqual(result.description, "New description")

        self.session.add.assert_called_with(result)
        self.session.commit.assert_awaited_once()
        self.session.refresh.assert_awaited_once_with(result)

    async def test_update_picture_description_not_exist(self):

        # Picture to update is not found in database
        mock_body = PictureDescrUpdate(description="New description")
        picture_id = self.mock_picture.id

        existing_picture = Mock()
        existing_picture.scalar.return_value = None
        self.session.execute.return_value = existing_picture

        with self.assertRaises(HTTPException) as context:
            await update_picture_description(id=picture_id, body=mock_body, current_user=self.user.id, db=self.session)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, messages.get_message("PICTURE_NOT_FOUND"))

        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    async def test_update_picture_description_empty_description(self):

        # The new description is an empty string
        mock_body = PictureDescrUpdate(description="")
        picture_id = self.mock_picture.id

        # Call a function with an empty description
        with self.assertRaises(HTTPException) as context:
            await update_picture_description(id=picture_id, body=mock_body, current_user=self.user.id, db=self.session)

        self.assertEqual(context.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(context.exception.detail, messages.get_message("DESCRIPTION_OF_PICTURE_CANT_BE_EMPTY"))
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    # ---------------------------------------------------------------testing of 'get_all_pictures' function

    async def test_get_all_pictures(self):

        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        results = await get_all_pictures(skip=0, limit=10, db=self.session)

        for result in results:
            self.assertIsInstance(result, Picture)

    # ---------------------------------------------------------------testing of 'get_picture_by_id' function

    async def test_get_picture_by_id(self):

        test_picture = self.mock_picture
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        results = await get_picture_by_id(id=test_picture.id, db=self.session)

        for result in results:
            self.assertIsInstance(result, Picture)

    # ---------------------------------------------------------------testing of 'get_all_pictures_of_user' function

    async def test_get_all_pictures_of_user(self):

        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        results = await get_all_pictures_of_user(user_id=self.user.id, skip=0, limit=10, db=self.session)

        for result in results:
            self.assertIsInstance(result, Picture)

    # ---------------------------------------------------------------testing of 'remove_picture' function

    async def test_remove_picture_success(self):

        self.user.roles = Role.admin
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        result = await remove_picture(picture_id=self.mock_picture.id, current_user=self.user, db=self.session)

        self.session.delete.assert_called_once_with(result)
        self.session.commit.assert_called_once()

    async def test_remove_picture_not_found(self):

        not_exist_id = 1000
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))
        result = await remove_picture(picture_id=not_exist_id, current_user=self.user, db=self.session)

        self.assertIsNone(result)
        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()

    # ---------------------------------------------------------------testing of 'get_qrcode' function

    async def test_get_qrcode(self):

        expected_qrcode = "https://example.com/test.jpg"
        mock_generate_qrcode = AsyncMock(return_value=expected_qrcode)
        picture = self.mock_picture
        self.session.execute.return_value = MagicMock(scalar=MagicMock(return_value=self.mock_picture))

        with patch('src.services.qrcode_generator.qrcode_generator.generate_qrcode', mock_generate_qrcode):
            result = await get_qrcode(picture_id=picture.id, db=self.session)

        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()

