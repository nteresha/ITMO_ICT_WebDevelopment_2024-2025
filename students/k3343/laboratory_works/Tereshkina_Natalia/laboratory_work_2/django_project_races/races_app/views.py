from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Race, Comment, Racer, Registration
from .forms import UserRegistrationForm, RacerProfileForm, CommentForm


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'racer':
                return redirect('racer_profile_setup')
            else:
                login(request, user)
                return redirect('all_races')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('all_races')


def racer_profile_setup(request):
    if not request.user.is_authenticated or request.user.user_type != 'racer':
        return redirect('all_races')
    if request.method == 'POST':
        form = RacerProfileForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            racer.user = request.user
            racer.save()
            return redirect('all_races')
    else:
        form = RacerProfileForm()
    return render(request, 'racer_profile_setup.html', {'form': form})


def get_all_races(request):
    query = request.GET.get('query', '')
    if query:
        races = Race.objects.filter(name__icontains=query)
    else:
        races = Race.objects.all()
    paginator = Paginator(races, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'race_list.html', {'page_obj': page_obj, 'races': page_obj.object_list, 'query': query})


def get_race_participants(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    participants = race.registration_set.filter(status__in=['approved', 'pending'])
    return render(request, 'race_participants.html', {'race': race, 'participants': participants})


@login_required
def get_race_comments(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    comments = Comment.objects.filter(race=race)
    return render(request, 'race_comments.html', {'race': race, 'comments': comments})


@login_required
def get_racer_info(request, racer_id):
    racer = get_object_or_404(Racer, id=racer_id)
    registrations = racer.registration_set.all()
    return render(request, 'racer_profile.html', {'racer': racer, 'registrations': registrations})


@login_required
def register_for_race(request, race_id):
    try:
        race = Race.objects.get(pk=race_id)
    except Race.DoesNotExist:
        raise Http404("Race does not exist")
    racer = Racer.objects.get(user=request.user)
    if request.method == 'POST':
        registration = Registration(race=race, racer=racer, status='pending')
        registration.save()
        return redirect('racer_profile', racer_id=racer.id)
    return render(request, 'register_for_race.html', {'race_id': race_id})


def cancel_registration(request, registration_id):
    racer = Racer.objects.get(user=request.user)
    try:
        registration = Registration.objects.get(id=registration_id)
        if registration.racer.user != request.user:
            raise Http404("Вы не можете отменить регистрацию для этого гонщика.")
        registration.delete()
        return redirect('racer_profile', racer_id=racer.id)
    except Registration.DoesNotExist:
        raise Http404("Регистрация не найдена.")


@login_required
def create_review(request, registration_id):
    try:
        registration = Registration.objects.get(id=registration_id)
    except Registration.DoesNotExist:
        raise Http404("Registration does not exist")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = registration.race
            comment.commentator = request.user
            comment.save()
            return redirect('all_races')
    else:
        form = CommentForm()
    return render(request, 'create_review.html', {'form': form, 'registration': registration})


@login_required
def race_applications(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    # Проверяем, является ли пользователь администратором этой гонки
    if not request.user.is_authenticated or request.user.user_type != 'admin' or race != request.user.managed_race:
        raise Http404("У вас нет прав для доступа к этой странице")

    registrations = Registration.objects.filter(race=race)

    if request.method == "POST":
        registration_id = request.POST.get('registration_id')
        new_status = request.POST.get('status')

        registration = get_object_or_404(Registration, id=registration_id)

        if registration.race != race:
            raise Http404("Заявка не принадлежит этой гонке")

        if new_status in ['approved', 'rejected']:
            registration.status = new_status
            registration.save()

        return redirect('race_applications', race_id=race.id)

    return render(request, 'admin_registrations.html', {
        'race': race,
        'registrations': registrations
    })
