from celery import shared_task
from apps.sm_accounts.models import ValidateEmail

@shared_task
def my_scheduled_task():

    # Get the not verified users based on the email vierified
    inactive_users = ValidateEmail.objects.filter(is_verified=False)

    # Deactive not verified users
    inactive_users.update(is_active=False)
