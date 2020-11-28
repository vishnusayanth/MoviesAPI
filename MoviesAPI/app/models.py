from django.core.exceptions import ValidationError
from django.db import models


# Model to save the request count calculated at the custom middleware.
# Only a single object can exist at a time. Handled by overriding the save function.
class RequestCounter(models.Model):
    value = models.IntegerField(default=None)

    def save(self, *args, **kwargs):
        if not self.pk and RequestCounter.objects.exists():
            raise ValidationError('There is can be only one RequestCounter instance')
        return super(RequestCounter, self).save(*args, **kwargs)
