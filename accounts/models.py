from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.

USER_TYPE_CHOICES=(
    ('STUDENT', 'STUDENT'),
    ('TEACHER', 'TEACHER'),
    )
class User(AbstractUser):
    user_type = models.CharField(choices=USER_TYPE_CHOICES,max_length=100)
class Student(models.Model):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    subject = models.ManyToManyField('Subject')
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name

class TeacherEnroll(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
class StudentEnroll(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher)

