import hashlib
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class DecryptionError(Exception):
    """Raised when encrypted vault data cannot be authenticated/decrypted."""


class CryptoEngine:
    """Envelope encryption: a random DEK encrypts notes; a password wraps the DEK."""

    SCRYPT_N = 2 ** 15
    SCRYPT_R = 8
    SCRYPT_P = 1
    KEY_LENGTH = 32
    NONCE_LENGTH = 12
    SALT_LENGTH = 16

    @staticmethod
    def _derive_kek(secret: str, salt: bytes) -> bytes:
        if not isinstance(secret, str) or not secret:
            raise ValueError("A non-empty secret is required.")
        return hashlib.scrypt(
            secret.encode("utf-8"),
            salt=salt,
            n=CryptoEngine.SCRYPT_N,
            r=CryptoEngine.SCRYPT_R,
            p=CryptoEngine.SCRYPT_P,
            dklen=CryptoEngine.KEY_LENGTH,
            maxmem=64 * 1024 * 1024,
        )

    @staticmethod
    def generate_dek() -> bytes:
        return os.urandom(CryptoEngine.KEY_LENGTH)

    @staticmethod
    def generate_recovery_key() -> str:
        return os.urandom(32).hex().upper()

    @staticmethod
    def wrap_dek(dek: bytes, secret: str, salt: bytes) -> bytes:
        key = CryptoEngine._derive_kek(secret, salt)
        nonce = os.urandom(CryptoEngine.NONCE_LENGTH)
        return nonce + AESGCM(key).encrypt(nonce, dek, None)

    @staticmethod
    def unwrap_dek(wrapped_dek: bytes, secret: str, salt: bytes) -> bytes:
        try:
            key = CryptoEngine._derive_kek(secret, salt)
            nonce = wrapped_dek[:CryptoEngine.NONCE_LENGTH]
            ciphertext = wrapped_dek[CryptoEngine.NONCE_LENGTH:]
            return AESGCM(key).decrypt(nonce, ciphertext, None)
        except (InvalidTag, ValueError, TypeError, IndexError) as exc:
            raise DecryptionError("Invalid password/recovery key or damaged vault.") from exc

    @staticmethod
    def encrypt_note(dek: bytes, plaintext: str) -> bytes:
        nonce = os.urandom(CryptoEngine.NONCE_LENGTH)
        return nonce + AESGCM(dek).encrypt(nonce, plaintext.encode("utf-8"), None)

    @staticmethod
    def decrypt_note(dek: bytes, encrypted_data: bytes) -> str:
        try:
            nonce = encrypted_data[:CryptoEngine.NONCE_LENGTH]
            ciphertext = encrypted_data[CryptoEngine.NONCE_LENGTH:]
            return AESGCM(dek).decrypt(nonce, ciphertext, None).decode("utf-8")
        except (InvalidTag, ValueError, TypeError, UnicodeDecodeError) as exc:
            raise DecryptionError("Note data is corrupted or tampered with.") from exc
