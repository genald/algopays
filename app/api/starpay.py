import requests
from time import time
from security import sha256_rsa_signed

private_key_pem = (
'''-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA5H+MSTOGzlTfaaNilj7RPNUCP92A4z34FBd7vsnlpJw1PJNi
2C2b9xdcXzILS5FygoEMPfrxFxPWH/2SUHoQViLpF6KLFqDDPdXSzmWzLiKGZqrh
LYLXnpN6L9jqZx6cpZ86kNLNr2+xO9QQlSe+pJRMO7ungxHqhn/07SLOsoPWEJhO
MRlwi+y8XBK1mX5eRWXYP7dfe+L6jigrLZtNn0ffllhfdzfmb/9HCDYpWNEtnM/2
jfJPC0BfpIh2cbTw9JSQ0yxK/AIudaPhlnZ9sQwtUBK5LfkkzM92PluRVIqoW0Sg
HG1YGVQOzpCDrCCDyNwkLsHWsz5BvLI6tLTIVwIDAQABAoIBABMN08vy4QXpq+uq
NTlkKZySAqsCtJG+hCZgwu/o9B5i7EmN3Ms8GmpjZ0+E4848ZbkeO8AbYelTvSJT
ydSuKRiVtqxC4KhVZZKNdxPBBU0OkfiTvU1HQOW3VJQS2ZEZy2RAP+j9uysq/DOJ
/owBkXM17pl4j4JthwoKN4liwqu+DEe8zuj6GEcDSJbngSQCz2IVKitJ6Ovq3sL6
gI1ql6Dep2Ie1/2Dqqp0T75GYwOUB9ftM/Q1KBU6y+HYSwG8CKNcwIjFte/LjJ+W
XPdoA/ARVf5A6o+AJLIrElBzazk/OXP26GnDL1LJqzswqpQjFAy5AeiPMc1CHNdl
HK9xV9kCgYEA6BfaB73uWx/x+ojqcJKo1n8JNw46Laj/bGUMeSwgdffHMwbGYIAp
ywWqxPtmQy8/1K3s7FxT3Z0nhORMtPrR9TH1VkYLFGKv1+CpVDFRfy5REuBhjgD5
0WkxbqgWvEk5JcZrATEIlVrWyvPMXU1R2XWSfZM93+OcrN7ovUi/te0CgYEA/Ajm
b8akrXiN3VAtp4+2mFzMMv787Vi7DPkgxsLj3REHJmlV1/l1z23wKO0XylbFCvzM
F5Jke+epaJAp6k+JQrWsxXb2FYDwsleRRNhhZ/+aW1V2w3HTDKQJv0htafm7KAYl
0UqxNJNAygVmDVF5Esu4RAWofDNFe4AOKKfebtMCgYEAq9Q8z06GkWBtPhbvurhZ
17PllqUp3XQo5o9JVMyem7f9+oEhjYBVcMGZVIzrgQISN9ssdTFFxeT7xR9gyvyH
RQjfoifpPAZ0OVdTBcodlBMuYtNMZl3Clo9S0aIQcwWjEZx8zD0JJcpDC67Dtq/v
0ReChQXl4UQaUsIVfU3G4WECgYEA03CQCjQHUbTypzmto4ZwtHAdq6a6AFDRU/fp
JHa5/WtcqT/zkaYpzOS5d0w5CjozQp2Ehz38aOqX+C4BzB3/1GRf1qWPm8i5pZTL
PYueZEZOc9NGOH9UhKVVvBECIcct2U0XCvdzpNzonNNco023miooo4Bvsgq9fveW
aUsz05sCgYEApeqBD2ijhDAqEgkafwOBLCBAUcJQ6d81l2Cv3AnlF0TZpMiHdF+P
5TLBe9vfwceppV0PMVS6v262l3ujmac7aSfBUSdoXVuUPEn56M6K4+QBEYT7oowt
XtLBp3wW/NN2OjzQ7ofDE2RBO7wZqOFT/ajz38iXtCM37jn3xwYws8I=
-----END RSA PRIVATE KEY-----''')

def generate_reference_id(deviceInfo: str):
    timestamp = int(time())
    return f"{deviceInfo}{timestamp}"

def generate_qr(amount: float, merchant_id: str, merchant_name: str) -> dict:
    # Environment Variables
    url          = 'https://financeapi.wepayez.com/finance-payment-service/v1/repayment'
    webhook      = 'https://webhook-test.com/5d3bfa75ac08baba3ee61ad895863d9e'
    currency     = 'PHP'
    service      = 'pay.starpay.repayment'
    deviceInfo   = 'ALGPYMT'

    # Starpay Payload
    request = dict(
        msgId       = generate_reference_id(deviceInfo),
        mchId       = merchant_id,
        notifyUrl   = webhook,
        deviceInfo  = deviceInfo,
        trxAmount   = int(amount*100),
        displayName = merchant_name,
        currency    = currency,
        service     = service
    )

    return requests.post(
        url = url,
        json = dict(
            request   = request,
            signature = sha256_rsa_signed(request, private_key_pem)
        )
    ).json()
