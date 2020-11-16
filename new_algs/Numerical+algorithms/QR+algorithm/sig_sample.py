if __name__ == '__main__':
    private_key = '''-----BEGIN PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAyQDti8YVmfrAIm6Pm3XN3MZWRH0XiIVqRC6nmdd0twDayZ3epsHbB/RBOM7QOxYRDBqUv8F9vlrBdWYnyey6iQIDAQABAkA2JGbYEIo/CLj6TVenY2sJPe980Ukmf/Fo3jxNByksJbdjFJx6a3iyP8G3GSjj5wKdO/yG4+xEfQvw+rr103rVAiEA7/keSShXBmeUApLJN8CZh22ntFAsVPF0n0tIoovlJqMCIQDWbYnI/TxzwjO5ietRjKEwyr4z0qq07NeCaZgptqYo4wIgMrp42oI6k1IGCd05yB1g1y4pC4b/OB2qx5nEiwgDsv0CIQCQYx4eqvbj8+ckjoxYU1vPIRZGixrLzZeohzYhEI5+hQIhAM52I8kzZHhNbEoWftdIHbIKa5PXmJ+mqgrSoOupo3yn
-----END PRIVATE KEY-----
'''

    public_key = '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMkA7YvGFZn6wCJuj5t1zdzGVkR9F4iFakQup5nXdLcA2smd3qbB2wf0QTjO0DsWEQwalL/Bfb5awXVmJ8nsuokCAwEAAQ==
-----END PUBLIC KEY-----
'''

message = 'chengxuyuanzhilu rsa'
signature = rsa_sign(message.encode(encoding='utf-8'), private_key)
result = rsa_verify(signature, message.encode('utf-8'), public_key)
print(result)
print("signature = " + signature.hex())
print()