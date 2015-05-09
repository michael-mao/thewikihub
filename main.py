import webapp2

from handlers import MainHandler, HomePage, RandomArticle, NewPostPage, EditPage, HistoryPage, PostPage
from auth import Signup, Login, Logout
from config import DEBUG, POST_RE, JINJA_ENV
# TODO: better homepage
# TODO: full text search
# TODO: pagination of articles
# TODO: user profiles


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/home', HomePage),
    ('/random_article', RandomArticle),
    ('/edit/newpost', NewPostPage),
    ('/edit' + POST_RE, EditPage),
    ('/history' + POST_RE, HistoryPage),
    (POST_RE, PostPage)
], debug=DEBUG)


def handle_404(request, response, exception):
    response.set_status(404)
    t = JINJA_ENV.get_template('404.html')
    response.out.write(t.render())


def handle_500(request, response, exception):
    response.set_status(500)
    t = JINJA_ENV.get_template('500.html')
    response.out.write(t.render())


app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500