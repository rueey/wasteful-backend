import requests
import json
from cv2 import *
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
    imshow("cam-test",img)
    waitKey(0)
    destroyWindow("cam-test")
    imwrite("filename.jpg",img) #save image

f = open('query.jpg', 'rb')
r = requests.post('http://127.0.0.1:5000/predict', files={'image': f})
d = json.loads(r.text)
a = [d[x] for x in d.keys()]
sorted(a)
a.reverse()
print(a[0])