from django.db import models
from django.contrib.auth.models import User

def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "users/user_{pk}/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(blank=True, null=True, upload_to=profile_avatar_directory_path)
