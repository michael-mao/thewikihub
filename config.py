import os
import jinja2
import re


DEBUG = False

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

HASH_KEY = 'supersecretkey1234!!!&$$$'

USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASS_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

POST_RE = r'(/(?:[a-zA-Z0-9_%+-]+/?)*)'

POSTS_LIMIT = 25