import pyqrcode
import png
from pyqrcode import QRCode
import cv2 as cv

from pyngrok import ngrok

# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">
http_tunnel = ngrok.connect(5000)
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1\"".format(http_tunnel.public_url))










def mouseClick(events, x, y, flags, params):
    if(events== cv.EVENT_LBUTTONDOWN):
        cv.destroyAllWindows()
        exit()
    
# def qrfunc():
s =http_tunnel.public_url
url = pyqrcode.create(s)

# url.svg("myqr.svg", scale = 8)

url.png('qr.png', scale = 6)
cv.waitKey(500)

img = cv.imread('qr.png')
while True:
    cv.imshow("QR", img)
    cv.setMouseCallback("QR", mouseClick)
    cv.waitKey(10)
# qrfunc()