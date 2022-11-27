from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    photo = models.ImageField(
        upload_to="account/%Y/%m/%d/", default="default.jpg", blank=True
    )
    bio = models.TextField()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})
