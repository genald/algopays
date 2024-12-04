import os, requests
from utils import generate_reference_id, encrypt_sha256

def generate_qr(
    amount     : float,
    svcType    : str = 'GCASHQR',
    currency   : str = 'PHP',
    callbackUrl: str = 'https://algopays.com/webhooks/da5'
) -> dict:
    auth_id  = os.getenv('INFINITI_PAY_MERCHANT_ID') or ''
    secret   = os.getenv('INFINITI_PAY_API_KEY') or ''
    base_url = os.getenv('INFINITI_PAY_BASE_URL') or ''

    refId = generate_reference_id()

    response = requests.post(
        url = f"{base_url}/api/txn/deposit",
        headers = dict(
            AUTHZID    = auth_id,
            AUTHZTOKEN = encrypt_sha256(f'{svcType}{currency}{refId}{secret}'),
        ),
        data = dict(
            svcType     = svcType,
            amount      = amount,
            currency    = currency,
            refId       = refId,
            callbackUrl = callbackUrl,
        )
    )

    try:
        data: dict = response.json()
    except Exception as e:
        raise e

    url   = data.get('redirect') or ''
    paths = url.split('/')
    tid   = paths[-1]
    url   = '/'.join(paths[:3])

    return dict(url = data.get('redirect')) | requests.get(f'{url}/pub/{svcType.lower()}/{tid}').json()
