from django.db import models
import uuid


class Language(models.Model):
    code = models.CharField(max_length=2)
    language = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.code


class ContentType(models.Model):
    content_type = models.CharField(max_length=30, primary_key=True)

    def __str__(self) -> str:
        return self.content_type


class LowerCaseField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCaseField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Content(models.Model):
    class Meta:
        unique_together = (("name", "content_type"))
    name = LowerCaseField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.content_type}: {self.name}"


class Translation(models.Model):
    class Meta:
        unique_together = (("language_code", "belongs_to"))
    language_code = models.ForeignKey(Language, on_delete=models.CASCADE)
    belongs_to = models.ForeignKey(Content, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.belongs_to} ({self.language_code})"
