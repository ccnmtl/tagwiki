from django.template import Library, Node, TemplateSyntaxError, Variable
from django.db.models import get_model
from django.db import connection
from django.template import resolve_variable
from tagging.models import Tag, TaggedItem
import sets 

register = Library()

class UserObjectTags(Node):
    def __init__(self, obj, user, variable):
        self.user = user
        self.obj = obj
        self.variable = variable

    def render(self, context):
        obj = resolve_variable(self.obj,context)
        user = resolve_variable(self.user,context)
        context[self.variable] = obj.get_user_tags(user)
        return ''

def get_user_tags(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise TemplateSyntaxError('get_user_tags tag takes exactly four arguments')
    if bits[3] != "as":
        raise TemplateSyntaxError("third argument must be 'as'")
    return UserObjectTags(bits[1], bits[2], bits[4])

get_user_tags = register.tag(get_user_tags)

class AllUserTags(Node):
    def __init__(self, user, model, variable):
        self.user = user
        self.model = model
        self.variable = variable

    def render(self, context):
        user = resolve_variable(self.user,context)
        model = get_model(*self.model.split('.'))
        alltags = sets.Set()
        for ui in model.objects.filter(user=user):
            for tag in ui.get_tags():
                alltags.add(tag)
        
        context[self.variable] = alltags
        return ''

def get_all_user_tags(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise TemplateSyntaxError('get_user_tags tag takes exactly four arguments')
    if bits[3] != "as":
        raise TemplateSyntaxError("third argument must be 'as'")
    return AllUserTags(bits[1], bits[2], bits[4])

get_all_user_tags = register.tag(get_all_user_tags)



class UserTaggedObjectsNode(Node):
    def __init__(self, tag, user, model, context_var):
        self.tag = Variable(tag)
        self.user = Variable(user)
        self.context_var = context_var
        self.model = model

    def render(self, context):
        user = self.user.resolve(context)
        model = get_model(*self.model.split('.'))
        if model is None:
            raise TemplateSyntaxError('user_tagged_objects tag was given an invalid model: %s' % self.model)
        if user is None:
            raise TemplateSyntaxError('user_tagged_objects tag was given an invalid user: %s' % self.user)
        context[self.context_var] = \
            [iu.get_item() for iu in TaggedItem.objects.get_by_model(model, self.tag.resolve(context)).filter(user=user)]
        return ''

def user_tagged_objects(parser,token):
    bits = token.contents.split()
    if len(bits) != 7:
        raise TemplateSyntaxError(_('%s tag requires exactly six arguments') % bits[0])
    if bits[3] != 'in':
        raise TemplateSyntaxError(_("third argument to %s tag must be 'in'") % bits[0])
    if bits[5] != 'as':
        raise TemplateSyntaxError(_("fifth argument to %s tag must be 'as'") % bits[0])
    return UserTaggedObjectsNode(bits[1], bits[2], bits[4], bits[6])

user_tagged_objects = register.tag(user_tagged_objects)
