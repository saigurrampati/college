from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_phone = models.IntegerField()
    ssc_marks = models.IntegerField()
    inter_marks = models.IntegerField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name


class Department(models.Model):
    code = models.CharField(max_length=10)
    desc = models.CharField(max_length=100)


class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Student = models.OneToOneField(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='media/', null=True, blank=True)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_name = models.CharField(max_length=100)
    staff_department = models.TextField()
    staff_email = models.EmailField()
    staff_phone = models.IntegerField()
    qualification = models.TextField()
    experience = models.IntegerField()
    photo = models.ImageField(upload_to='media1/')

    def __str__(self):
        return self.staff_name
