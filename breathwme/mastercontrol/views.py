from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'mastercontrol/home.html')


from django.shortcuts import render
from musicapp.models import MusicTrack  # Import your MusicTrack model

from django.shortcuts import render
from musicapp.models import MusicTrack
from django.contrib.auth.decorators import login_required

def master_control(request):
    tracks = MusicTrack.objects.all()  # Get all songs
    return render(request, 'mastercontrol/master.html', {'tracks': tracks})


from .models import ChatRoom, Member
from django.contrib import messages
from django.shortcuts import render , redirect , get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, Member
from musicapp.models import MusicTrack

# View to create or join a chatroom
@login_required
def create_or_join_chatroom(request):
    if request.method == "POST":
        chatroom_name = request.POST.get("chatroom_name")
        action = request.POST.get("action")
        passcode = request.POST.get("passcode")
        
        if action == "create":
            # Create a new chatroom
            chatroom = ChatRoom.objects.create(name=chatroom_name, passcode=passcode, admin=request.user)
            Member.objects.create(user=request.user, chatroom=chatroom)
            messages.success(request, f"You've created a new chatroom: {chatroom_name}!")
            return redirect("mastercontrol:chatroom_detail", chatroom_name=chatroom_name)
        
        elif action == "join":
            # Join an existing chatroom
            try:
                chatroom = ChatRoom.objects.get(passcode=passcode)
            except ChatRoom.DoesNotExist:
                messages.error(request, "Invalid passcode. Please try again.")
                return redirect("mastercontrol:create_or_join_chatroom")
            
            if not Member.objects.filter(user=request.user, chatroom=chatroom).exists():
                Member.objects.create(user=request.user, chatroom=chatroom)
                messages.success(request, f"You've joined the chatroom: {chatroom.name}!")
                return redirect("mastercontrol:chatroom_detail", chatroom_name=chatroom.name)
            else:
                messages.error(request, "You are already a member of this chatroom.")
                return redirect("mastercontrol:create_or_join_chatroom")
    
    return render(request, "mastercontrol/create_or_join_chatroom.html")


@login_required
def chatroom_detail(request, chatroom_name):
    chatroom = get_object_or_404(ChatRoom, name=chatroom_name)
    members = Member.objects.filter(chatroom=chatroom)
    songs = MusicTrack.objects.all()  # Fetch all songs

    is_member = Member.objects.filter(user=request.user, chatroom=chatroom).exists()

    return render(request, "mastercontrol/chatroom_detail.html", {
        "chatroom": chatroom,
        "is_member": is_member,
        "members": members,
        "songs": songs,
    })

# Displaying all chatrooms 
from django.contrib.auth.decorators import login_required

@login_required
def user_chatrooms(request):
    # Fetch all chatrooms where the user is a member
    chatrooms = ChatRoom.objects.filter(member__user=request.user)
    
    return render(request, "mastercontrol/user_chatrooms.html", {
        "chatrooms": chatrooms,
    })
