from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    """
    sender: the model that sent the signal
    instance: the instance of model that triggered this signal
    created: let us know whether the user's action (ADD/UPDATE) - True/False
    """

    if created:
        print("Creating new user:", instance)
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = "Welcome to DevSearch"
        message = "We are glad you are here."

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    """
    When a user update his/her profile, we want to update their user model as well
    """
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    print("Deleting user:", instance)
    user = instance.user
    user.delete()


# Connect the signal
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
