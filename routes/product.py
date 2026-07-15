from flask import Blueprint,render_template,request,redirect,url_for,flash
from extensions import db,bcrypt
from model import User,Product,WatchRequest
from flask_login import login_user,logout_user,login_required,current_user
from services.scraper import scrape_product

product=Blueprint("product",__name__)

@product.route("/add-product",methods=["POST","GET"])
@login_required
def add_product():
    if request.method=="POST":
        url=request.form["url"]
        target_price=float(request.form["target_price"])
        product = Product.query.filter_by(url=url).first()
        if not product:
            data=scrape_product(url)
            product = Product(
                title=data["title"],
                url=url,
                website="BookToScrape",
                current_price=data["price"],
                image_url=data["image"]
            )
            
            db.session.add(product)
            db.session.commit()
        existing_watch=WatchRequest.query.filter_by(
            user_id=current_user.id,
            product_id=product.id
        ).first()
        if existing_watch:
            flash("You are already tracking this product.")
            return redirect(url_for("product.add_product"))
        watch = WatchRequest(
            user_id=current_user.id,
            product_id=product.id,
            target_price=target_price
        )
        db.session.add(watch)
        db.session.commit()

        flash("Product Added Successfully")
        return redirect(url_for("auth.dashboard"))
    return render_template("add_product.html")

@product.route("/delete-watch/<int:watch_id>",methods=["POST"])
@login_required
def delete_watch(watch_id):
    watch=WatchRequest.query.get_or_404(watch_id)
    if watch.user_id!=current_user.id:
        flash("Unauthorized")
        return redirect(url_for("auth.dashboard"))
    db.session.delete(watch)
    db.session.commit()
    flash("Tracking Removed Successfully")
    return redirect(url_for("auth.dashboard"))
@product.route("/edit-watch/<int:watch_id>", methods=["GET", "POST"])
@login_required
def edit_watch(watch_id):
    watch = WatchRequest.query.get_or_404(watch_id)
    if watch.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        watch.target_price = float(request.form["target_price"])
        watch.notification_sent = False
        db.session.commit()
        flash("Target Price Updated Successfully")
        return redirect(url_for("auth.dashboard"))
    return render_template(
        "edit_watch.html",
        watch=watch
    )