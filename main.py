from flask import Flask, render_template, request, jsonify
import json
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask_wtf.csrf import CSRFProtect
import base64

import pytesseract
from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np
from werkzeug.datastructures import ImmutableMultiDict



app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
# csrf = CSRFProtect(app)



pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.3/bin/tesseract'
# def process_image(image_blob, image_dimension):
def process_image(image_blob, image_width, image_height):
    image = Image.open(BytesIO(image_blob))

    resize_image = image.resize((image_width, image_height))
    image_array = np.array(resize_image)
    # image = Image.open(image_blob)
    check_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # micr_img = check_img[0:1186, 0:1344]
    micr_img = check_img[0:image_height, 0: image_width] = image_array
    # micr_img = check_img[0:image_width, 0:image_height]

    tessdata_dir_config = r'--tessdata-dir "/usr/local/Cellar/tesseract-lang/4.1.0/share/tessdata"'

    micr_text = pytesseract.image_to_string(micr_img, lang='mcr', config=tessdata_dir_config)

    return micr_text


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    # form = UploadFileForm()
    # if form.validate_on_submit():
    #     file = form.file.data # First grab the file
    #     file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
    #     return "File has been uploaded."
    # return render_template('index.html', form=form)
    return render_template('index.html')


@app.route("/upload", methods=["POST"])
def upload_file():
    # if 'image' not in request.files:
    #     return jsonify({'error': 'No image part'})
    data = request.json
    image_height = data.get('image_height')
    image_width = data.get('image_width')
    base64_string = data.get('image', '')

    print("imageW", image_width)
    print("imageH", image_height)

    if base64_string == "":
        return jsonify({'error': 'No image part'})

    # Remove the "data:image/jpeg;base64," prefix
    image_data = base64_string.split(',')[1]

    # Decode base64 string to bytes
    image_bytes = base64.b64decode(image_data)

    # Open the image using PIL
    micr_text = process_image(image_bytes, image_width, image_height)
    response = {
        'micr_text': micr_text
    }

    return jsonify(response)
    # return micr_text  # Return just the string directly


if __name__ == '__main__':
    app.run(debug=True)