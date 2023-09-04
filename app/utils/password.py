import hashlib


def encrypt_password(plain_password_text: str) -> str:
    # Convert the plain text password to bytes
    password_bytes = plain_password_text.encode('utf-8')

    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the password bytes
    md5_hash.update(password_bytes)

    # Get the hexadecimal representation of the hash
    hashed_password = md5_hash.hexdigest()

    return hashed_password
