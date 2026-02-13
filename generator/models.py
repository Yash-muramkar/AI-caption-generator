from django.db import models


class GeneratedCaption(models.Model):

    media = models.FileField(upload_to="uploads/")
    raw_caption = models.TextField()
    final_caption = models.TextField()
    hashtags = models.TextField()

    ai_model = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


    def __str__(self):
        return self.final_caption[:50]


    def delete(self, *args, **kwargs):
        self.media.delete()
        super().delete(*args, **kwargs)
