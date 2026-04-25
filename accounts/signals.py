from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def add_points_on_login(sender, request, user, **kwargs):
    if hasattr(user, 'profile'):
        user.profile.points += 5
        user.profile.save(update_fields=['points'])
        user.profile.check_level_up()