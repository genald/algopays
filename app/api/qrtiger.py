import requests

def generate_qr(text: str, customization = {}) -> dict:
    return requests.post(
        url = 'https://qrtiger.com/api/qr/static',
        headers = {
            'Authorization' : 'Bearer 148005b0-b609-11ef-ad83-6b848c55110f',
            'Content-Type'  : 'application/json',
            'Accept'        : 'application/json',
        },
        json = dict(
            size            = 710,
            colorDark       = 'rgb(0,0,0)',
            logo            = 'https://s3-staging-justpayto-web-assets.s3.ap-southeast-1.amazonaws.com/img/icons/QRPH.jpg',
            eye_outer       = 'eyeOuter0',
            eye_inner       = 'eyeInner0',
            qrData          = 'pattern3',
            backgroundColor = 'rgb(255,255,255)',
            transparentBkg  = False,
            qrCategory      = 'text',
            text            = text,
        ),
    ).json()

def generate_qrph(code: str):
    return generate_qr(code)
