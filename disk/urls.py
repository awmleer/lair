from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.fileList),
    url(r'^file/list/(?P<prefix>.*)$',views.fileList),
    url(r'^file/upload/(?P<prefix>.*)$',views.fileUpload),
    url(r'^file/uploadToken/$',views.uploadToken),
    url(r'^file/rename/(?P<key>.+)/$',views.fileRename),
    url(r'^file/download/(?P<key>.+)/$',views.fileDownload),
]
