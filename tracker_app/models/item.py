from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=500)
    notify_when = models.CharField(
        max_length=50,
        choices=(
            ("below", "Below certain price"),
            ("down", "Goes down"),
            ("change", "Changes"),
            ("no", "Do not notify")
        )
    )
    desired_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    init_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    landing_image = models.URLField(max_length=500, null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

