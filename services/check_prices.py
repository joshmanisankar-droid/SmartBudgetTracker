from app import app
from services.scheduler import check_prices

print("Starting scheduled price check...")

with app.app_context():
    check_prices(app)

print("Finished scheduled price check.")