import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")


class ECCCipher:
    def __init__(self):
        os.makedirs(KEYS_DIR, exist_ok=True)

    def generate_keys(self):
        """Generate ECC public/private key pair and save to files."""
        sk = ec.generate_private_key(ec.SECP256K1())
        vk = sk.public_key()

        with open(os.path.join(KEYS_DIR, "privateKey.pem"), "wb") as p:
            p.write(sk.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(os.path.join(KEYS_DIR, "publicKey.pem"), "wb") as p:
            p.write(vk.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_keys(self):
        """Load ECC keys from PEM files."""
        with open(os.path.join(KEYS_DIR, "privateKey.pem"), "rb") as p:
            sk = serialization.load_pem_private_key(p.read(), password=None)

        with open(os.path.join(KEYS_DIR, "publicKey.pem"), "rb") as p:
            vk = serialization.load_pem_public_key(p.read())

        return sk, vk

    def sign(self, message, key):
        """Sign a message using the private key."""
        return key.sign(message.encode("utf-8"), ec.ECDSA(hashes.SHA256()))

    def verify(self, message, signature, key):
        """Verify a signature using the public key."""
        _, vk = self.load_keys()
        try:
            vk.verify(signature, message.encode("utf-8"), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
