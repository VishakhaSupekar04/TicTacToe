from django.contrib import admin

from .models import Move, Game

# Register your models here.


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id','first_player','second_player','game_status')
    list_editable = ('game_status',)


#admin.site.register(Move)

