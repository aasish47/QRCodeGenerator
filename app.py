import os
from flask import Flask, render_template, request, send_file
import qrcode

app = Flask(__name__)

# Our Home page
@app.route('/')
def index():
    return render_template('index.html')

# redirecting to the qr generating phase and opening the qr generated page
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form['data']
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="black")

    # Use the static folder to store the QR code image
    static_folder = os.path.join(app.root_path, 'static')
    img_path = os.path.join(static_folder, 'qrcode.png')
    img.save(img_path)
    return render_template('qrcode.html')

# downloading the qr
@app.route('/download_qr')
def download_qr():
    static_folder = os.path.join(app.root_path, 'static')
    img_path = os.path.join(static_folder, 'qrcode.png')
    return send_file(img_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
