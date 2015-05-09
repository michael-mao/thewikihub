import hashlib
import hmac
import random
from string import letters
from google.appengine.ext import db
from config import HASH_KEY, USER_RE, PASS_RE, EMAIL_RE


def wiki_key(name='default'):
    return db.Key.from_path('wiki', name)


def users_key(name='default'):
    return db.Key.from_path('users', name)


def create_hash_value(value):
    return '%s|%s' % (value, hmac.new(HASH_KEY, value).hexdigest())


def check_hash_value(hash_value):
    value = hash_value.split('|')[0]
    if hash_value == create_hash_value(value):
        return value


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_password_hash(username, password, salt=None):
    if not salt:
        salt = make_salt()
    password_hash = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (salt, password_hash)


def check_password(username, password, password_hash):
    salt = password_hash.split(',')[0]
    return password_hash == make_password_hash(username, password, salt)


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


def gray_style(lst):
    for n, x in enumerate(lst):
        if n % 2 == 0:
            yield x, ''
        else:
            yield x, 'gray'


def escape_space(string):
    string.replace(' ', '%20')
    return string