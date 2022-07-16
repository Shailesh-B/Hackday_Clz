from django.contrib.auth.models import AbstractUser
from django.db import models
# from .college import Semester


class CustomUser(AbstractUser):
    email = models.EmailField()
    address = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    profile = models.ImageField(upload_to='images/profiles')
    is_teacher = models.BooleanField(default=False)
    semester = models.ForeignKey("Semester", on_delete=models.SET_NULL,
                                 related_name="student", related_query_name="has_student", null=True,blank=True)
    def save(self,*args,**kwargs):
        if self.is_teacher:
            self.semester = None
        super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.get_full_name()}"
