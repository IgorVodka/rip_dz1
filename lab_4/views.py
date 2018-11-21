import sys

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from lab_4.models import User, Department, Subject, Teacher

if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from lab_4.forms import AddTeacherForm, AddSubjectForm, UpdateUserForm, AppointTeacherForm, SetTeacherPhotoForm


class IndexView(TemplateView):
    def get(self, *args, **kwargs):
        data = {
            'departments': Department.objects.all(),
            'front_page': True
        }
        return render(self.request, 'index.html', data)


class DepartmentMixin:
    def prepare_subjects(self, department, request):
        from django.db.models import Count
        from django.db.models import Q
        subjects = Subject.objects.filter(Q(teachers__department=department) | Q(default_department=department))
        subjects = subjects.annotate(dcount=Count('id')).order_by('-semester')
        from django.core.paginator import Paginator
        paginator = Paginator(subjects, 12)
        return paginator.get_page(self.request.GET.get('page'))


class DepartmentView(TemplateView, DepartmentMixin):
    def get(self, *args, **kwargs):
        department = kwargs['id']
        data = {
            'department': Department.objects.get(id=department),
            'form': AddSubjectForm(initial={'default_department': department})
        }
        return render(self.request, 'department.html', data)


class SubjectView(TemplateView):
    def get(self, *args, **kwargs):
        subject = Subject.objects.filter(id=kwargs['id']).first()
        data = {
            'subject': subject,
            'add_form': AddTeacherForm(initial={'department': subject.default_department}),
            'appoint_form': AppointTeacherForm
        }
        return render(self.request, 'subject.html', data)


@method_decorator(login_required, name='dispatch')
class AddTeacherView(CreateView):
    model = Teacher
    fields = ['first_name', 'patronymic', 'last_name', 'department']

    def form_valid(self, form):
        form = super().form_valid(form)
        Subject.objects.get(id=self.kwargs['subject_id']).teachers.add(self.object)
        return form

    def get_success_url(self):
        return reverse('teacher', kwargs={'id': self.object.id})


@method_decorator(login_required, name='dispatch')
class AppointTeacherView(View):
    def post(self, *args, **kwargs):
        form = AppointTeacherForm(self.request.POST)
        if form.is_valid():
            selected_teacher = form.cleaned_data['teacher']
            if selected_teacher is None:
                raise Exception('This teacher does not exist, and you are a hacker')
            selected_teacher.subjects.add(kwargs['subject_id'])
            selected_teacher.save()
        return redirect('subject', kwargs['subject_id'])


class TeacherView(TemplateView):
    def get(self, *args, **kwargs):
        data = {
            'teacher': Teacher.objects.filter(id=kwargs['id']).first(),
            'form': SetTeacherPhotoForm
        }
        return render(self.request, 'teacher.html', data)


@method_decorator(login_required, name='dispatch')
class UpdateTeacherView(UpdateView):
    model = Teacher
    fields = ['photo']

    def get_object(self):
        return Teacher.objects.get(id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('teacher', kwargs={'id': self.object.id})


@method_decorator(login_required, name='dispatch')
class ProfileView(FormView):
    model = User
    template_name = 'registration/profile.html'
    form_class = UpdateUserForm                     # uh

    def get_initial(self):
        super(ProfileView, self).get_initial()
        model = User.objects.get(id=self.request.user.id)
        self.initial = {
            'username': model.username,
            'first_name': model.first_name,
            'last_name': model.last_name,
            'avatar': model.avatar
        }
        return self.initial


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'avatar']
    success_url = '/accounts/profile'

    def get_object(self):
        return User.objects.get(id=self.request.user.id)
