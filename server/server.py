import firebase_admin
from firebase_admin import credentials, storage, db
import numpy as np
import cv2
from skimage import io

cred = credentials.Certificate("credentials\cred.json")
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://databaseName.firebaseio.com',
    "storageBucket": "card-duplicator.appspot.com",
    'databaseAuthVariableOverride': {
        'uid': 'python-server'
    }
})

bucket = storage.bucket()

ref = db.reference('job')
print ref.get()

def getImageExplained(s):
    b = bucket.blob("photos/" + s + " - image.jpg")
    url = bucket.blob("photos/" + s + " - image.jpg").public_url
    image_read = io.imread(url)
    image_colors_fixed = cv2.cvtColor(image_read, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_colors_fixed, (0, 0), fx=0.3, fy=0.3)
    return image_resized

def getImage(s):
    return cv2.resize(cv2.cvtColor(io.imread(bucket.blob("photos/" + s + " - image.jpg").public_url), cv2.COLOR_BGR2RGB), (0, 0), fx=0.3, fy=0.3)

cv2.imshow("image", getImage("4yb1kyjavjph9xgpg7l86w"))

cv2.waitKey(0)
cv2.destroyAllWindows()
