from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from lab_4.models import Like, Teacher, User, Subject
from lab_4.views import DepartmentMixin


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ApiLikesView(View):
    def get(self, *args, **kwargs):
        likes = Like.objects.filter(teacher=kwargs['teacher_id']).all()
        return JsonResponse({'likes': list(map(
            lambda like: {'id': like.user.id, 'username': like.user.username},
            likes
        ))})

    def post(self, *args, **kwargs):
        query = Q(teacher=kwargs['teacher_id']) & Q(user=self.request.user.id)
        if Like.objects.filter(query).count() > 0:
            likes = Like.objects.filter(query).all()
            for like in likes:
                like.delete()
        else:
            like = Like()
            like.teacher = Teacher.objects.get(id=kwargs['teacher_id'])
            like.user = User.objects.get(id=self.request.user.id)
            like.save()
        return JsonResponse({'success': True})


class ApiDepartmentView(View, DepartmentMixin):
    def get(self, *args, **kwargs):
        department = kwargs['id']
        subjects = self.prepare_subjects(department, self.request)
        data = {
            'subjects': [{'id': subject.id, 'name': subject.name, 'semester': subject.semester} for subject in subjects],
            'pagination': {
                'current': self.request.GET.get('page') or 1,
                'total': subjects.paginator.num_pages
            }
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ApiAddSubjectView(CreateView):
    model = Subject
    fields = ['name', 'semester', 'default_department']

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False}, status=400)
