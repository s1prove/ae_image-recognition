from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model 
from tensorflow.keras.preprocessing import image  

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


autoencoder = load_model('modelCifar100_86-81percents.h5')

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/archive')
def archive():
    return render_template('archive.html', archive_data=archive_data)

archive_data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    original_img = None
    decoded_img = None

    if request.method == 'POST':
        
        if 'photo' not in request.files:
            return redirect(request.url)
        
        file = request.files['photo']

        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            original_img = os.path.join('static', 'uploads', filename)
            decoded_img = os.path.join('static', 'decoded', filename)

            input_img = image.load_img(file_path)
            input_width, input_height = input_img.size


            img = image.load_img(file_path, target_size=(32, 32)) 
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0
            reconstructed_img = autoencoder.predict(img_array)
            reconstructed_img = (reconstructed_img * 255).astype(np.uint8)
            reconstructed_img = image.array_to_img(reconstructed_img[0])

            reconstructed_img = reconstructed_img.resize((input_width, input_height))

        
            archive_data.append({'original_img': original_img, 'decoded_img': decoded_img})

            decoded_img = os.path.join('static', 'decoded', filename)
            reconstructed_img.save(decoded_img)


    return render_template('index.html', original_img=original_img, decoded_img=decoded_img)

if __name__ == '__main__':
    app.run(debug=True)
