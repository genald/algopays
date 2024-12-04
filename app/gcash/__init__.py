import os, base64
from io import BytesIO
from urllib.parse import urlencode
from api import infinipay
from utils import decode_qr

def generate_qrcode(amount: float):
    qr_code = infinipay.generate_qr(amount).get('qr')
    qr = decode_qr(BytesIO(base64.b64decode(qr_code)))

    data = dict(
        qrCode       = qr,
        merchantId   = os.getenv('INFINITI_PAY_GCASH_MERCHANT_ID'),
        orderAmount  = amount,
        merchantName = os.getenv('INFINITI_PAY_MERCHANT_NAME'),
        clientId     = os.getenv('INFINITI_PAY_GCASH_CLIENT_ID'),
        sub          = 'p2mpay'
    )

    deep_link  = os.getenv('GCASH_PAYMENT_DEEP_LINK')
    deep_link += "?" + urlencode(data)

    return dict(
        merchant_name = data['merchantName'],
        currency      = 'PHP',
        amount        = f'{amount:,.2f}',
        qr_code       = qr_code,
        gcash_link    = deep_link
    )
