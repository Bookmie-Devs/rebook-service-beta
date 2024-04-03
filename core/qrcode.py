import qrcode
from qrcode.main import QRCode
from PIL import Image
from core.encryptions import encrypt_data


def generate_qrcode(verification_code=None):
    encrypted_code = encrypt_data(verification_code) 
    # verification code for every user
    qr = QRCode(version=1, box_size=10, border=4,  error_correction=qrcode.constants.ERROR_CORRECT_H)
    # print(encrypted_code)
    qr.add_data(encrypted_code)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    logo = Image.open('core/logo_img/logo.jpg')
    logo = logo.resize((500, 150), Image.LANCZOS)

    qr_code_image.paste(logo, ((qr_code_image.size[0]-logo.size[0])//2, (qr_code_image.size[1]-logo.size[1])//2))
    return qr_code_image
