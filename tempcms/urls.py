from django.conf.urls import url
from .import views

urlpatterns = [
	#urls for subsection create/edit
	url(r'^(?P<chap_slug>[\w-]+)/subtopic/(?P<subt_pk>\d+)/subsection/create/$', views.tempsubsection_create, name='subsection_create'),
	url(r'^(?P<chap_slug>[\w-]+)/subtopic/(?P<subt_pk>\d+)/subsection/(?P<subsec_pk>\d+)/edit/$', views.tempsubsection_edit, name='subsection_edit'),
	
	#urls for saq create/edit
	url(r'^(?P<chap_slug>[\w-]+)/saq/create$', views.tempsaq_create, name='saq_create'),
	url(r'^(?P<chap_slug>[\w-]+)/saq/(?P<saq_pk>\d+)/edit$', views.tempsaq_edit, name='saq_edit'),
	
	#urls for numerical create/edit
	url(r'^(?P<chap_slug>[\w-]+)/numerical/create$', views.tempnumerical_create, name='numerical_create'),
	url(r'^(?P<chap_slug>[\w-]+)/numerical/(?P<num_pk>\d+)/edit$', views.tempnumerical_edit, name='numerical_edit'),
	
	#urls for subsection image create/edit
	url(r'^(?P<chap_slug>[\w-]+)/subtopic/(?P<subt_pk>\d+)/subsection_image/create/$', views.tempsubsectionimage_create, name='subsection_image_create'),
	url(r'^(?P<chap_slug>[\w-]+)/subtopic/(?P<subt_pk>\d+)/subsection_image/(?P<subsecimg_pk>\d+)/edit/$', views.tempsubsectionimage_edit, name='subsection_image_edit'),

	#url to view items pending for approval
	url(r'^pending/subsections$', views.pending_subsections, name = 'pending_subsections'),
	url(r'^pending/saqs$', views.pending_saqs, name = 'pending_saqs'),
	url(r'^pending/numericals$', views.pending_numericals, name = 'pending_numericals' ),
	url(r'^pending/subsection_images$', views.pending_subsection_images, name = 'pending_subsection_images'),

	#urls to approve pending contents
	url(r'^pending/subsections/(?P<tempsubsec_pk>\d+)/approve$', views.approve_subsection, name = "approve_subsection"),
	url(r'^pending/numericals/(?P<tempnum_pk>\d+)/approve$', views.approve_numerical, name = "approve_numerical"),
	url(r'^pending/saqs/(?P<tempsaq_pk>\d+)/approve$', views.approve_saq, name = "approve_saq"),
	url(r'^pending/subsection_images/(?P<tempsubsecimg_pk>\d+)/approve$', views.approve_subsection_image, name = "approve_subsection_image"),
]