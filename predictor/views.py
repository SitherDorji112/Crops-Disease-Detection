from django.shortcuts import render
import numpy as np
import os
import cv2
import joblib
import base64
from io import BytesIO
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from django.conf import settings
from django.core.files.storage import default_storage

# Load model & classes
model = load_model(os.path.join(settings.BASE_DIR, "mobilenet_unknown_only.h5"))
class_names = joblib.load(os.path.join(settings.BASE_DIR, "leaf_class_names_with_unknown.pkl"))

#THRESHOLD = 0.7  # confidence threshold


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array


def predict_image(img_path):
    #Predict the leaf disease and return class + confidence
    img_array = preprocess_image(img_path)
    preds = model.predict(img_array)
    confidence = float(np.max(preds))
    predicted_index = np.argmax(preds)
    predicted_class = class_names[predicted_index]
    return predicted_class, confidence



def index(request):
    return render(request, "predictor/index.html")


def upload_page(request):
    return render(request, "predictor/upload.html")


def camera_page(request):
    return render(request, "predictor/camera.html")


def predict_upload(request):
    prediction = None
    if request.method == "POST" and "leaf_image" in request.FILES:
        uploaded_file = request.FILES["leaf_image"]
        file_path = default_storage.save("temp.jpg", uploaded_file)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        predicted_class, confidence = predict_image(full_path)
        os.remove(full_path)

        prediction = {
            "class": predicted_class,
            "confidence": round(confidence * 100, 2)
        }
        
    return render(request, "predictor/upload.html", {"prediction": prediction})

def predict_camera(request):
    prediction = None
    if request.method == "POST":
        data = request.POST.get("camera_image", "")
        if data:
            data = data.split(",")[1]
            image_data = base64.b64decode(data)
            img = Image.open(BytesIO(image_data))
            save_path = os.path.join(settings.MEDIA_ROOT, "camera_temp.jpg")
            img.save(save_path)

            predicted_class, confidence = predict_image(save_path)
            os.remove(save_path)

            prediction = {
                "class": predicted_class,
                "confidence": round(confidence * 100, 2)
            }

    return render(request, "predictor/camera.html", {"prediction": prediction})