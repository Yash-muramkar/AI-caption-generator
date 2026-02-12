from django.db import models

class GeneratedCaption(models.Model):
    media = models.FileField(upload_to="uploads/")
    raw_caption = models.TextField()
    final_caption = models.TextField()
    hashtags = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.final_caption[:50]
