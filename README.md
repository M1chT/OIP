# iRinse - Group 28
### A powerful 3 in 1 machine that washes, sterilizes and dries syringes.

<p align="center"><a href="https://ibb.co/Nm9zLx2"><img src="https://i.ibb.co/Nm9zLx2/desing-removebg-preview.png" alt="desing-removebg-preview" border="0"></a></p>
This project, the team have used Arduino, 2 Raspberry Pi to operate our iRinse. The iRinse is designed for its compactness, safety and bacterial-free.

## Project Structure
    .
    ├── Arduino                           # Arduino Communications and Sensors Code
    ├── Machine Learning Training         # Machine Learning Training codes - VGG16 & ResNet50
    ├── Main Raspberry Pi                 # Web-UI Flask and XML-RPC communication code
    ├── Secondary Raspberry Pi            # XML-RPC Communication and prediction code
    └── README.md

## How to Use
Arduino Folder: Import the arduino folder into the Arduino
Machine Learning Training: Import the .ipynb files onto Google Collab/Juypter Notebook to run it
Main Raspberry Pi: The code from this folder, import it into a Raspberry Pi and pip install the required libraries
Secondary Raspberry Pi: The code from this folder, import into the same Raspberry Pi or different Raspberry Pi, just change the IP Address accordingly and pip install the required libraries
