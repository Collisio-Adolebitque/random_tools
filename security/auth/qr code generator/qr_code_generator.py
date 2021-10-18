import qrcode
import sys
from PIL import Image


# OTP Key URI format: otpauth://TYPE/LABEL:USER?PARAMETERS
# E.g. otpauth://totp/Demo:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
otp_auth_key_type = "totp"
otp_auth_key_label = sys.argv[1] 
otp_auth_key_label_user = sys.argv[2] 
otp_auth_key_label_secret = sys.argv[3]
otp_auth_key_label_issuer = sys.argv[4] 
otp_auth_qrcode_filename = sys.argv[5]


def generate_qr_code(otp_auth_key_type="totp", otp_auth_key_label="Demo", otp_auth_key_label_user="alice@google.com", otp_auth_key_label_secret="JBSWY3DPEHPK3PXP", otp_auth_key_label_issuer="Example", otp_auth_qrcode_filename="inverse_graph.png") -> str:
    # Encode OTP Auth Key URI data
    data = f"otpauth://{otp_auth_key_type}/{otp_auth_key_label}:{otp_auth_key_label_user}?secret={otp_auth_key_label_secret}&issuer={otp_auth_key_label_issuer}"
    # instantiate QRCode object
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10, 
        border=4
        )
    
    qr.add_data(data)  # Add data to the QR code
    qr.make(fit=True)  # Compile the data into a QR code array
    qr_code_array = qr.make_image(fill_color="black", back_color="white")  # Create the image.
    qr_code_array.save(otp_auth_qrcode_filename)  # Save the image.

    return f"QR Code: {otp_auth_key_label} generated in: {otp_auth_qrcode_filename}."

if __name__ == '__main__':
    if len(sys.argv) > 4 and len(sys.argv) < 7:
        try: 
            qr_code = generate_qr_code(otp_auth_key_type, otp_auth_key_label, otp_auth_key_label_user, otp_auth_key_label_secret, otp_auth_key_label_issuer, otp_auth_qrcode_filename)
        except Exception as err:
            print(f"Something broke: {err}")
        finally:
            print(f"{qr_code}")
            im = Image.open(otp_auth_qrcode_filename)
            im.show(im)
