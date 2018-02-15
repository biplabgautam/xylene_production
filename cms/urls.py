from django.conf.urls import url
from .import views

urlpatterns = [
	#Urls for forms
	url(r'^subject/create/$', views.subject_create, name='subject_create'),
	url(r'^subject/(?P<sub_pk>\d+)/edit$', views.subject_edit, name='subject_edit'),
	url(r'^(?P<sub_slug>[\w-]+)/chapter/create/$', views.chapter_create, name='chapter_create'),
	url(r'^(?P<chap_slug>[\w-]+)/edit$', views.chapter_edit, name='chapter_edit'),
	url(r'^(?P<chap_slug>[\w-]+)/subtopic/create/$', views.subtopic_create, name='subtopic_create'),
	url(r'^(?P<chap_slug>[\w-]+)/subtopic/(?P<subt_pk>\d+)/edit$', views.subtopic_edit, name='subtopic_edit'),

	#url for selection and listing
	url(r'^subjects/$', views.subject_list, name='subject_list'),
	url(r'^subject_select/(?P<sub_pk>\d+)/$', views.subject_select, name='subject_select'),
	url(r'^(?P<chap_slug>[\w-]+)/select/$', views.chapter_select, name='chapter_select'),
	url(r'^(?P<chap_slug>[\w-]+)/saq_list/$', views.saq_list, name='saq_list'),
	url(r'^(?P<chap_slug>[\w-]+)/numerical_list/$', views.numerical_list, name='numerical_list'),
	url(r'^(?P<chap_slug>[\w-]+)/saq/(?P<saq_pk>[\w-]+)/$', views.saq_select, name='saq_select'),
	url(r'^(?P<chap_slug>[\w-]+)/numerical/(?P<num_pk>[\w-]+)/$', views.numerical_select, name='numerical_select'),
	url(r'^(?P<chap_slug>[\w-]+)/(?P<subt_slug>[\w-]+)/$', views.subtopic_select, name='subtopic_select'),

]
