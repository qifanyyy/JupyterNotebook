from __future__ import print_function
import qrcode
import json
from PIL import Image, ImageOps
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
            return self.matrix[y][x]
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

def getStateMask(M, pX, pY):
    state = 0
    if M.get((pX - 10) // 20, (pY - 10) // 20):
        state |= 0b1000
    if M.get((pX + 10) // 20, (pY - 10) // 20):
        state |= 0b0100
    if M.get((pX + 10) // 20, (pY + 10) // 20):
        state |= 0b0010
    if M.get((pX - 10) // 20, (pY + 10) // 20):
        state |= 0b0001
    return state

def getTileTuple(state):
    xywh = [0, 0, 20, 20]
    xywh[0] = (state %  5) * 20
    xywh[1] = (state // 5) * 20
    xywh[2] += xywh[0]
    xywh[3] += xywh[1]
    return tuple(xywh)

def blit(source, xywh, destination, xy):
    img = source.crop(xywh)
    destination.paste(img, xy)

# version is max "size" of content.
def makeQRcode(url, filename, color="#00FFFF", version=4, tilesetName="round"):
    #### Make QR code
    # 4 for orgsync
    qr = qrcode.QRCode(version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size = 20,
        border = 4
    )
    # url = "https://orgsync.com/89537/events/1400089/occurrences/3175380"
    qr.add_data(url)
    qr.make(fit=False)
    qr.make_image().save("outputs/output_reference.png")
    matrix = qr.get_matrix()
    itr = matrixiterator(matrix)

    #### Load images for pretty QR code
    tileset = Image.open("tiles/tileset_%s.png" % tilesetName)
    eye     = Image.open("tiles/eye_round2.png")

    #### Draw pretty QR code
    dim = itr.dim + 1
    output = Image.new("RGB", (dim*20, dim*20), "#00FFFF")
    for y in range(-10, dim * 20, 20):
        for x in range(-10, dim * 20, 20):
            state = getStateMask(itr, x, y)
            # print("%2d,%2d" % (x//20, y//20) + ":" + "{0:b}".format(state).rjust(4, '0'))
            xywh = getTileTuple(state)
            blit(tileset, xywh, output, (x+10, y+10))
    # draw the eyes
    output.paste(eye, (4 * 20 + 10, 4 * 20 + 10))
    output.paste(eye.transpose(Image.FLIP_LEFT_RIGHT), ((dim-12) * 20 + 10, 4 * 20 + 10))
    output.paste(eye.transpose(Image.FLIP_TOP_BOTTOM), (4 * 20 + 10, (dim-12) * 20 + 10))
    # change color
    mask = ImageOps.invert(output)
    color = Image.new("RGB", (dim*20, dim*20), color)
    output.paste(color, mask=mask.convert("1"))
    # save
    output.save("outputs/" + filename + ".png")

if __name__=="__main__":
    tilesets = ["round", "round2", "angular", "angular2"]
    for ts in tilesets:
        makeQRcode("http://www.google.com", ts, color="#57068c", tilesetName=ts)


# "#324774" blue
# "#57068c" nyu purple