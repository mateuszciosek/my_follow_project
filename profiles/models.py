from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics", default="profile_pics/default.jpg")
    bio = models.TextField(max_length=200, blank=True)
    accepted_follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False, blank=True)
    follows = models.ManyToManyField(
        'self', related_name='to_accept_follow', symmetrical=False, blank=True)
    request_follows = models.ManyToManyField(
        'self', related_name='requested_follows', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.follows.add(profile)

    def unfollowe(self, profile):
        self.follows.remove(profile)

    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        self.followed_by.filter(pk=profile.pk).exists()

    def accept_follow(self, profile):
        if profile in self.request_follows:
            profile.accepted_follows.add(self)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
