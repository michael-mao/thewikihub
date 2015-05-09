import webapp2
from models import User, Post
from config import JINJA_ENV, POSTS_LIMIT
from utils import *


class RequestHandler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        params['gray_style'] = gray_style
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, name, value):
        cookie_value = create_hash_value(value)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_value))

    def read_cookie(self, name):
        cookie_value = self.request.cookies.get(name)
        return cookie_value and check_hash_value(cookie_value)

    def login(self, user):
        self.set_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_cookie('user_id')
        self.user = uid and User.find_by_id(int(uid))
 

class MainHandler(RequestHandler):
    
    def get(self):
        self.redirect('/home')


class HomePage(RequestHandler):
    
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post WHERE version = 1 ORDER BY date_created DESC LIMIT " + str(POSTS_LIMIT))
        self.render("home.html", top_posts=posts)


class RandomArticle(RequestHandler):
    
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post")
        count = posts.count()
        i = random.randrange(0, count-1)
        post = posts[i]
        path = '/' + post.title.replace(" ", "_")
        self.render("post_page.html", post=post, path=path)

        
class EditPage(RequestHandler):
    
    def get(self, path):
        if not self.user:
            self.redirect('/login')

        post_id = self.request.get('id')
        if post_id and post_id.isdigit():
            post = Post.find_by_id(post_id=int(post_id), path=path)
            if not post:
                self.abort(404)
        else:
            post = Post.find_by_path(path=path).get()

        self.render("edit_post.html", path=path, post=post)

    def post(self, path):
        if not self.user:
            self.error(403)
            return

        author = self.user.username
        title = self.request.get('post_title')
        content = self.request.get('post_content')
            
        # look for old version first
        old_post = Post.find_by_path(path).get()     
        if old_post:
            old_post.version = 0
            old_post.put()

        if not (old_post or content or title):
            return
        # TODO: problem with versioning if title is changed
        elif not old_post or old_post.content != content or old_post.title != title:
            post = Post(parent=Post.parent_key(path), author=author, title=title, content=content)
            post.put()
    
        self.redirect(path)
        
##        if title and content:
##            post = Post(parent=wiki_key(), title=title, content=content)
##            post.put()
##            postID = str(post.key().id())
##            self.redirect('/%s' % postID)
##        else:
##            error_edit = "Please enter a title and content"
##            self.render("edit_post.html", title=title, content=content, error_edit=error_edit)


class HistoryPage(RequestHandler):

    def get(self, path):
        title = path.strip('/').replace('_', ' ')
        posts = db.GqlQuery("SELECT * FROM Post WHERE title = :1 ORDER BY date_created DESC", title)

        if posts:
            self.render("history_page.html", posts=posts, path=path)

        else:
            self.abort(404)

      
class PostPage(RequestHandler):
    
    def get(self, path):
        post_id = self.request.get('id')
        if post_id and post_id.isdigit():
            post = Post.find_by_id(post_id=int(post_id), path=path)
            if not post:
                self.abort(404)
        else:
            post = Post.find_by_path(path=path).get()

        if post:
            self.render("post_page.html", post=post, path=path)
        else:
            self.abort(404)


class NewPostPage(RequestHandler):
    
    def get(self):
        if not self.user:
            self.redirect('/login')
        
        self.render("edit_post.html", path=None, post=None)

    def post(self):
        if not self.user:
            self.error(403)
            return

        author = self.user.username
        title = self.request.get('post_title')
        content = self.request.get('post_content')
        path = '/' + title.replace(" ", "_")

        if not title or not content or title == '' or content == '':
            error_edit = "Please enter a title and content"
            self.render("edit_post.html", path=None, post=None, error_edit=error_edit)
        else:
            post = Post(parent=Post.parent_key(path), author=author, title=title, content=content)
            post.put()
            self.redirect(path)