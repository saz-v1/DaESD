from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm2
from .models import Post,Notification
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@login_required
def posts_home(request):
    posts = Post.objects.all().order_by('-created_at')
    selected_user = request.GET.get("user")
    users = User.objects.all()
    all_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    notifications = all_notifications[:10]  # Slice after filtering
    unread_count = all_notifications.filter(read=False).count()
    if selected_user:
        posts = posts.filter(user__username=selected_user)
    if request.method == 'POST':
         form = PostForm2(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the current logged-in user as the post owner
            post.save()

    # Create a notification for all users (except the post author)
            for user in User.objects.exclude(id=request.user.id):
                 Notification.objects.create(
                    user=user,
                    message=f"{request.user.username} created a new post."
                )
            return redirect("home")
             
    else:
     form = PostForm2()
     
    return render(request,'posts/posts_home.html', {"form":form,"posts":posts,"users": users, "selected_user": selected_user,"notifications": notifications,
    "unread_count": unread_count})

@require_POST
@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    return JsonResponse({"status": "success"})

@login_required
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    
    if content:
        # Create the comment
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # Create notification for post author
        if post.user != request.user:
            Notification.objects.create(
                user=post.user,
                message=f"{request.user.username} commented on your post."
            )
        
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Comment cannot be empty.')
    
    return redirect('home')
