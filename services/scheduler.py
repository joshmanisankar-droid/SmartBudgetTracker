from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from model import Product,PriceHistory
from services.scraper import scrape_product
from services.email_services import send_price_alert
from extensions import db
import traceback
scheduler = BackgroundScheduler()
def check_prices(app):
    with app.app_context():
        print(f"=== Scheduler started at {datetime.utcnow()} ===")
        try:
            products = Product.query.all()
            print(f"Found {len(products)} products")

            for product in products:
                print(f"Checking: {product.title}")
                try:
                    print("Calling send_price_alert()...")
                    send_price_alert(watch.user, product)
                    print("mail.send() returned successfully")

                    watch.notification_sent = True
                    db.session.commit()

                    print("notification_sent updated")
                except Exception as e:
                    print("EMAIL ERROR:", e)
                    traceback.print_exc()
                    db.session.rollback()

                product.current_price = data["price"]
                product.last_checked = datetime.utcnow()

                db.session.add(
                    PriceHistory(
                        product_id=product.id,
                        price=data["price"]
                    )
                )

                for watch in product.watch_requests:
                    print(f"Current={product.current_price}, Target={watch.target_price}, Sent={watch.notification_sent}")
                    if product.current_price <= watch.target_price and not watch.notification_sent:
                        print(f"Sending alert to {watch.user.email}")
                        try:
                            send_price_alert(watch.user, product)
                            watch.notification_sent = True
                            print("Alert sent successfully")
                        except Exception:
                            traceback.print_exc()
                            db.session.rollback()

                db.session.commit()
                db.session.remove()
                print(f"Finished {product.title}")

        except Exception:
            traceback.print_exc()
            db.session.rollback()
        finally:
            db.session.remove()
            print("=== Scheduler finished ===")
def start_scheduler(app):
    if scheduler.running:
        return
    print("Starting APScheduler...")
    scheduler.add_job(
        check_prices,
        trigger="interval",
        minutes=2,
        args=[app],
        id="price_checker",
        max_instances=1,
        coalesce=True,
        misfire_grace_time=30,
        replace_existing=True,
    )
    scheduler.start()
    print("APScheduler started.")