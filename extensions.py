from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view="auth.login"
from flask_mail import Mail
mail = Mail()