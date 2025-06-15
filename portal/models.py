from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid


class Subject(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

    
class Student(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


class StudentMarks(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='stu_marks')
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stu_teacher')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='stu_subject')
    marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        unique_together = ('student', 'subject')  
        verbose_name_plural = "Student Marks"

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks}"