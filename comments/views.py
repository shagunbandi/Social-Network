from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from .models import Comment


# COMMENT UPDATE AND CREATE IN POST DETAIL FUNCTION IN POST PACKAGE

# TODO On Post delete Comment should also be deleted
@login_required(login_url='accounts:login')
def comment_delete(request, pk=None, slug=None):
    instance = get_object_or_404(Comment, pk=pk)
    if not (request.user == instance.user or request.user == instance.content_object.user):
        response = HttpResponse('You are not authorized to make changes to the post')
        response.status_code = 403
        return response
    instance.delete()
    return HttpResponseRedirect(instance.content_object.get_absolute_url())


# TODO Update Comment
@login_required(login_url='account:login')
def comment_update(request, pk=None):
    pass