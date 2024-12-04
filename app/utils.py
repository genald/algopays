import uuid
import hashlib
import jinja2
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image

def generate_reference_id(prefix = "AGP"):
    timestamp     = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = uuid.uuid4().hex[:6].upper()

    return f"{prefix}{timestamp}{random_suffix}"

def encrypt_sha256(input_string: str):
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()
    # Encode the input string and update the hash object
    sha256.update(input_string.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    return sha256.hexdigest()

def decode_qr(image_file):
    # Load the QR code image
    image = Image.open(image_file)

    # Decode the QR code
    decoded_data = decode(image)
    return decoded_data[0].data.decode()

def generate_html(file, data, path = ""):
    templateLoader = jinja2.FileSystemLoader(searchpath=path)
    templateEnv    = jinja2.Environment(loader=templateLoader)
    template       = templateEnv.get_template(file)
    return template.render(data=data)
