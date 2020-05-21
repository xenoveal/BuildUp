import hashlib, binascii, os
from functools import wraps
from flask import redirect, url_for, session
from itsdangerous import URLSafeTimedSerializer


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'data' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def login_notrequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('data' not in session):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index_login'))
    return wrap

def generate_confirmation_token(email, app):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, app, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

