import time
import random

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def send_notify_mail(item, scrape_payload):
    while not scrape_payload.get('emailed'):
        try:
            plain_text = get_template('emails/amazon_notify_email.txt')
            html_template = get_template('emails/amazon_notify_email.html')

            context = {
                'landing_image': item.landing_image,
                'current_price': scrape_payload.get('current_price'),
                'item_url': item.url,
                'unsubscribe_url': 'https://amazontrack.herokuapp.com/unsubscribe/{id}'.format(id=item.id)
            }

            subject_start = 'Price change for ' if item.notify_when == 'change' else 'Lower price for '
            subject = subject_start + item.title
            from_email = settings.EMAIL_HOST_USER
            to_email = item.user.username
            text_content = plain_text.render(context)
            html_content = html_template.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            print('HEY EMAIL HAS BEEN SENT!')

            scrape_payload['emailed'] = True
        
        except Exception as e:
            print(str(e))
            rest_time = random.choice([1,2,4,8,16,32])
            print('email resting...', rest_time) 
            time.sleep(rest_time)