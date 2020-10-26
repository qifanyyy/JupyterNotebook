from ScanInvedio import detect
from rsa_sig import rsa_sign, rsa_verify
import qrcode
import argparse

const_private_key = '''-----BEGIN PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAyQDti8YVmfrAIm6Pm3
XN3MZWRH0XiIVqRC6nmdd0twDayZ3epsHbB/RBOM7QOxYRDBqUv8F9vlrBdWYnyey6
iQIDAQABAkA2JGbYEIo/CLj6TVenY2sJPe980Ukmf/Fo3jxNByksJbdjFJx6a3iyP8
G3GSjj5wKdO/yG4+xEfQvw+rr103rVAiEA7/keSShXBmeUApLJN8CZh22ntFAsVPF0
n0tIoovlJqMCIQDWbYnI/TxzwjO5ietRjKEwyr4z0qq07NeCaZgptqYo4wIgMrp42o
I6k1IGCd05yB1g1y4pC4b/OB2qx5nEiwgDsv0CIQCQYx4eqvbj8+ckjoxYU1vPIRZG
ixrLzZeohzYhEI5+hQIhAM52I8kzZHhNbEoWftdIHbIKa5PXmJ+mqgrSoOupo3yn
-----END PRIVATE KEY-----
'''

const_public_key = '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMkA7YvGFZn6wCJuj5t1zdzGVkR9F4iFak
Qup5nXdLcA2smd3qbB2wf0QTjO0DsWEQwalL/Bfb5awXVmJ8nsuokCAwEAAQ==
-----END PUBLIC KEY-----
    '''

def qrcode_generate(private_key = const_private_key):
    print(private_key)
    message = input("input message:")
    signature = rsa_sign(message.encode(encoding='utf-8'), private_key)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=2
    )

    qrcode_message = message + "$" + signature.hex() + "$"
    print(qrcode_message)
    qr.add_data(qrcode_message)

    qr.make(fit=True)
    img = qr.make_image()
    img.save('qrcode.png')
    img.show()

def qrcode_varify(public_key = const_public_key):
    print(public_key)
    print("opening camera...")
    context = detect()

    if len(context) <= 130:
        print("normal urcode:\n" + context)
        return
    if context[-1] == "$" and context[-130] == "$":
        print("normal urcode:\n" + context)
        return

    sig_now = context[-129:-1]
    message = context[:-130]

    print(sig_now + '\n' + message)

    result = rsa_verify(bytes.fromhex(sig_now), message.encode('utf-8'), public_key)

    print("context: " + message)
    if result == True:
        print("status: True message.")
    else:
        print("status: Fake message!")

def parse_args():
    parser = argparse.ArgumentParser(description="Tools for qrcodes.")
    parser.add_argument("action", choices={"generate", "identify"}, action="store")
    parser.add_argument("-e", "--pri", dest="pri_key_file", help="pri.key")
    parser.add_argument("-d", "--pub", dest="pub_key_file", help="pub.key")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.action == "identify":
        if args.pub_key_file:
            f = open(args.pub_key_file, "r")
            const_public_key = f.read()
            f.close()
        else:
            print("No public key is provided. Use default key.\n")
        qrcode_varify()
    elif args.action == "generate":
        if args.pri_key_file:
            f = open(args.pri_key_file, "r")
            const_private_key = f.read()
            f.close()
        else:
            print("No private key is provided. Use default key.\n")
        qrcode_generate()


main()