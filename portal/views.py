from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student, StudentMarks, Subject
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import logging

logger = logging.getLogger('app_logger')


class LoginPage(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            logger.info(f"[LOGIN SUCCESS] User '{username}' logged in.")
            return super().form_valid(form)
        else:
            logger.warning(f"[LOGIN FAILED] Invalid credentials for user '{username}'.")
            form.add_error(None, "Invalid Username or Password")
            return self.form_invalid(form)


@method_decorator(csrf_exempt, name='dispatch')
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = StudentMarks.objects.select_related('student', 'subject')
        context['subjects'] = Subject.objects.all()
        logger.debug("[DASHBOARD LOAD] Student data loaded.")
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get('name')
            subject_id = request.POST.get('subject_id')
            marks = int(request.POST.get('marks'))

            if not name or not subject_id:
                logger.warning("[MARK ENTRY] Missing required fields.")
                return JsonResponse({'status': 'error', 'message': 'Name and Subject are required.'}, status=400)

            subject = Subject.objects.get(id=subject_id)
            student, _ = Student.objects.get_or_create(name=name)

            student_mark = StudentMarks.objects.filter(student=student, subject=subject).first()

            if student_mark:
                student_mark.marks += marks
                student_mark.save()
                logger.info(f"[MARK UPDATED] Existing student '{name}' updated with +{marks} marks in '{subject.subject_name}'. Total: {student_mark.marks}")
                return JsonResponse({'status': 'updated', 'message': 'Marks updated successfully.', 'new_mark': student_mark.marks})
            else:
                StudentMarks.objects.create(
                    student=student,
                    subject=subject,
                    marks=marks,
                    teacher=request.user
                )
                logger.info(f"[MARK CREATED] New student entry: '{name}' with {marks} marks in '{subject.subject_name}'.")
                return JsonResponse({'status': 'created', 'message': 'New student mark added successfully.'})

        except Subject.DoesNotExist:
            logger.error(f"[SUBJECT ERROR] Subject with ID {subject_id} does not exist.")
            return JsonResponse({'status': 'error', 'message': 'Invalid subject.'}, status=400)

        except Exception as e:
            logger.error(f"[MARK ERROR] Unexpected error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def edit_student_mark(request, mark_id):
    if request.method == "POST":
        try:
            mark = get_object_or_404(StudentMarks, uuid=mark_id)

            new_name = request.POST.get('name')
            subject_id = request.POST.get('subject_id')
            marks = int(request.POST.get('marks'))

            if not new_name or not subject_id:
                logger.warning("[STUDENT EDIT] Missing required fields.")
                return JsonResponse({'status': 'error', 'message': 'Name and Subject are required.'}, status=400)

            # Get or create student
            student, _ = Student.objects.get_or_create(name=new_name)
            subject = get_object_or_404(Subject, id=subject_id)

            # Check for uniqueness (exclude the current mark being edited)
            existing = StudentMarks.objects.filter(student=student, subject=subject).exclude(uuid=mark.uuid).first()
            if existing:
                logger.warning(f"[STUDENT EDIT] Duplicate student '{new_name}' and subject '{subject.subject_name}' combination.")
                return JsonResponse({'status': 'error', 'message': 'A record already exists for this student and subject.'}, status=400)

            # Update the record
            mark.student = student
            mark.subject = subject
            mark.marks = marks
            mark.save()

            logger.info(f"[STUDENT EDIT] Updated record: student '{student.name}', subject '{subject.subject_name}', marks {marks}")
            return JsonResponse({'status': 'success', 'message': 'Student details updated successfully', 'new_mark': mark.marks})

        except Exception as e:
            logger.error(f"[STUDENT EDIT ERROR] {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    logger.warning("[STUDENT EDIT] Invalid request method.")
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)



@csrf_exempt
def delete_student_mark(request, mark_id):
    if request.method == "POST":
        try:
            student_mark = get_object_or_404(StudentMarks, uuid=mark_id)
            logger.info(f"[STUDENT DELETE] Deleting mark for student '{student_mark.student.name}' and subject '{student_mark.subject.subject_name}'.")
            student_mark.delete()
            return JsonResponse({'status': 'success', 'message': 'Student Details deleted successfully'})
        except Exception as e:
            logger.error(f"[DELETE ERROR] {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    logger.warning("[STUDENT DELETE] Invalid request method.")
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def logout_view(request):
    username = request.user.username if request.user.is_authenticated else "Anonymous"
    logger.info(f"[LOGOUT] User '{username}' logged out.")
    logout(request)
    return redirect('login')
