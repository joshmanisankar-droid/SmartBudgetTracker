from flask_mail import Message
from extensions  import mail

def send_price_alert(user,product):
    msg=Message(
        subject="Price Drop Alert",
        recipients=[user.email]
    )
    msg.body = f"""
                Hello {user.name},
                Good News!
                {product.title}
                Current Price : {product.current_price}
                The product has reached your target price.
                Happy Shopping!
                """
    mail.send(msg)