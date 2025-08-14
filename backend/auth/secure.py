from passlib.context import CryptContext


class Hasher:
    """Utility class for password hashing and verification."""

    _crypt_context: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @classmethod
    def hash_password(cls: type["Hasher"], unhashed_password: str) -> str:
        """Return a hash of password.

        :param unhashed_password: A password to hash
        :return: hashed password
        """
        return cls._crypt_context.hash(unhashed_password)

    @classmethod
    def verify_password(
        cls: type["Hasher"],
        unhashed_password: str,
        hashed_password: str,
    ) -> bool:
        """Check if raw password equal to hashed password.

        :param unhashed_password: Raw password
        :param hashed_password: Hashed password
        :return: True if hashed password identical to raw, false otherwise
        """
        return cls._crypt_context.verify(unhashed_password, hashed_password)
