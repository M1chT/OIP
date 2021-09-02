
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import pandas as pd
import numpy as np
import argparse
import pickle
import cv2
import os

def build_dataset(df):
	# initialize an empty list to temporarily store the image array
	temp = []

	# loop through the image paths in the data frame
	for imagePath in df.image_path:
		# load the image from disk and convert it from BGR to RGB channel ordering
		img = cv2.imread(os.path.join(dataPath, imagePath))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		# resize the image, change its data-type to *float* and append it to our temporary list
		img = cv2.resize(img, (224, 224))
		temp.append(img.astype("float"))

	# stack the arrays in the temporary variable and get the labels
	data = np.stack(temp)
	labels = np.array(df.coarse_grained_label)

	# encode the labels and convert them in one-hot encoded form
	labels = le.transform(labels)
	labels = to_categorical(labels)

	# return a tuple of the data and labels
	return (data, labels)


np.random.seed(7)

# grab the original dataset path and append with the current working directory
print("[INFO] loading the datasets...")
dataPath = "C:/Users/Michelle Tan/Documents/SCH/Y2.3/OIP/ml/dataset-builder"

# load the classes.csv to properly map the labels
classDF = pd.read_csv(os.path.join(dataPath, "data.csv"))

# filter out the values
col = "Class Name "
print(classDF[col])
classDFShort = \
	classDF[(classDF[col] == "Dry")
		| (classDF[col] == "Wet")
		| (classDF[col] == "Dirty")]

# extract the numerical encoding of the desired classes,
# instantiate the LabelEncoder class, and specify the
# names of the columns with which we wish to load the data files
encodings = classDFShort["Class ID "].unique()
le = LabelEncoder().fit(encodings)
columns = ["image_path", "coarse_grained_label"]

# load the data file containing paths to the images in the
# train set along with their labels and filter out the train set
trainDF = pd.read_csv(os.path.join(dataPath, "dataset/classes.txt"), sep=",", header=None, names=columns)
trainDFShort = trainDF[trainDF.coarse_grained_label.isin(encodings)]


# build the training and testing datasets
print("[INFO] building dataset...")
(trainX, trainY) = build_dataset(trainDFShort)

# split the train set additionally
print("[INFO] splitting the train set additionally...")
(trainX, testX, trainY, testY) = train_test_split(trainX, trainY, test_size = 0.2, stratify = trainY, random_state=42)

# specify the names of the pickle files to save the splits in a tuple
splits = (
	("trainX.cpickle", trainX),
	("trainY.cpickle", trainY),
	("testX.cpickle", testX),
	("testY.cpickle", testY)
)

# loop over the data splits and save them to disk
print("[INFO] serializing the dataset splits...")
for (fileName, split) in splits:
	f = open(os.path.join("C:/Users/Michelle Tan/Documents/SCH/Y2.3/OIP/ml/dataset-builder/preprocessed_data", fileName), "wb")
	f.write(pickle.dumps(split))
	f.close()
