from django.db import models

class SlipperyPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    slipperiness = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.latitude}, {self.longitude}) - Slipperiness: {self.slipperiness}"