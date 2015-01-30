from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vrautotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^superuser', 'vrapp.views.superuser', name='superuser'),
    url(r'^$', 'vrapp.views.home', name='home'),
    url(r'^checkContestName', 'vrapp.views.checkContestName', name='checkContestName'),
    url(r'^checkUserName', 'vrapp.views.checkUserName', name='checkUserName'),
    url(r'^addContest', 'vrapp.views.addContest', name='addContest'),
    url(r'^deleteContest', 'vrapp.views.deleteContest', name='deleteContest'),
    url(r'^loginvalidate', 'vrapp.views.loginvalidate', name='loginvalidate'),
    url(r'^regisuccess', 'vrapp.views.regisuccess', name='regisuccess'),
    url(r'^registration', 'vrapp.views.registration', name='registration'),
    url(r'^loginform', 'vrapp.views.loginform', name='loginform'),
    url(r'^contestanthome', 'vrapp.views.contestanthome', name='contestanthome'),
    url(r'^testadminhome', 'vrapp.views.testadminhome', name='testadminhome'),
    url(r'^testcreatorhome', 'vrapp.views.testcreatorhome', name='testcreatorhome'),
    url(r'^participantapproverhome', 'vrapp.views.participantapproverhome', name='participantapproverhome'),
    url(r'^puppet', 'vrapp.views.puppet', name='puppet'),
    url(r'^stop', 'vrapp.views.stop', name='stop'),
    url(r'^admin/', include(admin.site.urls)),
)
