from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from qiniu import Auth
from qiniu import BucketManager

q = Auth(settings.QINIU['accessKey'], settings.QINIU['secretKey'])
bucket = BucketManager(q)
bucket_name = 'zjulibrary'


def test(request):
    # ret, eof, info = bucket.list(bucket=bucket_name, prefix='assets/', marker=None, delimiter='/')
    # print(ret)
    # # print(info)
    # dirs = ret['commonPrefixes'] if 'commonPrefixes' in ret else []
    # files = ret['items'] if 'items' in ret else []
    # print(dirs)
    # print(files)
    return render(request,'disk/list.html')