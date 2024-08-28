from django.db import models

class UserProfile(models.Model):
    chat_id = models.BigIntegerField(unique=True)  # Chat ID field
    username = models.CharField(max_length=255, null=True, blank=True)
    public_key = models.CharField(max_length=255, null=True, blank=True)
    private_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.public_key if self.public_key else str(self.chat_id)
