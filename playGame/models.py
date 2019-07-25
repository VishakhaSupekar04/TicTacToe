from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

#This is a list of choices and appears as a drop down on the html page
from django.db.models import Q

BOARD_SIZE=3

Game_Status_choices =(('F',"First Player move"),
                      ('S',"Second Player move"),
                      ('W',"First Player wins"),
                      ('w',"Second Player wins"),
                      ('D',"Draw"))

# Create your models here.


class GamesQuerySet(models.QuerySet):
    def games_for_user(self,user):
        # Q() | Q() is used for or condition
        return self.filter(Q(first_player=user) | Q(second_player=user))

    def active_games(self):

        return self.filter(Q(game_status='F') | Q(game_status='S'))


class Game(models.Model):
    first_player = models.ForeignKey(User,related_name="first_player",on_delete=models.CASCADE)
    second_player = models.ForeignKey(User, related_name="second_player",on_delete=models.CASCADE)

    game_start_time =models.DateTimeField(auto_now_add=True)
    game_last_active = models.DateTimeField(auto_now=True)
    game_status = models.CharField(max_length=1,default='F',choices=Game_Status_choices)

    objects = GamesQuerySet.as_manager()


    def board(self):
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def is_users_move(self, user):
        return (user == self.first_player and self.game_status == 'F') or \
               (user == self.second_player and self.game_status == 'S')

    def new_move(self):
        """Returns a new move object with player, game, and count preset"""
        if self.game_status not in 'FS':
            raise ValueError("Cannot make move on finished game")

        return Move(
            game=self,
            by_first_player=self.game_status == 'F'
        )

    def update_after_move(self, move):
        """Update the status of the game, given the last move."""
        self.game_status = self._get_game_status_after_move(move)

    def _get_game_status_after_move(self, move):
        x, y = move.x, move.y
        board = self.board()
        if (move == board[y][0] == board[y][1] == board[y][2]) or \
                (move == board[0][x] == board[1][x] == board[2][x]) or \
                (move == board[0][0] == board[1][1] == board[2][2]) or \
                (move == board[0][2] == board[1][1] == board[2][0]):
            return "W" if move.by_first_player else "L"
        if self.move_set.count() >= BOARD_SIZE ** 2:
            return 'D'
        return 'S' if self.game_status == 'F' else 'F'

    def get_absolute_url(self):
        return reverse('gameplay_detail',args=[self.id])

    def __str__(self):
        return "{0} vs {1}".format(self.first_player,self.second_player)


class Move(models.Model):
    x = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE - 1)]
    )
    y = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE - 1)]
    )
    comment = models.CharField(max_length=300, blank=True)
    game = models.ForeignKey(Game, editable=False, on_delete=models.CASCADE)
    by_first_player = models.BooleanField(editable=False)

    def __eq__(self, other):
        if other is None:
            return False
        return other.by_first_player == self.by_first_player

    def save(self, *args, **kwargs):
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        self.game.save()

