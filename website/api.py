from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from revelation_ink import settings
from revelation_ink.logger import logger
from datetime import datetime

class ContactForm(APIView):
    """
    Starts the process of bundling a running instance
    """

    def post(self, request):
        """
        Send an email and return 200
        """
        data = request.DATA
        email_addr = data.get('email')
        subject = "Contact Form Submission"
        message = "From:%s\nE-mail:%s\nMessage:%s\n---\nForm submission time:%s \nForm submitted from IP:%s" % (data.get('full-name','no-name'),email_addr if email_addr else 'no-email', data.get('message','no-message'), datetime.now(), request.META['REMOTE_ADDR'])

        try:
            send_email(subject, message, email_addr)
            return Response('')
        except Exception, e:
            logger.error(e)
            return Response('Email Failed: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def send_email(subject, message, sent_by=None):
  from email.mime.text import MIMEText
  from subprocess import Popen, PIPE
  import smtplib
  adminemail = settings.ADMINS[0][1]
  toemail = settings.ADMINS[0][1]
  fromemail = adminemail # Can no longer 'send as the user'
  email = MIMEText(message)
  email['Subject'] = subject
  email['From'] = fromemail
  email['To'] = toemail
  if sent_by:
      email['cc'] = sent_by
  logger.debug(email.as_string())

  from revelation_ink.secrets import SMTP_USERNAME, SMTP_PASSWORD
  s = smtplib.SMTP('mail.rev-ink.com')
  s.login(SMTP_USERNAME, SMTP_PASSWORD)
  s.sendmail(fromemail, toemail, email.as_string())
  s.quit()
  return True
  #p = Popen(['/usr/sbin/sendmail', '-t'], stdin=PIPE)
  #p.communicate(email.as_string())
  #return True

  

  # sendmail function takes 3 arguments: sender's address, recipient's address
  # and message to send - here it is sent as one string.
  # Send the message via local SMTP server.
