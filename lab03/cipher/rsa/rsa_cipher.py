import rsa
import os

KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")


class RSACipher:
    def __init__(self):
        os.makedirs(KEYS_DIR, exist_ok=True)

    def generate_keys(self):
        """Generate RSA public/private key pair and save to files."""
        (public_key, private_key) = rsa.newkeys(2048)

        with open(os.path.join(KEYS_DIR, "publicKey.pem"), "wb") as f:
            f.write(public_key.save_pkcs1())

        with open(os.path.join(KEYS_DIR, "privateKey.pem"), "wb") as f:
            f.write(private_key.save_pkcs1())

    def load_keys(self):
        """Load RSA keys from PEM files."""
        with open(os.path.join(KEYS_DIR, "publicKey.pem"), "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open(os.path.join(KEYS_DIR, "privateKey.pem"), "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        return private_key, public_key

    def encrypt(self, message, key):
        """Encrypt a message using the given key."""
        message_bytes = message.encode("utf-8")
        encrypted = rsa.encrypt(message_bytes, key)
        return encrypted

    def decrypt(self, ciphertext, key):
        """Decrypt ciphertext using the given key."""
        decrypted = rsa.decrypt(ciphertext, key)
        return decrypted.decode("utf-8")

    def sign(self, message, private_key):
        """Sign a message using the private key."""
        message_bytes = message.encode("utf-8")
        signature = rsa.sign(message_bytes, private_key, "SHA-256")
        return signature

    def verify(self, message, signature, public_key):
        """Verify a signature using the public key."""
        try:
            message_bytes = message.encode("utf-8")
            rsa.verify(message_bytes, signature, public_key)
            return True
        except rsa.VerificationError:
            return False
