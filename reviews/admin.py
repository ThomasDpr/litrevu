from django.contrib import admin

from .models import Review, Ticket, UserBlocks, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    list_filter = ('user', 'time_created')
    search_fields = ('title', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'ticket', 'user', 'rating', 'time_created')
    list_filter = ('user', 'rating', 'time_created')
    search_fields = ('headline', 'body')


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    list_filter = ('user', 'followed_user')


admin.site.register(UserBlocks)
