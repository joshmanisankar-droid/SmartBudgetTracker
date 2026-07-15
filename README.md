# 💰 Smart Budget Tracker

A Flask-based web application that helps users monitor product prices and receive email notifications when products reach their desired target price.

---

## 🚀 Features

- 🔐 User Authentication (Register/Login/Logout)
- 📦 Track products using a product URL
- 💲 Set a custom target price
- 🔄 Automatic price monitoring using APScheduler
- 📧 Email notifications when target price is reached
- 📝 Edit target price anytime
- 🗑 Delete tracked products
- 📊 Dashboard showing all tracked products
- 🟢 Live status indicators
    - Watching
    - Target Reached
    - Alert Sent
- 🖼 Product image, title and current price display
- ☁️ Deployable on Render
- 🐘 PostgreSQL support (Production)
- 🗄 SQLite support (Development)

---

## 🛠 Tech Stack

### Backend

- Flask
- Flask SQLAlchemy
- Flask Login
- Flask Mail
- Flask Bcrypt
- APScheduler

### Database

- SQLite (Development)
- PostgreSQL (Production)

### Frontend

- HTML
- CSS
- Jinja2

### Web Scraping

- Requests
- BeautifulSoup4
- lxml

### Deployment

- Render
- Gunicorn

---

## 📂 Project Structure

```
SmartBudgetTracker/
│
├── app.py
├── model.py
├── extensions.py
├── requirements.txt
├── Procfile
├── .env
│
├── routes/
│   ├── auth.py
│   └── product.py
│
├── services/
│   ├── scraper.py
│   ├── scheduler.py
│   └── email_services.py
│
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── add_product.html
│   └── edit_watch.html
│
├── static/
│   ├── css/
│   └── images/
│
└── instance/
    └── price_tracker.db
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/joshmanisankar-droid/SmartBudgetTracker.git
```

Move into the project

```bash
cd SmartBudgetTracker
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

DATABASE_URL=sqlite:///instance/price_tracker.db
```

For production (Render)

```env
DATABASE_URL=<your_render_postgresql_database_url>
```

---

## ▶️ Run Locally

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## 📸 Workflow

1. Register an account
2. Login
3. Add a product URL
4. Set your target price
5. Scheduler checks prices automatically
6. Receive email when target price is reached

---

## 📬 Email Alerts

When the current price becomes lower than or equal to the target price, an email notification is automatically sent to the user.

---

## 📈 Future Improvements

- Amazon support
- Flipkart support
- eBay support
- CamelCamelCamel API integration
- Price history graphs
- Wishlist categories
- Multiple currency support
- Telegram notifications
- SMS notifications
- Chrome Extension
- Mobile App

---

## 👨‍💻 Author

**Josh Mani Sankar**

Mechanical Engineering Undergraduate  
National Institute of Technology Warangal

GitHub

https://github.com/joshmanisankar-droid

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
