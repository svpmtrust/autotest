from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vrautotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^superuser', 'vrapp.views.superuser', name='superuser'),
    url(r'^home', 'vrapp.views.home', name='home'),
    url(r'^registration', 'vrapp.views.registration', name='registration'),
    url(r'^loginform', 'vrapp.views.loginform', name='loginform'),
    url(r'^contestanthome', 'vrapp.views.contestanthome', name='contestanthome'),
    url(r'^testadminhome', 'vrapp.views.testadminhome', name='testadminhome'),
    url(r'^testcreatorhome', 'vrapp.views.testcreatorhome', name='testcreatorhome'),
    url(r'^participantapproverhome', 'vrapp.views.participantapproverhome', name='participantapproverhome'),
    url(r'^pup', 'vrapp.views.pup', name='pup'),
    url(r'^admin/', include(admin.site.urls)),
)
