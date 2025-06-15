from django.urls import path
from portal import views 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.LoginPage.as_view(),name='login'),
    path('home/',views.HomeView.as_view(),name="home"),
    path('student/edit/<uuid:mark_id>/',views.edit_student_mark, name='edit-mark'),
    path('student/delete/<uuid:mark_id>/',views.delete_student_mark, name='delete-mark'),
    path('logout/', views.logout_view, name='logout'),
]