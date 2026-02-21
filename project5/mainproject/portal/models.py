from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Alert(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('resolved', 'Resolved'),
    )

    SEVERITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    disaster_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    # 🔥 ADD THESE TWO LINES
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_time = models.DateTimeField(auto_now_add=True)
    auto_generated = models.BooleanField(default=False)


    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f"{self.disaster_type} - {self.location}"
