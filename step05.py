import requests
import random
import string

URL = "http://183.175.14.145:8006/step_05"

USERNAME = "0221915012"
PASSWORD = "999732KH"

e = 65537
n = 135261828916791946705313569652794581721330948863485438876915508683244111694485850733278569559191167660149469895899348939039437830613284874764820878002628686548956779897196112828969255650312573935871059275664474562666268163936821302832645284397530568872432109324825205567091066297960733513602409443790146687029

def str2num(text):
    value = 0
    for b in text.encode("ascii"):
        value = value * 256 + b
    return value


def num2str(num):
    if num == 0:
        return ""

    data = []

    while num > 0:
        data.append(num & 0xff)
        num >>= 8

    data.reverse()

    return bytes(data).decode(errors="ignore")


def encrypt_number(number):
    return pow(number, e, n)


def encrypt_string(text):
    return encrypt_number(str2num(text))


def submit(params):
    r = requests.get(URL, params=params)
    print("\nRequest:", params)
    print("Response:", r.text)
    return r.json()

print("===== Verification 1 =====")

submit({
    "num": encrypt_number(31415926)
})

print("\n===== Verification 2 =====")

submit({
    "str2num": str2num("hello, world!")
})

print("\n===== Verification 3 =====")

hello_cipher = encrypt_string("hello, world!")

submit({
    "str": hello_cipher
})

print("\n===== Verification 4 =====")

submit({
    "hex": hex(hello_cipher)[2:]
})

print("\n===== LOGIN =====")

cipher = encrypt_string(PASSWORD)

response = submit({
    "user": USERNAME,
    "password": hex(cipher)[2:]
})

if response.get("is_success"):

    print("\nLogin Successful!")

    encrypted_message = int(response["message"], 16)

    decoded_number = pow(encrypted_message, e, n)

    print("\nDecoded integer:")
    print(decoded_number)

    print("\nDecoded text:")
    print(num2str(decoded_number))

else:
    print("\nLogin failed.")