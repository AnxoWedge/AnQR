from flask import Flask, request, send_file
import qrcode
from PIL import Image
import qrcode.constants
import os

app = Flask(__name__)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    url = data.get('url')
    logo_link = data.get('logo', None)  # Optional logo link

    # Check if URL is provided
    if not url:
        return {"error": "URL is required"}, 400

    # Check if logo exists and open it if provided
    logo = None
    if logo_link:
        try:
            logo = Image.open(logo_link)
            # width 
            basewidth = 150

            # adjust image size 
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        except FileNotFoundError:
            logo = None  # Logo is optional, set to None if not found

    # Create QR code
    Qrcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    Qrcode.add_data(url)
    Qrcode.make()

    # Asking for color and adding color
    QRcolor = '#000'
    BGcolor = '#fff'

    # Generate the QR code image
    QRimg = Qrcode.make_image(
        fill_color=QRcolor,
        back_color=BGcolor,
    ).convert('RGB')

    # If logo is provided, paste it on the QR code
    if logo:
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

    # Save the QR code image
    qr_code_path = 'QRgenerated.png'
    QRimg.save(qr_code_path)

    return send_file(qr_code_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)