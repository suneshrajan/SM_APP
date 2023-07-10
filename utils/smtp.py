import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(user_name=None, otp=None):
    # SMTP server configuration
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    # Email content
    sender = 'sunesh.rajan@outlook.com'
    password = 'Sunsetpoint@1'
    receiver = 'sunesh17498@gmail.com'
    subject = 'VERIFY YOUR ACCOUNT'
    message = f'Dear {user_name},\n\nYour account was successfuly created, please verify your email using this otp {otp}. \
                \n\n\nnote: Your accout willbe automacilly deactivated after 7pm, please verify your email to prevent this. \
                \n\n\n\n Thanks & Regords, \n Sunesh Rajan'

    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    # Attach the message to the MIME message
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Authentication
        server.login(sender, password)

        # Send the email
        server.sendmail(sender, receiver, msg.as_string())
        print('Email sent successfully.')

    except Exception as e:
        print('An error occurred while sending the email:', str(e))

    finally:
        # Close the SMTP server connection
        server.quit()