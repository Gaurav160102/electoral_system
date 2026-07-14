from django.db import models

class Voter(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=200)
    father_husband_name = models.CharField(max_length=200, verbose_name="Father/Husband Name")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    epic_no = models.CharField(max_length=50, unique=True, verbose_name="EPIC No.")
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='voter_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Voter"
        verbose_name_plural = "Voters"

    def __str__(self):
        return f"{self.name} ({self.epic_no})"