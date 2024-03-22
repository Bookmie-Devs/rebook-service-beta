import qrcode
from core.encryptions import encrypt_data

def generate_qrcode(verification_code=None):
    encrypted_code = encrypt_data(verification_code) 
    # verification code for every user
    qr = qrcode.QRCode(version=1, box_size=10, border=4,)
    qr.add_data(encrypted_code)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill_color="black", back_color="white")
    return qr_code_image
