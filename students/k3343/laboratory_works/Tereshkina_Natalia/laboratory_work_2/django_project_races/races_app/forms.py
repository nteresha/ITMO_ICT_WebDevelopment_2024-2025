from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Racer, Race, Team, Comment


class UserRegistrationForm(UserCreationForm):
    USER_TYPES = [
        ('racer', 'Гонщик'),
        ('admin', 'Администратор'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, label='Тип пользователя', widget=forms.Select(attrs={'id': 'user_type'}))
    managed_race = forms.ModelChoiceField(queryset=Race.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type', 'managed_race')
        labels = {
            'username': "Имя пользователя",
            'password1': "Пароль",
            'password2': "Подтверждение пароля",
            'user_type': "Тип пользователя",
            'managed_race': "Гонка (для администратора)",
        }
        widgets = {
            'username': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'user_type': forms.Select(),
            'managed_race': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

        if self.instance and self.instance.user_type == 'admin':
            self.fields['managed_race'].required = True


class RacerProfileForm(forms.ModelForm):
    full_name = forms.CharField(label="Полное имя")
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Команда")
    car_description = forms.CharField(label="Описание машины", widget=forms.Textarea())
    participant_description = forms.CharField(label="Описание участника", widget=forms.Textarea())
    experience = forms.IntegerField(label="Опыт (лет)")
    racer_class = forms.ChoiceField(choices=Racer.RACER_CLASS, label="Класс гонщика")

    class Meta:
        model = Racer
        fields = ['full_name', 'team', 'car_description', 'participant_description', 'experience', 'racer_class']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('rating', 'text', 'comment_type')