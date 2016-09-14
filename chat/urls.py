from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^chat/$', views.chat, name="chat"),
	url(r'^dialogs/$', views.dialogs, name="dialogs"),
	url(r'^search/$', views.search, name="search"),
	url(r'^send_message/$', views.send_message, name="send_message"),
	url(r'^messages/$', views.messages, name="messages"),
	url(r'^login/$', views.login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),
]
