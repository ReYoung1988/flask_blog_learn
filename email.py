from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object() #get the real object
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg]) #open a new thread
    thr.start()
    '''    
    print(app.config['MAIL_SERVER'])
    print(app.config['MAIL_PORT'])
    print(app.config['MAIL_USE_SSL'])
    print(app.config['MAIL_USE_TLS'])
    print(app.config['MAIL_USERNAME'])
    print(app.config['MAIL_PASSWORD'])
    print(app.config['FLASKY_MAIL_SUBJECT_PREFIX'])
    print(app.config['FLASKY_MAIL_SENDER'])
    print(app.config['FLASKY_ADMIN'])
    '''
    return thr


