from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm2
from .models import Post
from django.contrib.auth.models import User


def posts_home(request):
    posts = Post.objects.all().order_by('-created_at')
    selected_user = request.GET.get("user")
    users = User.objects.all()
    if selected_user:
        posts = posts.filter(user__username=selected_user)
    if request.method == 'POST':
         if "delete_post" in request.POST:  # If the delete button was pressed
            post_id = request.POST.get("delete_post")
            post = get_object_or_404(Post, id=post_id)

            # Ensure only the owner can delete
            if post.user == request.user:
                post.delete()
            return redirect("home")
         form = PostForm2(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the current logged-in user as the post owner
            post.save()
            return redirect("posts_home")
             
    else:
     form = PostForm2()
     
    return render(request,'posts/posts_home.html', {"form":form,"posts":posts,"users": users, "selected_user": selected_user})