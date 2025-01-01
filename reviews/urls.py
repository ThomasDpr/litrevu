from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    # URLs des tickets
    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/', views.ticket_edit, name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),
    
    # URLs des reviews
    path('ticket/<int:ticket_id>/review/create/', views.review_create, name='review_create'),
    path('review/create/', views.create_ticket_and_review, name='create_ticket_and_review'),
    path('review/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    
    # URLs des abonnements
    path('subscriptions/', views.subscription_page, name='subscriptions'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),

    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),

]