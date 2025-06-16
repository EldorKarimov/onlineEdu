from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class About(BaseModel):
    content = RichTextUploadingField()

    def __str__(self):
        return self.content[:20]