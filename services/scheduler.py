from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from model import Product,PriceHistory
from services.scraper import scrape_product
from services.email_services import send_price_alert
from extensions import db
scheduler = BackgroundScheduler()
def check_prices(app):
    with app.app_context():
        products=Product.query.all()
        print(f"Checking {len(products)} products at {datetime.utcnow()}")
        for product in products:
            try:
                print(f"Checking product: {product.title}")
                data = scrape_product(product.url)
            except Exception as e:
                print(f"Skipping '{product.title}': {e}")
                continue
            product.current_price = data["price"]
            product.last_checked = datetime.utcnow()
            history = PriceHistory(
                product_id=product.id,
                price=data["price"]
            )
            db.session.add(history)

            for watch in product.watch_requests:
                if (
                    product.current_price <= watch.target_price
                    and not watch.notification_sent
                ):
                    print(f"Price reached for {product.title}")
                    print(f"Current: {product.current_price} | Target: {watch.target_price}")
                    print(f"Sending email to {watch.user.email}")
                    send_price_alert(watch.user, product)
                    watch.notification_sent = True
                    print("Email sent successfully.")
            db.session.commit()
            print(f"Finished checking {product.title}")
def start_scheduler(app):
    if scheduler.running:
        return
    print("Starting APScheduler...")
    scheduler.add_job(
        check_prices,
        "interval",
        seconds=10,
        args=[app]
    )
    scheduler.start()
    print("APScheduler started.")