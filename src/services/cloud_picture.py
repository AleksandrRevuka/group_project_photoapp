import hashlib

import cloudinary
import cloudinary.uploader
import cloudinary.api

from src.conf.config import settings


class CloudPicture:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    @staticmethod
    def generate_folder_name(email: str):
        """
        The generate_folder_name function takes in an email address as a string and returns the first character of the
        SHA256 hash of that email address.

        :param email: str: Specify the type of parameter that is expected to be passed into the function
        :return: A string
        """

        folder_name = hashlib.sha256(email.encode("utf-8")).hexdigest()[12]
        return folder_name

    @staticmethod
    def upload_picture(file, public_id: str, transformation: dict = {}):
        """
        The upload_picture function takes in a file, public_id, and transformation.
            The function then uploads the picture to cloudinary with the given public_id and transformation.
            It returns a dictionary containing information about the uploaded picture.

        :param file: Specify the file to upload
        :param public_id: str: Specify the name of the file that is being uploaded
        :param transformation: dict: Specify the transformation that will be applied to the image
        :return: A dict with the image's url, id and more
        """

        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True, transformation=transformation)
        return r

    @staticmethod
    def get_url_for_picture(public_id, r):
        """
        The get_url_for_picture function takes in a public_id and an r (which is the result
        of a cloudinary.api.resources() call) and returns the url for that picture, with width=350, height=350,
        crop='fill', and version = r['version']

        :param public_id: Identify the image in cloudinary
        :param r: Get the version of the image
        :return: A url for a picture
        """

        src_url = cloudinary.CloudinaryImage(public_id).build_url(width=350, height=350, crop="fill", version=r.get("version"))
        return src_url
