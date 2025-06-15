from django.test import TestCase
from .models import Student, Subject, StudentMarks

class StudentMarkTest(TestCase):
    def test_student_creation(self):
        student = Student.objects.create(name="Test User")
        self.assertEqual(str(student.name), "Test User")
