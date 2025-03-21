from django.contrib import admin
from .models import Community, Membership, Post, Comment

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('title', 'author', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at', 'member_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MembershipInline, PostInline]

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'community', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__username', 'community__name')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'community', 'created_at')
    list_filter = ('community', 'created_at')
    search_fields = ('title', 'content', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title') 