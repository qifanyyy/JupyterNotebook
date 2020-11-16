from __future__ import print_function
import qrcode
import json
from PIL import Image
import sys
class matrixiterator:
    def __init__(self, mat):
        self.matrix = mat
        self.dim = len(mat)

    def __iter__(self):
        for i in range(self.dim):
            for j in range(self.dim):
                yield (i, j)

    def get(self, x, y):
        if 0 <= x < self.dim and 0 <= y < self.dim:
            return self.matrix[x][y]
        return False

    def getNeighborState(self, x, y):
        # Encodes the von neumann neighbor state as a 4 bit number.
        x, y = y, x
        state = 0
        if self.get(x, y) == False:
            state += 16
        if self.get(x, y-1):
            state += 1
        if self.get(x+1, y):
            state += 2
        if self.get(x, y+1):
            state += 4
        if self.get(x-1, y):
            state += 8
        return state




#### Make QR code
# 4 for orgsync
qr = qrcode.QRCode(version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size = 20,
    border = 4
)
url = "https://orgsync.com/89537/events/1400089/occurrences/3175380"
# url = "www.google.com"
qr.add_data(url)
qr.make(fit=False)
qr.make_image().save("test.png")
matrix = qr.get_matrix()

#### Load images for pretty QR code
rotationInfo = json.load(open("rotations.json"))
rotationArray = []
tilearray = {} # preload all images into memory, only once
imgsrc = "resources/" + sys.argv[1]
for i in range(32):
    rotationArray.append(rotationInfo[str(i)])
    imgname = rotationArray[-1]["img"]
    if imgname not in tilearray:
        tilearray[imgname] = Image.open(imgsrc + "/" + imgname)

#### Draw pretty QR code
states = {}
itr = matrixiterator(matrix)
output = Image.new("RGB", (itr.dim*20, itr.dim*20), "#00FFFF")
for i, j in itr:
    state = itr.getNeighborState(i, j)
    if state not in states:
        lookup = rotationArray[state]
        imgname = lookup["img"]
        img = tilearray[imgname]
        rotation = lookup["rot"]
        states[state] = img.rotate(rotation)
        stateimg = states[state]
    else:
        stateimg = states[state]
    output.paste(stateimg, (i*20, j*20))
output.save(imgsrc.split("/")[-1] + ".png")