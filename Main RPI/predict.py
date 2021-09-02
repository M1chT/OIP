import tensorflow as tf
import cv2
from picamera import PiCamera
import time

    
## take picture
def takepic():
    print("[INFO]Taking Picture...")
    camera = PiCamera()
    camera.capture("/home/pi/ml/img.jpg")
    print("[INFO]Picture Taken...") 
    
    

# Load the tensorflow model
def loadmodel():
     loaded_model = tf.keras.models.load_model('model/myModel.h5')  # load tensorflow model
     print("[INFO]Model Loaded Successfully...")
    
     return loaded_model


# prepare the input image into what the model desire
def prepare(filepath):
    IMAGE_SIZE = 224  # set the image size to 224
    img_array = cv2.imread(filepath)  # read the image in
    new_array = cv2.resize(img_array, (IMAGE_SIZE, IMAGE_SIZE))  # resize the image
    new_image = new_array.reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 3)  # reshape the image to what the model desire
    return new_image


# predicting the input image
def prediction(model,imgpath):
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
    return status
    


## MAIN PROGRAM START HERE

# call the load model function
def predicting():
    t0 = time.time()
    loaded_model = loadmodel()
    takepic()
    ## prepare the image
    img = "/home/pi/ml/img.jpg"
    ## prediction
    result = prediction(loaded_model, img)
    t1 = time.time()
    total = t1-t0
    print("Total Time for detecting " + str(total) +" sec")
    return result
