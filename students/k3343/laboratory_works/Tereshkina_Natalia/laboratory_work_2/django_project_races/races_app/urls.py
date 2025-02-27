from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/setup/', views.racer_profile_setup, name='racer_profile_setup'),
    path('races/', views.get_all_races, name='all_races'),
    path('races/<int:race_id>/participants/', views.get_race_participants, name='race_participants'),
    path('races/<int:race_id>/comments/', views.get_race_comments, name='race_comments'),
    path('racer_profile/<int:racer_id>/', views.get_racer_info, name='racer_profile'),
    path('ragister_for_race/<int:race_id>/', views.register_for_race, name='ragister_for_race'),
    path('cancel_registration/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
    path('create_review/<int:registration_id>/', views.create_review, name='create_review'),
    path('race/<int:race_id>/applications/', views.race_applications, name='race_applications'),

]
