import hashlib
import os
import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


def ticket_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_string = str(uuid.uuid4())
    hash_object = hashlib.sha256(unique_string.encode('utf-8'))
    unique_filename = hash_object.hexdigest()
    return os.path.join('tickets', instance.user.username, f"{unique_filename}.{ext}")


class Ticket(models.Model):
    """Modèle pour les demandes de critiques."""

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=ticket_image_path, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Supprimer l'image si elle existe
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Review(models.Model):
    """Modèle pour les critiques."""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.ticket.title}"

    class Meta:

        constraints = [models.UniqueConstraint(fields=['ticket'], name='unique_review_per_ticket')]


class UserFollows(models.Model):
    """Modèle pour gérer les abonnements entre utilisateurs."""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by'
    )

    class Meta:
        # Garantit qu'un utilisateur ne peut suivre un autre utilisateur qu'une seule fois
        unique_together = ('user', 'followed_user')
        # Empêche un utilisateur de se suivre lui-même
        constraints = [
            models.CheckConstraint(check=~models.Q(user=models.F('followed_user')), name='cannot_follow_self')
        ]

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"


class UserBlocks(models.Model):
    """Modèle pour gérer les utilisateurs bloqués."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocking',
        help_text="L'utilisateur qui bloque",
    )
    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by',
        help_text="L'utilisateur qui est bloqué",
    )
    date_blocked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} à bloqué {self.blocked_user}"

    class Meta:
        unique_together = ('user', 'blocked_user')
        verbose_name_plural = 'User blocks'

    def save(self, *args, **kwargs):
        UserFollows.objects.filter(user=self.user, followed_user=self.blocked_user).delete()
        UserFollows.objects.filter(user=self.blocked_user, followed_user=self.user).delete()
        super().save(*args, **kwargs)
