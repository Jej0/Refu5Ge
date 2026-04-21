from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone


#table qui stocke les token pour verif le mail
class EmailVerifToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        #token exipre après 24 heure
        return (timezone.now() - self.created_at).total_seconds() > 86400
    
