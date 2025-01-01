from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from account.forms import LoginForm
from reviews.models import Review, Ticket, UserBlocks, UserFollows


@login_required
def user_posts(request):
    """Vue pour afficher les posts de l'utilisateur."""

    tickets = (
        Ticket.objects.filter(user=request.user)
        .select_related('user')
        .prefetch_related('review_set')
        .order_by('-time_created')
    )

    # Pour chaque ticket, récupére les critiques associées
    posts = []
    for ticket in tickets:
        posts.append({'type': 'TICKET', 'post': ticket, 'has_review': ticket.review_set.exists()})

    # Récupére les critiques faites par l'utilisateur
    user_reviews = Review.objects.filter(user=request.user).select_related('user', 'ticket').order_by('-time_created')
    for review in user_reviews:
        posts.append({'type': 'REVIEW', 'post': review})

    # Trier tous les posts par date
    posts.sort(key=lambda x: x['post'].time_created, reverse=True)

    return render(request, 'feed/user_posts.html', {'posts': posts})


def home(request):
    """Vue pour la page d'accueil et le flux."""
    if request.user.is_authenticated:

        # Récupérer les utilisateurs qui ont bloqué l'utilisateur actuel
        blocked_by = UserBlocks.objects.filter(blocked_user=request.user).values_list('user', flat=True)

        # Récupérer les utilisateurs suivis
        followed_users = (
            UserFollows.objects.filter(user=request.user)
            .exclude(followed_user__in=blocked_by)
            .values_list('followed_user', flat=True)
        )

        tickets = (
            Ticket.objects.filter(Q(user=request.user) | Q(user__in=followed_users))
            .select_related('user')
            .prefetch_related('review_set')
            .order_by('-time_created')
        )

        posts = []
        for ticket in tickets:
            posts.append({'type': 'TICKET', 'post': ticket, 'has_review': ticket.review_set.exists()})

        reviews = (
            Review.objects.filter(Q(user=request.user) | Q(user__in=followed_users) | Q(ticket__user=request.user))
            .select_related('user', 'ticket')
            .distinct()
        )

        for review in reviews:
            posts.append({'type': 'REVIEW', 'post': review})

        # Trier par date
        posts.sort(key=lambda x: x['post'].time_created, reverse=True)

        return render(request, 'feed/feed.html', {'posts': posts})

    # Gestion de la connexion
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('home')
        else:
            messages.error(request, 'Identifiants incorrects')
    else:
        form = LoginForm()

    return render(request, 'feed/home.html', {'form': form})


def logout_user(request):
    if request.method == 'POST':
        messages.success(request, 'Vous êtes déconnecté')
        logout(request)
    return redirect('home')
