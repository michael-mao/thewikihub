from google.appengine.ext import db
from utils import users_key, make_password_hash, check_password
from config import JINJA_ENV


class Post(db.Model):
    author = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    version = db.IntegerProperty(required=True, default=1)
    date_created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @staticmethod
    def parent_key(path):
        return db.Key.from_path('/root' + path, 'posts')

    @classmethod
    def find_by_path(cls, path):
        q = cls.all()
        q.ancestor(cls.parent_key(path))
        q.order('-date_created')
        return q

    @classmethod
    def find_by_id(cls, post_id, path):
        return cls.get_by_id(post_id, cls.parent_key(path))

    def render(self):
        self.render_text = self.content.replace('/n', '<br>')
        t = JINJA_ENV.get_template('post_format.html')
        return t.render(post=self)


class User(db.Model):
    username = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def find_by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def find_by_name(cls, username):
        user = User.all().filter('username =', username).get()
        return user

    @classmethod
    def register(cls, username, password, email=None):
        password_hash = make_password_hash(username, password)
        return User(parent=users_key(),
                    username=username,
                    password_hash=password_hash,
                    email=email)

    @classmethod
    def login(cls, username, password):
        user = cls.find_by_name(username)
        if user and check_password(username, password, user.password_hash):
            return user