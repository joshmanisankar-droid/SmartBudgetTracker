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
            data=scrape_product(product.url)
            product.current_price=data["price"]
            product.last_checked = datetime.utcnow()
            history=PriceHistory(
                product_id=product.id,
                price=data["price"]
            )
            db.session.add(history)
            
            for watch in product.watch_requests:
                if (
                    product.current_price <= watch.target_price
                    and not watch.notification_sent
                ):
                    send_price_alert(watch.user,product)
                    watch.notification_sent=True
                    print(watch.notification_sent)
            db.session.commit()
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