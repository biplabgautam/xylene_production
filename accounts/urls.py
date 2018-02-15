from django.conf.urls import url
from .import views

urlpatterns = [
#URL for pending contents of user
	url(r'^pending_content$', views.pending_content, name="pending_content"),
#urls to allow user to view and edit only his submitted contents 
	url(r'^pending_content/subsection/(?P<tempsubsec_pk>\d+)$', views.see_tempsubsection, name="see_tempsubsection"),
	url(r'^pending_content/saq/(?P<tempsaq_pk>\d+)$', views.see_tempsaq, name="see_tempsaq"),
	url(r'^pending_content/numerical/(?P<tempnum_pk>\d+)$', views.see_tempnumerical, name="see_tempnumerical"),
	url(r'^pending_content/subsection_image/(?P<tempsubsecimg_pk>\d+)$', views.see_tempsubsection_image, name="see_tempsubsection_image"),
]