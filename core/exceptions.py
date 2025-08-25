class EncryptionError(Exception):
    """Raised when trying to encrypt encrypted text."""


class DecryptionError(Exception):
    """Raised when trying to decrypt decrypted text."""


class UnsupportedCipherError(Exception):
    """Raised when an unsupported cipher type used."""