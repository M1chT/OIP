import tensorflow as tf
import cv2
#from picamera import PiCamera
import time
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np


server_add = "192.168.120.227"

# Load the tensorflow model
def loadmodel():
     global loaded_model
     loaded_model = tf.keras.models.load_model('model/myModel.h5')  # load tensorflow model
     print("[INFO]Model Loaded Successfully...")

     return "Model Loaded..."


# prepare the input image into what the model desire
def prepare(filepath):
    IMAGE_SIZE = 224  # set the image size to 224
    img_array = cv2.imread(filepath)  # read the image in
    new_array = cv2.resize(img_array, (IMAGE_SIZE, IMAGE_SIZE))  # resize the image
    new_image = new_array.reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 3)  # reshape the image to what the model desire
    return new_image


# predicting the input image
def prediction(model, imgpath):
    test = model.predict([prepare(imgpath)])
    print("[INFO] Predicting...")
    predict = test.argmax()  # predict the categories
    status = ""
    if predict == 0:
        status = "Dry"
    elif predict == 1:
        status = "Wet"
    else:
        status = "Dirty"
    print(status)
    # output the predicted results onto the image
    original = Image.open(imgpath)
    draw = ImageDraw.Draw(original)
    font = ImageFont.truetype('arial.ttf', 50)
    txt = "Predicted Label: " + status + " , Accuracy: " + str(round(accuracy * 100)) + "%"
    draw.text((10, 10), txt, font=font, fill=(255,0,0,255))
    original.save("output.png")

    return status


def server_receive_file(arg):
    with open("C:/Users/Michelle Tan/Documents/SCH/Y2.3/OIP/final_oip/oip/img.jpg", "wb") as handle:
        handle.write(arg.data)
        return True


# call the load model function
def predicting():
    t0 = time.time()
    ## prediction
    img = "C:/Users/Michelle Tan/Documents/SCH/Y2.3/OIP/final_oip/oip/img.jpg"
    result = prediction(loaded_model, img)
    t1 = time.time()
    total = t1-t0
    print("Total Time for detecting " + str(total) +" sec")
    return result


class RequestHandler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        # print(client_address[0]) # do what you need to do with client_address here
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)


with SimpleXMLRPCServer((server_add, 8001), requestHandler=RequestHandler) as server:
    server.register_function(loadmodel, "loadmodel")
    server.register_function(predicting, "predicting")
    server.register_function(server_receive_file, "server_receive_file")
    print('Serving initiating...')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
