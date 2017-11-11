from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$',views.fileList),
    url(r'^file/list/(?P<prefix>.*)$',views.fileList),
    url(r'^file/download/(?P<key>.+)/$',views.fileDownload),
]
