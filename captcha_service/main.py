import base64

from pika import BasicProperties
import random
import string
from initializing_connections import broker_obj
from models.exeption_handler import exception_handler
from captcha.image import ImageCaptcha


def generate_captcha_text():
    # Generate a random CAPTCHA text with a combination of letters and numbers
    captcha_length = 6
    captcha_characters = (string.ascii_letters + string.digits).lower()
    captcha = ''.join(random.choice(captcha_characters) for _ in range(captcha_length))
    return captcha


# Function with incoming message processing logic
@exception_handler
def callback(_ch, _method, properties: BasicProperties, _body):
    # Generate CAPTCHA key and image
    captcha_text = generate_captcha_text()
    captcha_image = ImageCaptcha(width=280, height=90)

    # Encode image to base64 for transferring via message broker
    captcha = base64.b64encode(captcha_image.generate(captcha_text).getvalue()).decode('utf-8')
    captcha_string = f"data:image/png;base64,{captcha}"
    broker_obj.send(data={"key": captcha_text, "image": captcha_string}, recipient=properties.headers.get("answer_key"),
                    answer_user=properties.headers.get("answer_user"), answer_type="get_captcha")


# Create a connection to queue
broker_obj.channel.basic_consume(queue='captcha_service',
                                 auto_ack=True,
                                 on_message_callback=callback)

try:
    # Starting service
    print("Captcha server initialize successful.", flush=True)
    broker_obj.channel.start_consuming()
finally:
    broker_obj.connection.close()
