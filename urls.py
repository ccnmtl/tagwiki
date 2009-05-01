from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       # Example:
                       # (r'^tagwiki/', include('tagwiki.foo.urls')),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include('survey.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),

                       (r'^page/(?P<slug>[^/]+)/add_tags/','demo.views.add_tags'),
                       (r'^page/(?P<slug>[^/]+)/','demo.views.page'),

                       (r'^tag/(?P<name>[^/]+)/','demo.views.tag'),

                       (r'^user/(?P<username>[^/]+)/','demo.views.user'),
                       

)
