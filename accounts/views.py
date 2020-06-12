from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserLoginForm, UserRegistrationForm, User
from posts.models import Post
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


#
# USER
#
def login_view(request):
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("posts:index")
    title = "Login"
    context = {
        'form': form,
        'title': title
    }
    return render(request, "accounts/forms.html", context)


def logout_view(request):
    logout(request)
    return redirect("posts:index")


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    next = request.GET.get('next')
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("posts:index")
    title = "Register"
    context = {
        'form': form,
        'title': title
    }
    return render(request, "accounts/forms.html", context)


def search_username(request):
    queryset_list = User.objects.all().order_by('username')
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(username__icontains=query)

    context = {
        "title": "Friends",
        "query": queryset_list
    }
    print('hey')
    return render(request, "accounts/friendSearch.html", context)


#
# Friend Requests
#
def send_request(request, username=None):
    if not request.user.is_authenticated or not request.user.username != username:
        return HttpResponse('Cannot send Request')
    friend = get_object_or_404(User, username=username)

    # Update User
    user = request.user
    user_profile = user.userprofile

    if friend in user_profile.friends_list.all():
        return HttpResponse('Cannot send Request')
    user_profile.friend_request_sent.add(friend)

    # Update Friend
    friend_profile = friend.userprofile
    friend_profile.friend_request_received.add(user)
    return redirect(reverse('accounts:profile', kwargs={'username': username}))


def cancel_sent_request(request, username=None):
    if not request.user.is_authenticated or not request.user.username != username:
        return HttpResponse('Cannot send Request')
    friend = get_object_or_404(User, username=username)

    # Update User
    user = request.user
    user_profile = user.userprofile
    if friend in user_profile.friends_list.all():
        return HttpResponse('Cannot cancel Request User already in your friend list')

    if friend in user_profile.friend_request_sent.all():
        user_profile.friend_request_sent.remove(friend)

    # Update Friend
    friend_profile = friend.userprofile
    if user in friend_profile.friend_request_received.all():
        friend_profile.friend_request_received.remove(user)
    return redirect(reverse('accounts:profile', kwargs={'username': user.username}))


def decline_request(request, username=None):
    if not request.user.is_authenticated or not request.user.username != username:
        return HttpResponse('Cannot send Request')
    friend = get_object_or_404(User, username=username)

    # Update User
    user = request.user
    user_profile = user.userprofile

    if friend in user_profile.friends_list.all():
        return HttpResponse('Cannot decline request, already in your friend list')

    if friend in user_profile.friend_request_received.all():
        user_profile.friend_request_received.remove(friend)

    # Update Friend
    friend_profile = friend.userprofile
    if user in friend_profile.friend_request_sent.all():
        friend_profile.friend_request_sent.remove(user)
    return redirect(reverse('accounts:profile', kwargs={'username': user.username}))


def accept_request(request, username=None):
    if not request.user.is_authenticated or not request.user.username != username:
        return HttpResponse('Cannot send Request')
    friend = get_object_or_404(User, username=username)
    user = request.user
    friend_profile = friend.userprofile
    user_profile = user.userprofile

    if friend in user_profile.friends_list.all():
        return HttpResponse('Already in your friend list')

    if user in friend_profile.friend_request_sent.all():
        user_profile.friends_list.add(friend)
        friend_profile.friends_list.add(user)

        user_profile.friend_request_received.remove(friend)
        friend_profile.friend_request_sent.remove(user)
    else:
        return HttpResponse('Request not received fom that user')

    return redirect(reverse('accounts:profile', kwargs={'username': user}))


def unfriend(request, username=None):
    if not request.user.is_authenticated or not request.user.username != username:
        return HttpResponse('Cannot unfriend')
    friend = get_object_or_404(User, username=username)
    user = request.user
    friend_profile = friend.userprofile
    user_profile = user.userprofile

    if friend not in user_profile.friends_list.all():
        return HttpResponse('Not a friend')

    user_profile.friends_list.remove(friend)
    friend_profile.friends_list.remove(user)

    return redirect(reverse('accounts:profile', kwargs={'username': user}))


#
# Profile
#
def get_user_instance(request, username):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    instance = get_object_or_404(User, username=username)
    return instance


def get_user_profile(request, username):
    instance = get_user_instance(request, username)
    user_profile = instance.userprofile
    return user_profile


@login_required(login_url='accounts:login')
def friend_list(request, username=None):
    if request.user.username != username:
        return HttpResponse('You are not allowed to delete the post')
    user_profile = get_user_profile(request, username)
    friend_list = user_profile.friends_list.all()

    context = {
        'title': username,
        'friend_list': friend_list,
        'username': username
    }
    return render(request, 'accounts/profile/friend_list.html', context)


@login_required(login_url='accounts:login')
def friend_requests(request, username=None):
    if request.user.username != username:
        return HttpResponse('You are not allowed to delete the post')
    user_profile = get_user_profile(request, username)
    friend_request_sent = user_profile.friend_request_sent.all()
    friend_request_received = user_profile.friend_request_received.all()

    context = {
        'title': username,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received
    }
    return render(request, 'accounts/profile/friend_request.html', context)


@login_required(login_url='accounts:login')
def user_posts(request, username=None):
    instance = get_user_instance(request, username)
    posts = Post.objects.filter(user=instance)

    context = {
        'title': username,
        'posts': posts,
    }
    return render(request, 'accounts/profile/user_posts.html', context)


@login_required(login_url='accounts:login')
def user_comments(request, username=None):
    instance = get_user_instance(request, username)
    comments = Comment.objects.filter(user=instance)
    comments_segregated = {}
    for comment in comments:
        if comment.content_object in comments_segregated.keys():
            comments_segregated[comment.content_object].append(comment)
        else:
            comments_segregated[comment.content_object] = [comment]
    comments_profile = []
    for keys in comments_segregated:
        comments_profile.append({
            'key': keys,
            'value': comments_segregated[keys]
        })
    print(comments_profile)

    context = {
        'title': username,
        'comments': comments_profile,
    }
    return render(request, 'accounts/profile/user_comments.html', context)


@login_required(login_url='accounts:login')
def liked_posts(request, username=None):
    instance = get_user_instance(request, username)
    liked_posts = Post.objects.all().filter(upvotes=instance)

    context = {
        'title': username,
        'liked_posts': liked_posts,
    }
    return render(request, 'accounts/profile/liked_posts.html', context)


@login_required(login_url='accounts:login')
def profile(request, username=None):
    instance = get_user_instance(request, username)

    context = {
        'title': username,
        'instance': instance,
    }
    return render(request, 'accounts/profile/main.html', context)


@login_required(login_url='accounts:login')
def profile_complete(request, username=None):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    instance = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=instance)
    liked_posts = Post.objects.all().filter(upvotes=instance)
    user_profile = instance.userprofile
    friend_list = user_profile.friends_list.all()
    friend_request_sent = user_profile.friend_request_sent.all()
    friend_request_received = user_profile.friend_request_received.all()

    # TODO Keep all comments with same post together
    comments = Comment.objects.filter(user=instance)
    comments_segregated = {}
    for comment in comments:
        if comment.content_object in comments_segregated.keys():
            comments_segregated[comment.content_object].append(comment)
        else:
            comments_segregated[comment.content_object] = [comment]
    comments_profile = []
    for keys in comments_segregated:
        comments_profile.append({
            'key': keys,
            'value': comments_segregated[keys]
        })
    print(comments_profile)
    context = {
        'title': instance.username,
        'instance': instance,
        'posts': posts,
        'comments': comments_profile,
        'liked_posts': liked_posts,
        'friend_list': friend_list,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received
    }
    return render(request, "accounts/profile.html", context)
