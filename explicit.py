from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
import requests
import numpy as np
import cv2
import os
import random



def explicit_img_detector(img_url):
    MODEL_PATH = "./explicit_content_weights/model.h5"
    classifier = load_model(MODEL_PATH)
    labels = ['nsfw', 'sfw']
    IMAGE_LENGTH = 192
    
    response = requests.get(img_url,stream=True)
    response.raw.decode_content = True
    size = (IMAGE_LENGTH,IMAGE_LENGTH)
    img = Image.open(response.raw).resize(size)
    #img_tensor = np.asarray(Image.open(img_url).resize((IMAGE_LENGTH,IMAGE_LENGTH,3)))
    #img = image.load_img(file, target_size=(IMAGE_LENGTH, IMAGE_LENGTH, 3))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    pred_prob = classifier.predict(img_tensor)[0][0]
    #if close to zero it belongs to not safe for work(nsfw) class, else it belongs to safe for work(sfw) class
    pred_class = classifier.predict_classes(img_tensor)[0][0]
    pred_class_dict = {1:'No Explicit Content',0:'Explicit Content'}
    return pred_class_dict[pred_class]

# vals = pred_image("https://pbs.twimg.com/media/D_lJJtJXUAY4qSa.jpg")
# print(vals)