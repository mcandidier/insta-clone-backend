

from anymail.message import AnymailMessage


def send_reset_password(email, token):
    message = AnymailMessage(
        to=[email],
    )
        # Anymail extra attributes:
    message.template_id = 1  # use this Sendinblue template
    message.from_email = None  # to use the template's default sender
    message.merge_global_data = {
        'token': str(token),
    }
    message.send() 