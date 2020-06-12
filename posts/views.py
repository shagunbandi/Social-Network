from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Imports from posts
from .models import Post
from .forms import PostForm

# Imports from comments
from comments.models import Comment
from comments.forms import CommentForm


# Search, List Posts
def posts_list(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        ).distinct()

    context = {
        'object_list': queryset,
        'title': 'List'
    }
    return render(request, 'posts/index.html', context)


@login_required(login_url='accounts:login')
def posts_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    title = "New Post"
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'posts/create.html', context)


def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id
    }

    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        if request.user.is_authenticated:
            user = request.user
            c_type = comment_form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            object_id = comment_form.cleaned_data.get("object_id")
            content = comment_form.cleaned_data.get("content")

            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=object_id,
                content=content,
                parent=parent_obj,
            )
            if created:
                return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
            else:
                return HttpResponse('Could not create. Please contact +91 9932538111 about the issue')
        else:
            return HttpResponse('Login in to comments on a post')

    comments = instance.comments

    has_upvoted = instance.has_upvoted(user=request.user)

    context = {
        'title': instance.title,
        'instance': instance,
        'comments': comments,
        'comment_form': comment_form,
        'has_upvoted': has_upvoted
    }
    return render(request, 'posts/details.html', context)


@login_required(login_url='accounts:login')
def posts_update(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    if request.user != instance.user:
        return HttpResponse('You are not authorized to make changes to the post')

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'instance': instance,
        'form': form,
        'title': instance.title,
    }
    return render(request, 'posts/create.html', context)


@login_required(login_url='accounts:login')
def posts_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.user != request.user:
        return HttpResponse('You are not allowed to delete the post')
    comments = Comment.objects.filter(object_id=instance.id)
    comments.delete()
    instance.delete()
    return redirect('posts:index')


class PostVoteToggleRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        pk = self.kwargs.get('pk')

        # For Voting Post, pk is not passed thus will be none and for Comment pk is not None
        if pk is None:
            obj = get_object_or_404(Post, slug=slug)
            url_ = obj.get_absolute_url()
        else:
            obj = get_object_or_404(Comment, pk=pk)
            url_ = obj.content_object.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.upvotes.all():
                obj.upvotes.remove(user)
            else:
                obj.upvotes.add(user)
        return url_


class PostApiVoteToggleRedirect(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, pk=None, format=None):
        if pk is None:
            obj = get_object_or_404(Post, slug=slug)
        else:
            obj = get_object_or_404(Comment, pk=pk)

        user = self.request.user
        response = {
            'upvote': False,
            'updates': False
        }
        if user.is_authenticated:
            # TODO Optimize
            if user in obj.upvotes.all():
                obj.upvotes.remove(user)
                response['upvote'] = False
            else:
                obj.upvotes.add(user)
                response['upvote'] = True
            response['updates'] = True
        return Response(response)
