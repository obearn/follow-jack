from django.conf.urls.defaults import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^facebook_django/', include('facebook_django.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
#     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^myeworld/$', 'facebook_django.myeworld.views.index'),
     (r'^myeworld/login', 'facebook_django.myeworld.views.login'),
     (r'^myeworld/logout', 'facebook_django.myeworld.views.logout'),
     (r'^myeworld/console', 'facebook_django.myeworld.views.console'),
     (r'^myeworld/facebook/(?P<user_id>\d+)/links', 'facebook_django.myeworld.views.user_links'),
     (r'^myeworld/statics/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': '/home/obearn/projets/facebook_django/resources/html/'}),
     (r'^myeworld/fql', 'facebook_django.myeworld.views.fql'),                  
)


