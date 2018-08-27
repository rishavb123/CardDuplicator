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
db.reference('server').set('on')

# def getImageExplained():
#     b = bucket.blob("photos/" + s + " - image.jpg")
#     url = bucket.blob("photos/" + s + " - image.jpg").public_url
#     image_read = io.imread(url)
#     image_colors_fixed = cv2.cvtColor(image_read, cv2.COLOR_BGR2RGB)
#     image_resized = cv2.resize(image_colors_fixed, (0, 0), fx=0.3, fy=0.3)
#     rotated =  ndimage.rotate(image_resized, -90)

def getImage():
    return ndimage.rotate(cv2.resize(cv2.cvtColor(io.imread(bucket.blob("image.jpg").public_url), cv2.COLOR_BGR2RGB), (0, 0), fx=0.3, fy=0.3), -90)

def crop(image, rectangle):

    # rotate img
    angle = rectangle[2]
    rows, cols, _ = image.shape
    m = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    img_rot = cv2.warpAffine(image, m, (cols, rows))

    # rotate bounding box
    box = cv2.boxPoints(rectangle)
    pts = np.int0(cv2.transform(np.array([box]), m))[0]
    pts[pts < 0] = 0
    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1],
                       pts[1][0]:pts[2][0]]

    return img_crop


def getCard(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)

    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if len(contours) == 0:
        return img
    card = contours[0]
    perimeter = cv2.arcLength(card, True)
    approx = cv2.approxPolyDP(card, 0.02*perimeter, True)
    rect = cv2.minAreaRect(contours[0])
    # cv2.polylines(img, [approx], True, (0, 255, 255), 5)

    return ndimage.rotate(crop(img, rect), 90)

#--------------------------------IDEA------------------------------------------------------
# Another Way to find the card would by to pick specific predetermined cordinates
# for where to crop the image; I would have to show the client these cordinates somehow tho
#--------------------------------IDEA---------------------------------------------------------

while True:
    if ref.get() == 'start':
        ref.set("doing")
        card = getCard(getImage())
        cv2.imwrite("card-local.jpg", card)
        bucket.blob("card.jpg").upload_from_filename("card-local.jpg")
        ref.set("complete")
    cv2.imshow("image", getImage())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

db.reference('server').set('off')
cv2.destroyAllWindows()
