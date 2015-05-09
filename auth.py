from handlers import RequestHandler
from models import User
from utils import valid_username, valid_password, valid_email


class Signup(RequestHandler):

    def get(self):
        if not self.user:
            self.render('signup_page.html')
        else:
            self.redirect('/home')

    def post(self):
        error_input = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username, email=email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username"
            error_input = True
            
        if not valid_password(password):
            params['error_password'] = "That's not a valid password"
            error_input = True

        elif password != verify:
            params['error_verify'] = "Your passwords do not match"
            error_input = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email"
            error_input = True

        if error_input:
            self.render('signup_page.html', **params)
        else:
            user = User.find_by_name(username)
            
            if user:
                params['error_username'] = "That username already exists"
                self.render('signup_page.html', **params)
            else:
                user = User.register(username, password, email)
                user.put()

                self.login(user)
                self.redirect('/home')


class Login(RequestHandler):

    def get(self):
        if not self.user:
            self.render('login_page.html')
        else:
            self.redirect('/home')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            self.login(user)
            self.redirect('/home')
        else:
            error_login = 'Invalid username and password'
            self.render('login_page.html', error_login=error_login)


class Logout(RequestHandler):

    def get(self):
        self.logout()
        self.redirect('/home')