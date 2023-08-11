from django.db import models
from django.core.validators import MinValueValidator
from v1.models.consumptions import Consumptions


class Appointments(models.Model):
    registration_id = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    scheduling = models.DateTimeField()
    created_by = models.ForeignKey(Consumptions, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Appointments, self).save(*args, **kwargs)
