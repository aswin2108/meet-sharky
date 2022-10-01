import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from PIL import Image, ImageOps

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()

# You can also use pretrained model from Keras
# Check https://keras.io/applications/

model ='model.h5'
print('Model loaded. Check http://127.0.0.1:5000/')


def classifier(img, file):
    np.set_printoptions(suppress=True)
    model = keras.models.load_model(file)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = img
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    return prediction



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        image = Image.open(file_path).convert('RGB')
        # Make prediction
        prediction = classifier(image, model)

        # x = x.reshape([64, 64]);
        pest_class = ['Garnet',
        'Ilmenite','Monazite','Rutile','Sillimanite','Zircon'
        ]
        a = prediction[0]
        ind=np.argmax(a)
        print('Suggestion:', pest_class[ind])
        result1=pest_class[ind]
        if result1=="Garnet":
            result="It's Garnet"
        elif result1=="Ilmenite":
            result="It's Ilmenite"
        elif result1=="Monazite":
            result="It's Monazite"
        elif result1=="Rutile":
            result="It's Rutile"
        elif result1=="Sillimanite":
            result="It's Sillimanite"
        elif result1=="Zircon":
            result="It's Zircon"
       
        return result
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    app.run()