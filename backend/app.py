from flask import Flask, request, send_file
from flask_cors import CORS
import segno
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    url = data.get('url')
    color = data.get('color', "#000")
    bgcolor = data.get('bgcolor', "#fff")
    logo_link = data.get('logo', None)  # Optional logo link

    # Check if URL is provided
    if not url:
        return {"error": "URL is required"}, 400

    # Generate QR code with Segno
    qr = segno.make(url, error='h')

    # Save QR code to an in-memory buffer with custom colors
    buff = io.BytesIO()
    qr.save(buff, kind='png', scale=8, dark=color, light=bgcolor)
    buff.seek(0)

    # Open QR as image for possible logo addition
    QRimg = Image.open(buff).convert("RGBA")

    # If logo is provided, paste into QR
    if logo_link:
        try:
            logo = Image.open(logo_link).convert("RGBA")
            # Resize logo to fit inside QR code
            basewidth = QRimg.size // 3
            wpercent = basewidth / float(logo.size)
            hsize = int((float(logo.size[13]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            # Center logo
            pos = ((QRimg.size - logo.size) // 2,
                   (QRimg.size[13] - logo.size[13]) // 2)
            QRimg.paste(logo, pos, mask=logo)
        except FileNotFoundError:
            pass

    # Save final image and send
    out_buff = io.BytesIO()
    QRimg.save(out_buff, format='PNG')
    out_buff.seek(0)
    return send_file(out_buff, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
