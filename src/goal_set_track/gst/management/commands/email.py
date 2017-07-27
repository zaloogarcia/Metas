EMAIL = 'gstenterpriseas@gmail.com'
PASSWORD = 'gstenterpriseasgstenterpriseas'

import smtplib

class Email():
    def send(self, destination, subject, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n".format(EMAIL, destination, subject)
        msg += message
        server.sendmail(EMAIL, destination, msg)
        print(msg)
        server.quit()
