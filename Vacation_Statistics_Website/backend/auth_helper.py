"""
Helper module for Django password verification in Flask.
Django uses PBKDF2 algorithm for password hashing.
"""
import hashlib
import base64


def verify_django_password(password: str, encoded: str) -> bool:
    """
    Verify a password against Django's PBKDF2 hash.

    Django password format: 
    pbkdf2_sha256$iterations$salt$hash

    Args:
        password: Plain text password to verify
        encoded: Django's encoded password hash

    Returns:
        bool: True if password matches, False otherwise
    """
    if not encoded:
        return False

    try:
        algorithm, iterations, salt, hash_value = encoded.split('$')

        if algorithm != 'pbkdf2_sha256':
            return False

        # Generate hash with same parameters
        dk = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            int(iterations)
        )

        # Encode to base64 to match Django's format
        encoded_hash = base64.b64encode(dk).decode('ascii').strip()

        return encoded_hash == hash_value

    except (ValueError, AttributeError):
        return False


def list_admin_users(conn):
    """
    List all admin users in the database for debugging purposes.
    """
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, first_name, last_name, is_staff, is_superuser, is_active, date_joined
        FROM accounts_user 
        WHERE is_staff = true 
        ORDER BY date_joined
    """)

    admin_users = cur.fetchall()
    cur.close()

    if admin_users:
        print("Found admin users:")
        for user in admin_users:
            print(
                f"  ID: {user['id']}, Email: {user['email']}, Name: {user['first_name']} {user['last_name']}, Active: {user['is_active']}")
    else:
        print("No admin users found in database")

    return admin_users
