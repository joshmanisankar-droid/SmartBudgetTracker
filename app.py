from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()
from extensions import db, migrate,bcrypt,login_manager,mail
app=Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    database_url = "sqlite:///price_tracker.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"

app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
db.init_app(app)
migrate.init_app(app,db)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from model import User, Product, WatchRequest, PriceHistory
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
with app.app_context():
    db.create_all()

#from services.scheduler import start_scheduler

# Start the scheduler once. On Render (gunicorn) WERKZEUG_RUN_MAIN is not set,
# so start the scheduler unless we're the Werkzeug parent process.
#if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#    start_scheduler(app)

from routes.auth import auth 
app.register_blueprint(auth)
from routes.product import product
app.register_blueprint(product)


if __name__=="__main__":
    app.run(debug=True)