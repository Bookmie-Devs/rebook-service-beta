import qrcode

def generate_qrcode(verification_id):
    qr = qrcode.QRCode(version=1, box_size=10, border=4,)
    qr.add_data(verification_id)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill_color="black", back_color="white")
    return qr_code_image
