import qrcode
import cv2
from pyzbar.pyzbar import decode
from random import choice
from string import ascii_letters
def generate_qr(data,mode):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    if mode==1:
        name = "dataqr.png"
    else:
        name = "keyqr.png"
    img.save(name)
    if mode==1:
        l = cv2.imread("dataqr.png",cv2.COLOR_RGB2GRAY)
        cv2.imshow("Data_Qr",l)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        l = cv2.imread("keyqr.png",cv2.COLOR_RGB2GRAY)
        cv2.imshow("Key_Qr",l)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def generate_transmission_qr(mode):
    if mode==1:
        s = cv2.imread("dataqr.png",cv2.COLOR_RGB2GRAY)
    else:
        s = cv2.imread("transmission_qr.png",cv2.COLOR_RGB2GRAY)
    t = cv2.imread("keyqr.png",cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
    s = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
    u = cv2.bitwise_xor(s,t)
    u = cv2.threshold(u,1,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)[1]
    if mode==1:
        cv2.imwrite("transmission_qr.png",u)
    else:
        cv2.imwrite("retrieved_qr.png",u)
        l = cv2.imread("retrieved_qr.png")
        s = decode(l)
        text = s[0][0]
        text = str(text,'utf-8')
        print(text)
        cv2.imshow("Retrieved_Qr",l)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def key_qr_text_generator(n):
    s=''.join(choice(ascii_letters) for i in range(n))
    return s

def sender():
    print("**************************************************************")
    print("\n\n")
    print("Enter the text to be Encrypted in QR code: ")
    text = input().strip()
    n = len(text)
    keytext = key_qr_text_generator(n)
    generate_qr(text,1)
    generate_qr(keytext,2)
    generate_transmission_qr(1)
    transmission_qr = cv2.imread("transmission_qr.png",cv2.COLOR_RGB2GRAY)
    cv2.imshow("TRANSMITTED QR CODE",transmission_qr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("**************************************************************")
def receiver():
    print("**************************************************************")
    print("Decrypting the qr code now: ")
    generate_transmission_qr(2)

if __name__ == '__main__':
    print("Welcome to CryptQr Transmission:")
    print("Select 1 for sender encryption:")
    print("Select 2 for receiver decryption:")
    n = int(input())
    if n==1:
        sender()
    print("Press 1 to decrypt the transmission_qrcode")
    n = int(input())
    if n==1:
        receiver()
