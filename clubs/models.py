from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()

    def __str__(self):
        return f'Member(id={self.id}, last_name={self.last_name})'
