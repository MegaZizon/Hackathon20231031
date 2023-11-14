from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string

def send(receiverEmail,verifyCode):
    try:
        content = {'verifyCode':verifyCode}
        print(verifyCode)
        msg_html = render_to_string('sendEmail/email_format.html',content)
        print(msg_html)
        msg = EmailMessage(subject="인증 코드 발송 메일",body=msg_html,from_email="wnsdh8846@gmail.com",bcc=[receiverEmail])
        msg.content_subtype='html'
        msg.send()
        return True
    except:
        return False
