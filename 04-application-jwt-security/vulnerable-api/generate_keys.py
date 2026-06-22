from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

BASE_DIR = Path(__file__).resolve().parent.parent
KEY_DIR = BASE_DIR / "keys"

KEY_DIR.mkdir(exist_ok=True)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

(KEY_DIR / "private.pem").write_bytes(private_pem)
(KEY_DIR / "public.pem").write_bytes(public_pem)

print("RSA key pair generated successfully.")