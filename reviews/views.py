from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from litrevu import settings

from .forms import DeleteReviewForm, DeleteTicketForm, ReviewForm, TicketForm, UserFollowsForm
from .models import Review, Ticket, UserBlocks, UserFollows


@login_required
def ticket_create(request):
    """Vue pour créer un nouveau ticket."""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Votre ticket a été créé avec succès.')
            return redirect('home')
    else:
        form = TicketForm()

    return render(request, 'reviews/ticket_form.html', {'form': form, 'title': 'Créer un ticket'})


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier ce ticket.")

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)

        #  si une nouvelle img a été uplod
        if 'image' in request.FILES:
            # Avant de toucher au formulaire, on supprime l'ancienne image si elle existe
            if ticket.image:
                import os

                old_image_path = os.path.join(settings.MEDIA_ROOT, ticket.image.name)

                # On vérifie si l'img  existe et on le supprime
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
                    print(f"Fichier supprimé: {old_image_path}")

                # On nettoie la ref dans la bdd
                ticket.image = None
                ticket.save()

        if form.is_valid():
            form.save()
            messages.success(request, 'Votre ticket a été modifié avec succès.')
            return redirect('home')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/ticket_form.html', {'form': form, 'ticket': ticket, 'title': 'Modifier le ticket'})


@login_required
def ticket_delete(request, ticket_id):
    """Vue pour supprimer un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce ticket.")

    if request.method == 'POST':
        form = DeleteTicketForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            ticket.delete()
            messages.success(request, 'Votre ticket a été supprimé avec succès.')
            return redirect('user_posts')
    else:
        form = DeleteTicketForm()

    return render(request, 'reviews/ticket_confirm_delete.html', {'form': form, 'ticket': ticket})


@login_required
def review_create(request, ticket_id):
    """Vue pour créer une critique sur un ticket existant."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, 'Vous avez déjà publié une critique pour ce ticket.')
        return redirect('home')

    if UserBlocks.objects.filter(user=ticket.user, blocked_user=request.user).exists():
        messages.error(request, "Vous ne pouvez pas créer de critique car l'auteur du ticket vous a bloqué.")
        return redirect('home')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Votre critique a été publiée avec succès.')
            return redirect('home')
    else:
        form = ReviewForm()

    return render(
        request,
        'reviews/review_form.html',
        {
            'form': form,
            'ticket': ticket,
            'title': 'Publier une critique',
            'subtitle': 'Créez votre critique et partagez votre avis',
        },
    )


@login_required
def create_ticket_and_review(request):
    """Vue pour créer un ticket et sa critique en même temps."""
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, 'Votre ticket et votre critique ont été publiés avec succès.')
            return redirect('home')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(
        request,
        'reviews/ticket_and_review_form.html',
        {'ticket_form': ticket_form, 'review_form': review_form, 'title': 'Créer une critique'},
    )


@login_required
def review_edit(request, review_id):
    """Vue pour modifier une critique existante."""
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier cette critique.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre critique a été modifiée avec succès.')
            return redirect('home')
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        'reviews/review_form.html',
        {
            'form': form,
            'ticket': review.ticket,
            'title': 'Modifier la critique',
            'subtitle': 'Modifiez votre critique et partagez votre avis',
        },
    )


@login_required
def review_delete(request, review_id):
    """Vue pour supprimer une critique."""
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer cette critique.")

    if request.method == 'POST':
        form = DeleteReviewForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            review.delete()
            messages.success(request, 'Votre critique a été supprimée avec succès.')
            return redirect('user_posts')
    else:
        form = DeleteReviewForm()

    return render(request, 'reviews/review_confirm_delete.html', {'form': form, 'review': review})


@login_required
def subscription_page(request):
    if request.method == 'POST':
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            User = get_user_model()
            try:
                user_to_follow = User.objects.get(username=username)

                # Vérifier qu'on n'essaie pas de se suivre soi-même
                if user_to_follow == request.user:
                    messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
                    return redirect('reviews:subscriptions')

                # Vérifier si l'utilisateur est bloqué
                if UserBlocks.objects.filter(user=user_to_follow, blocked_user=request.user).exists():
                    messages.error(request, "Vous ne pouvez pas suivre cet utilisateur car il vous a bloqué.")
                    return redirect('reviews:subscriptions')

                # Vérifier si on ne suit pas déjà cet utilisateur
                if not UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                    messages.success(request, f"Vous suivez maintenant {username}")
                else:
                    messages.warning(request, f"Vous suivez déjà {username}")

            except User.DoesNotExist:
                messages.error(request, "Cet utilisateur n'existe pas.")

            return redirect('reviews:subscriptions')
        else:
            # j'ajoute le message d'erreur au système de messages
            for error in form.errors['username']:
                messages.error(request, error)
    else:
        form = UserFollowsForm()

    # Récupérer les listes d'utilisateurs
    following = UserFollows.objects.filter(user=request.user).select_related('followed_user')
    followers = UserFollows.objects.filter(followed_user=request.user).select_related('user')
    blocked_users = UserBlocks.objects.filter(user=request.user).select_related('blocked_user')

    return render(
        request,
        'reviews/subscription.html',
        {'form': form, 'following': following, 'followers': followers, 'blocked_users': blocked_users},
    )


@login_required
def unfollow_user(request, user_id):
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(get_user_model(), id=user_id)
        UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}")
    return redirect('reviews:subscriptions')


@login_required
def block_user(request, user_id):
    """Vue pour bloquer un utilisateur."""
    user_to_block = get_object_or_404(get_user_model(), id=user_id)

    # Empêcher de se bloquer soi-même
    if user_to_block == request.user:
        messages.error(request, "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect('reviews:subscriptions')

    # Créer le blocage
    UserBlocks.objects.get_or_create(user=request.user, blocked_user=user_to_block)

    messages.success(request, f"Vous avez bloqué {user_to_block.username}")
    return redirect('reviews:subscriptions')


@login_required
def unblock_user(request, user_id):
    """Vue pour débloquer un utilisateur."""
    user_to_unblock = get_object_or_404(get_user_model(), id=user_id)

    # Supprimer le blocage
    UserBlocks.objects.filter(user=request.user, blocked_user=user_to_unblock).delete()

    messages.success(request, f"Vous avez débloqué {user_to_unblock.username}")
    return redirect('reviews:subscriptions')
