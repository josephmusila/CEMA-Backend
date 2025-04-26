# health_info/models.py
from django.db import models

class HealthProgram(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    doctor=models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='programs',null=True, blank=True)
   


    def __str__(self):
        return self.name

class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'program')

    def __str__(self):
        return f"{self.client} in {self.program}"