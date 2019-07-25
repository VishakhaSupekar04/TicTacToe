from django.shortcuts import render,redirect,get_object_or_404
from playGame.models import Game
from django.contrib.auth.decorators import login_required
from .forms import InvitationForm
from .models import Invitation
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.


@login_required  # this decorator makes sure that the page is viewed only after user is logged in
def home(request):

    my_games = Game.objects.games_for_user(request.user)
    # get the list of all active games
    active_games = my_games.active_games()
    finished_games = my_games.difference(active_games)
    # get the list of all invitations received
    invitations =request.user.invitations_received.all()
    return render(request, "player/home.html", {'active_games': active_games, 'invitations': invitations,
                                                'finished_games': finished_games})

    # #find all game of user when user played as player one. The result is a list of games
    # game_first_player = Game.objects.filter(
    #     first_player= request.user,
    #     game_status = 'F'
    # )
    # # find all game of user when user played as player two. The result is a list of games
    # game_second_player = Game.objects.filter(
    #     second_player=request.user,
    #     game_status='S'
    # )
    # #concatinate both the lists into one
    # all_my_games = list(game_first_player) + \
    #                list(game_second_player)
    # # 'games' is the vairable which conatins the result and is passed to the template
    # return render(request, "player/home.html", {'games': all_my_games})


@login_required
def new_invite(request):
    if request.method=="POST":
        invitation = Invitation(from_user=request.user)
        # to validate if the data entered is correct, generate a new form with the entered data as argument
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request,"player/new_invite.html",{'form': form})


@login_required
def accept_invite(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == "POST":
        if "accept" in request.POST:
            game = Game.objects.create(
                first_player = invitation.to_user,
                second_player = invitation.from_user,
            )
        invitation.delete()
        return redirect(game)
    else:
        return render(request,
                      "player/accept_invite.html",
                       {'invitation': invitation})

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "player/signup_form.html"
    success_url = reverse_lazy('player_home')