from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, FollowersCount, LikePost
from django.contrib.auth import authenticate, login as auth_login
from itertools import chain


@login_required(login_url='login')
def index(request):
    user_object = request.user
    user_profile = get_object_or_404(Profile, user=user_object)
    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        new_post = Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('index')  # Redirect to index after upload
    return render(request, 'upload.html')

@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        LikePost.objects.create(post=post, username=username)
        post.no_of_likes += 1
    else:
        like_filter.delete()
        post.no_of_likes -= 1
    post.save()
    return redirect('index')

@login_required(login_url='login')
def profile(request, username):
    user_object = get_object_or_404(User, username=username) 
    user_profile = get_object_or_404(Profile, user=user_object)  
    user_posts = Post.objects.filter(user=user_object)  
    user_post_length = user_posts.count() 

    follower = request.user.username

    # Determine follow/unfollow button text
    button_text = 'Unfollow' if FollowersCount.objects.filter(follower=follower, user=username).exists() else 'Follow'

    user_followers = FollowersCount.objects.filter(user=username).count()
    user_following = FollowersCount.objects.filter(follower=username).count()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def settings(request):
    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image', user_profile.profileimg)
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        auth.login(request, user)
        Profile.objects.create(user=user, id_user=user.id)
        return redirect('settings')

    return render(request, 'signup.html')
 

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/', username=user.username)  # Ensure username is passed
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
        
    return render(request, 'login.html')


@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        follower_record = FollowersCount.objects.filter(follower=follower, user=user).first()
        if follower_record:
            follower_record.delete()
        else:
            FollowersCount.objects.create(follower=follower, user=user)

        return redirect('profile', username=user)
    
    return redirect('index')
def search(request):
    return render(request,'search.html')


@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()  # Get username from the form

        # Filter users based on the search input
        username_object = User.objects.filter(username__icontains=username).first()

        if username_object:
            # Redirect to the specific user's profile
            return redirect('profile', username=username_object.username)
        else:
            messages.info(request, 'No users found.')

    return render(request, 'search.html', {
        'user_profile': user_profile,
    })
