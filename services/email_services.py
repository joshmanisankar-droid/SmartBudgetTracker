from flask_mail import Message
from flask import current_app
from extensions  import mail

def send_price_alert(user, product):
    print(f"Preparing email for {user.email}")

    msg = Message(
        subject="Price Drop Alert",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email]
    )

    msg.body = f"""
Hello {user.name},

Good News!

{product.title}

Current Price: ₹{product.current_price}

The product has reached your target price.

Happy Shopping!
"""

    print("Sending email...")
    mail.send(msg)
    print("Email sent!")