import firebase_admin
from firebase_admin import credentials, storage, db
import numpy as np
import cv2
from skimage import io
from scipy import ndimage

cred = credentials.Certificate("credentials\cred.json")
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://card-duplicator.firebaseio.com/',
    "storageBucket": "card-duplicator.appspot.com",
    'databaseAuthVariableOverride': {
        'uid': 'python-server'
    }
})

bucket = storage.bucket()

ref = db.reference('job')

# def getImageExplained():
#     b = bucket.blob("photos/" + s + " - image.jpg")
#     url = bucket.blob("photos/" + s + " - image.jpg").public_url
#     image_read = io.imread(url)
#     image_colors_fixed = cv2.cvtColor(image_read, cv2.COLOR_BGR2RGB)
#     image_resized = cv2.resize(image_colors_fixed, (0, 0), fx=0.3, fy=0.3)
#     rotated =  ndimage.rotate(image_resized, -90)

def getImage():
    return ndimage.rotate(cv2.resize(cv2.cvtColor(io.imread(bucket.blob("image.jpg").public_url), cv2.COLOR_BGR2RGB), (0, 0), fx=0.3, fy=0.3), -90)

def getCard(img):
    return img

while True:
    if ref.get() == 'start':
        ref.set("doing")
        card = getCard(getImage())
        cv2.imwrite("card-local.jpg", card)
        bucket.blob("card.jpg").upload_from_filename("card-local.jpg")
    cv2.imshow("image", getImage())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
