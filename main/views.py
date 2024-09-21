from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Student,FriendRequest, Friendship
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid credentials or user doesn't exist."
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create a Student instance
            student = Student(
                user=user,
                registration_no=form.cleaned_data['registration_no'],
                branch=form.cleaned_data['branch'],
                enrollment_year=form.cleaned_data['enrollment_year']  # If you're collecting this
            )
            student.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def dashboard_view(request):
    student = Student.objects.get(user=request.user)
    context = {
        'user': request.user,
        'registration_no': student.registration_no,
        'branch': student.branch,
    }
    return render(request, 'dashboard.html', context)

def leaderboard_view(request):
    return render(request, 'leaderboard.html')

@login_required
def friends_view(request):
    profile = request.user.profile
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    friends = profile.friends.all()

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'friends': friends,
        'user': request.user,
    }
    return render(request, 'friends.html', context)


@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if request.user != to_user:
        Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
    return HttpResponseRedirect(reverse('friends'))

@login_required
def accept_friend_request(request, request_id):
    friendship = get_object_or_404(Friendship, id=request_id)
    if friendship.to_user == request.user:
        friendship.to_user.profile.friends.add(friendship.from_user)
        friendship.from_user.profile.friends.add(friendship.to_user)
        friendship.delete()  # Remove the request after acceptance
    return HttpResponseRedirect(reverse('friends'))

@login_required
def decline_friend_request(request, request_id):
    friendship = get_object_or_404(Friendship, id=request_id)
    if friendship.to_user == request.user:
        friendship.delete()  # Simply delete the request
    return HttpResponseRedirect(reverse('friends'))
