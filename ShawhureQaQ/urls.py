from django.conf.urls import include, url
from django.contrib import admin
from qaq.views import*

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$',homepage),
	url(r'^topic/',topic),
	url(r'^find/',find),
	url(r'^info/',info),
	url(r'^myhome/',myhome),
	url(r'^editUser/',editUser),
	url(r'^edit_detail/',edit_detail),
	url(r'^search/',search),
	url(r'^ask/',ask),
	url(r'^gethint.asp/$', ajax),
	url(r'^indexhint.asp/$', ajax_index),
	url(r'^login/',login),
	url(r'^register/',register),
	url(r'^registerDetail/',registerDetail),
	url(r'^loginDetail/',loginDetail),
	url(r'^add_question/',add_question),
	url(r'^add_answer/',add_answer),	
	url(r'^answer_question/',answer_question),
	url(r'^tag/',tag_details),
	url(r'^logout/',logout),
	url(r'^otherhome/',other_home),
	url(r'^follow_user/',follow_user),
	url(r'^cancel_follow/',cancel_follow),
	url(r'^contact_user/',contact_user),
]
