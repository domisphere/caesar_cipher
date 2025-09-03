class UnsupportedCipherError(Exception):
    """Raised when an unsupported cipher type used."""


class EmptyBufferError(Exception):
    """Raised when empty buffer"""


class RotTypeMismatchError(Exception):
    """Raised when mismatch rot type"""