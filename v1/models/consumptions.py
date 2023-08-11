from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Consumptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255, blank=False, null=False)
    appointments_entries = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    imported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def clean(self):
        if not self.file_name.strip():
            raise ValidationError({"file_name": "File name cannot be empty or just whitespace."})
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Consumptions, self).save(*args, **kwargs)

