"""lab_4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

from lab_4.forms import CustomUserRegistrationForm

from lab_4.views import *
from lab_4.api_views import *

urlpatterns = [
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(
        r'accounts/register/',
        RegistrationView.as_view(form_class=CustomUserRegistrationForm),
        name='django_registration_register',
    ),
    path(r'accounts/', include('django_registration.backends.one_step.urls')),
    path(r'accounts/profile', ProfileView.as_view(), name='user_profile'),
    path(r'accounts/profile/update', UpdateProfileView.as_view(), name='update_user_profile'),
    path(r'admin/', admin.site.urls),
    path(r'subject/<int:id>', SubjectView.as_view(), name='subject'),
    path(r'teacher/<int:id>', TeacherView.as_view(), name='teacher'),
    path(r'teacher/update/<int:id>', UpdateTeacherView.as_view(), name='update-teacher'),
    path(r'teacher/add/<int:subject_id>', AddTeacherView.as_view(), name='add-teacher'),
    path(r'teacher/appoint/<int:subject_id>', AppointTeacherView.as_view(), name='appoint-teacher'),
    path(r'department/<int:id>', DepartmentView.as_view(), name='department'),

    path(r'api/likes/<int:teacher_id>', ApiLikesView.as_view(), name='api-likes'),
    path(r'api/department/<int:id>', ApiDepartmentView.as_view(), name='api-department'),
    path(r'api/department/add-subject/<int:department_id>', ApiAddSubjectView.as_view(), name='api-add-subject'),
    path(r'', IndexView.as_view(), name='index')
]
