import json
from api import starpay, qrtiger
from urllib.parse import urlencode, quote

def generate_qrcode(amount: float, merchant_id: str, merchant_name: str):
    response = starpay.generate_qr(amount, merchant_id, merchant_name).get('response')
    qr_code  = response.get('codeUrl')
    qr_image = qrtiger.generate_qrph(qr_code)

    return dict(
        merchant_name = response.get('displayName') or '',
        currency      = 'PHP',
        amount        = f'{amount:,.2f}',
        qr_code       = qr_image.get('url') or '',
        gcash_link    = generate_gcash_link(qr_code)
    )

def generate_gcash_link(qr: str):
    # Environment variables
    gcash_app_url = "gcash://com.mynt.gcash/app/006300000800"
    merchantId    = "217020000119199251998"
    clientId      = "2023062916065505394208"
    qrCodeFormat  = "EMVCO"
    sub           = "p2mpay"
    bizNo         = None
    lucky         = False

    # Decode QR
    qr_data = decode(qr)
    ppmi_data = qr_data.get('28') or {}
    provider_data = qr_data.get('62') or {}

    # Generate Params
    query = urlencode(dict(
        qrCode       = qr,
        merchantId   = merchantId,
        bizNo        = bizNo,
        orderAmount  = qr_data.get('54') or '',
        merchantName = qr_data.get('59') or '',
        shopId       = ppmi_data.get('03') or '',
        qrCodeFormat = qrCodeFormat,
        tfrbnkcode   = ppmi_data.get('01') or '',
        clientId     = clientId,
        param3       = "~".join((
            '99960005',
            ppmi_data.get('00') or '',
            '',
            '',
            ppmi_data.get('05') or ''
        )),
        param5 = "~".join((
            ppmi_data.get('03') or '',
            provider_data.get('03') or '',
            (provider_data.get('07') or '').strip(),
            '',
            provider_data.get('05') or ''
        )),
        tfrAcctNo = ppmi_data.get('03') or '',
        acqInfo   = provider_data.get('05') or '',
        sub       = sub,
        lucky     = json.dumps(lucky)
    ), quote_via=quote).replace('~', '%7E')

    # Build URL
    return f"{gcash_app_url}?{query}"

def decode(qr: str):
    data = dict()
    while qr:
        key       = qr[:4]
        qr        = qr[4:]
        length    = int(key[2:])
        data[key] = qr[:length]
        qr        = qr[length:]
        if key[:2] in ['28', '62', '88']:
            data[key] = decode(data[key])

    return {key[:2]: data[key] for key in data}
