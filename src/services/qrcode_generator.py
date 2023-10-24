import qrcode
import base64
import mimetypes
import requests
from io import BytesIO


class QRGenerator:
    @staticmethod
    def generate_qrcode(link: str):
        """
        The generate_qrcode function takes a link as an argument and returns the base64 encoded QR code of that link.
        The function first makes a GET request to the URL provided in order to get its content type. If it is successful, 
        it then uses mimetypes library's guess_extension method to determine what format the object at that URL is in
        (e.g., .png, .jpg). 
        If it can successfully determine this format, it then creates a QR code using qrcode library's make method and saves 
        this image into memory using BytesIO(). 
        It then encodes this image into base64 encoding
        
        :param link: str: Specify the url that will be used to generate the qr code
        :return: A string containing a base64-encoded qr code image

        """
        response = requests.get(link)

        if response.status_code == 200:
            content_type = response.headers.get("content-type")

            if content_type is not None:
                object_format = mimetypes.guess_extension(content_type)

                if object_format:
                    qrcode_img = qrcode.make(link)
                    buffered = BytesIO()
                    qrcode_img.save(buffered)
                    base64code_object = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    complete_qr_code = f"data:{content_type};base64,{base64code_object}"

                    return complete_qr_code
                else:
                    return "Unknown data format"
            else:
                return "Unknown content type"
        else:
            return "Failed to fetch content from URL"


qrcode_generator = QRGenerator()
