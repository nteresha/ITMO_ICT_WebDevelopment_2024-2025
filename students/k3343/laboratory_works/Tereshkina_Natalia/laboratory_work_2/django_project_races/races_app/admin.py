from django.contrib import admin
from .models import Racer, Race, Comment, Team, Registration

admin.site.register(Team)
admin.site.register(Racer)
admin.site.register(Race)
admin.site.register(Registration)
admin.site.register(Comment)