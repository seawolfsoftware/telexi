from django.db import models


class PressEvent(models.Model):
    device_id = models.CharField(max_length=3)
    is_button_on = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.device_id
