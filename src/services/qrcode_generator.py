import qrcode
import base64
import mimetypes
import requests
from io import BytesIO


class QRGenerator:
    @staticmethod
    def generate_qrcode(link: str):
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
