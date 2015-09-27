from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vrautotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    #--------------SuperUser------------#
    
    url(r'^superuser', 'vrapp.views.superuser', name='superuser'),
    url(r'^addContest', 'vrapp.views.addContest', name='addContest'),
    url(r'^deleteContest', 'vrapp.views.deleteContest', name='deleteContest'),
    url(r'^checkContestName', 'vrapp.views.checkContestName', name='checkContestName'),

	#------------Home---------------#
	
    url(r'^$', 'vrapp.views.home', name='home'),
    url(r'^registration', 'vrapp.views.registration', name='registration'),
    url(r'^checkUserName', 'vrapp.views.checkUserName', name='checkUserName'),
    url(r'^regisuccess', 'vrapp.views.regisuccess', name='regisuccess'),

	#---------Login----------#
	
    url(r'^loginform', 'vrapp.views.loginform', name='loginform'),
    url(r'^loginvalidate', 'vrapp.views.loginvalidate', name='loginvalidate'),
	#------------Contestant Home------------#

    url(r'^contestanthome', 'vrapp.views.contestanthome', name='contestanthome'),
    #url(r'^submissions', 'vrapp.views.submissions', name='submissions'),

	#------------TestAdmin Home------------#
   
    url(r'^testadminhome', 'vrapp.views.testadminhome', name='testadminhome'),
    url(r'^puppetrun', 'vrapp.views.puppetrun', name='puppetrun'),
    url(r'^puppetstop', 'vrapp.views.puppetstop', name='puppetstop'),
    url(r'^deactivateuser', 'vrapp.views.deactivateuser', name='deactivateuser'),
    
	#------------TestCreator Home------------#

    url(r'^testcreatorhome$', 'vrapp.views.testcreatorhome', name='testcreatorhome'),
    url(r'^createquestionpaper', 'vrapp.views.createquestionpaper', name='createquestionpaper'),

	#------------ParticipantApprover Home------------#

    url(r'^participantapproverhome', 'vrapp.views.participantapproverhome', name='participantapproverhome'),
    url(r'^approve', 'vrapp.views.approve', name='approve'),
    url(r'^admin/', include(admin.site.urls)),    
)
