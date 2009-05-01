# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from datetime import datetime
from django.template.defaultfilters import slugify
import simplejson
from models import *
from forms import *

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

@rendered_with('demo/page.html')
def page(request,slug):
    page = get_object_or_404(Page,slug=slug)
    return dict(page=page,
                add_tags_form=AddTagsForm())

def add_tags(request,slug):
    tags = request.POST['tags']
    page = get_object_or_404(Page,slug=slug)
    try:
        pu = PageUser.objects.get(page=page,user=request.user)
    except PageUser.DoesNotExist:
        pu = PageUser.objects.create(page=page,user=request.user)
    pu.set_tags(tags)
    return HttpResponseRedirect(page.get_absolute_url())

@rendered_with('demo/tag.html')
def tag(request,name):
    tag = get_object_or_404(Tag,name=name)
    return dict(tag=tag)

@rendered_with('demo/user.html')
def user(request,username):
    user = get_object_or_404(User,username=username)
    # can't think of a better way
    pus = PageUser.objects.filter(user=user)
    return dict(user=user,pus=pus)
        
