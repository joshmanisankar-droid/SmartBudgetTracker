from flask import Blueprint,render_template,request,redirect,url_for,flash
from extensions import db,bcrypt
from model import User,WatchRequest
from flask_login import login_user,logout_user,login_required,current_user

auth=Blueprint("auth",__name__)
@auth.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email Already Exists")
            return redirect(url_for("auth.register"))
        
        hashed_password=bcrypt.generate_password_hash(password).decode("utf-8")
        user=User(
            name=name,
            email=email,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        user=User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash,password):
            login_user(user)
            flash("Login Successful")
            return redirect(url_for("auth.dashboard"))
        flash("Invalid Credentials")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out Successfully")
    return redirect(url_for("auth.login"))

@auth.route("/dashboard")
@login_required
def dashboard():
    watch_requests = WatchRequest.query.filter_by(
        user_id=current_user.id
    ).all()
    return render_template(
        "dashboard.html",
        user=current_user,
        watch_requests=watch_requests
    )