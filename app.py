from flask import Flask
from extensions import db, migrate,bcrypt,login_manager,mail
app=Flask(__name__)
app.config["SECRET_KEY"] = "josh_secret_key_2026"  
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///price_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "joshmanisankar@gmail.com"
app.config["MAIL_PASSWORD"] = "jyse jbkq jroz elkp"
app.config["MAIL_DEFAULT_SENDER"] = "joshmanisankar@gmail.com"
db.init_app(app)
migrate.init_app(app,db)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from model import User, Product, WatchRequest, PriceHistory
@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
with app.app_context():
    db.create_all()
from services.scheduler import start_scheduler
import os
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    start_scheduler(app)

from routes.auth import auth 
app.register_blueprint(auth)
from routes.product import product
app.register_blueprint(product)


if __name__=="__main__":
    app.run(debug=True)