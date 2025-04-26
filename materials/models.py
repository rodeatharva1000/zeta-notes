from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")


class Subject(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name

class Content(models.Model):
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='pdfs/', validators=[validate_pdf])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.description[:30]} - {self.subject.name}'