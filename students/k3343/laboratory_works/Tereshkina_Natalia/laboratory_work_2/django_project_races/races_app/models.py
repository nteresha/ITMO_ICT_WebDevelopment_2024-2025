from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Race(models.Model):
    RACE_TYPES = (
        ('ring', 'Кольцевые гонки'),
        ('rally', 'Ралли'),
        ('trophy', 'Трофи'),
        ('endurance', 'Гонки на выносливость'),
        ('drag', 'Дрэг-рейсинг'),
    )
    RACE_STATUS = (
        ('scheduled', 'Запланирована'),
        ('in process', 'В процессе'),
        ('finished', 'Завершена'),
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=RACE_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(max_length=20, choices=RACE_STATUS)


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('racer', 'Гонщик'),
        ('admin', 'Администратор'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='racer')
    managed_race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True, blank=True, related_name='admins')


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Racer(models.Model):
    RACER_CLASS = (
        ('Новичок', 'Новичок'),
        ('Любитель', 'Любитель'),
        ('Профессионал', 'Профессионал')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    car_description = models.TextField()
    participant_description = models.TextField()
    experience = models.PositiveIntegerField()
    racer_class = models.CharField(max_length=50, choices=RACER_CLASS)


class Registration(models.Model):
    REGISTRATION_STATUS = (
        ('pending', 'Ожидает подтверждения'),
        ('approved', 'Подтверждена'),
        ('rejected', 'Отклонена')
    )
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='pending')


class Comment(models.Model):
    COMMENT_TYPES = (
        ('collaboration', 'Сотрудничество'),
        ('race', 'Гонка'),
        ('other', 'Другое'),
    )
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
