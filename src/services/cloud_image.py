import hashlib

import cloudinary
import cloudinary.uploader
import cloudinary.api

from src.conf.config import settings


class CloudImage:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def generate_folder_name(email: str):
        folder_name = hashlib.sha256(email.encode('utf-8')).hexdigest()[12]
        return folder_name

    @staticmethod
    def upload_image(file, public_id: str):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_for_image(public_id, r):
        src_url = cloudinary.CloudinaryImage(public_id).build_url(width=350, height=350, crop='fill',
                                                                  version=r.get('version'))
        return src_url

