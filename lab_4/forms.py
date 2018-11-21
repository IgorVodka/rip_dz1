from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_registration.forms import RegistrationForm

from lab_4.models import User, Department, Teacher


class CustomUserRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class AddTeacherForm(forms.Form):
    first_name = forms.Field(
        label='Имя',
        required=True
    )
    patronymic = forms.Field(
        label='Отчество',
        required=False
    )
    last_name = forms.Field(
        label='Фамилия',
        required=True
    )
    department = forms.ModelChoiceField(
        label='Кафедра',
        queryset=Department.objects.all()
    )


class SetTeacherPhotoForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['photo']

    def clean_image(self):
        image = self.cleaned_data.get('photo', False)
        if image:
            if image._size > 4 * 1024 * 1024:
                from django.core.exceptions import ValidationError
                raise ValidationError("Image file too large ( > 4mb )")
            return image


class AppointTeacherForm(forms.Form):
    class TeacherModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return f'{obj} ({obj.department})'

    teacher = TeacherModelChoiceField(
        label='Преподаватель',
        queryset=Teacher.objects.order_by('last_name').all(),
        required=True
    )


class AddSubjectForm(forms.Form):
    @staticmethod
    def validate_semester(semester):
        return 0 <= semester <= 8

    name = forms.Field(
        label='Название предмета',
        required=True
    )
    semester = forms.ChoiceField(
        label='Семестр',
        choices=list(map(lambda x: (x, x), range(1, 9))) + [(0, 'Всегда')],
        required=True,
        validators=[validate_semester]
    )
    default_department = forms.ModelChoiceField(
        label='Кафедра по умолчанию',
        queryset=Department.objects.all(),
        required=True,
    )


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def clean_image(self):
        image = self.cleaned_data.get('avatar_file', False)
        if image:
            if image._size > 4 * 1024 * 1024:
                from django.core.exceptions import ValidationError
                raise ValidationError("Image file too large ( > 4mb )")
            return image
