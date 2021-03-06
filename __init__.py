# Larger Applications
# http://flask.pocoo.org/docs/0.12/patterns/packages/


from flask import Flask

from flask_login import LoginManager, login_required

from .database import db_session
from .views.index_view import IndexView
from .views.users_view import RegisterView, ProfileView, LoginView, LogoutView
from .models.users_model import User


app = Flask(__name__)

# Configuration Handling
# http://flask.pocoo.org/docs/0.12/config/
app.config.from_object('taberu.config.DevelopmentConfig')
app.config.from_pyfile('settings.cfg')

# Flask-Login
# https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.init_app(app)


# Flask-Login
# https://flask-login.readthedocs.io/en/latest/
@login_manager.user_loader
def load_user(user_email):
    user = User.query.filter_by(email=user_email).first()
    return user


# SQLAlchemy
# http://flask-sqlalchemy.pocoo.org/2.3/
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Decorating Views
# http://flask.pocoo.org/docs/0.12/views/
logout_view = login_required(LogoutView.as_view(
    'logout_action', next_url='index_page'))
profile_view = login_required(ProfileView.as_view(
    'profile_page', template_name='users/profile.html'))

# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/
app.add_url_rule('/', view_func=IndexView.as_view(
    'index_page', template_name='index.html'))
app.add_url_rule('/register', view_func=RegisterView.as_view(
    'register_page', template_name='users/register.html'))
app.add_url_rule('/login', view_func=LoginView.as_view(
    'login_page', template_name='users/login.html'))
app.add_url_rule('/logout', view_func=logout_view)
app.add_url_rule('/profile', view_func=profile_view)


if __name__ == '__main__':
    app.run()
