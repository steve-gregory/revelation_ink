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
        subject = "Contact Form Submission"
        message = "From:%s\nE-mail:%s\nMessage:%s\n---\nForm submission time:%s \nForm submitted from IP:%s" % (data.get('full-name','no-name'), data.get('email','no-email'), data.get('message','no-message'), datetime.now(), request.META['REMOTE_ADDR'])
        if not send_email(subject, message):
            return Response('Email Failed', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response('')
        
def send_email(subject, message):
  from email.mime.text import MIMEText
  from subprocess import Popen, PIPE
  adminemail = settings.ADMINS[0][1]
  toemail = settings.ADMINS[1][1]
  email = MIMEText(message)
  email['Subject'] = subject
  email['From'] = adminemail
  email['To'] = toemail
  logger.debug(email.as_string())
  p = Popen(['/usr/sbin/sendmail', '-t'], stdin=PIPE)
  p.communicate(email.as_string())
  return True

