from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from qiniu import Auth
from qiniu import BucketManager

q = Auth(settings.QINIU['accessKey'], settings.QINIU['secretKey'])
bucket = BucketManager(q)
bucket_name = 'zjulibrary'


def fileList(request, prefix):
    ret, eof, info = bucket.list(bucket=bucket_name, prefix=prefix, marker=None, delimiter='/')
    print(ret)
    # print(info)
    dirs=[]
    if 'commonPrefixes' in ret:
        for commonPrefix in ret['commonPrefixes']:
            dirs.append({
                'wholePath': commonPrefix,
                'displayName': commonPrefix.replace(prefix,'',1)
            })
    files = ret['items'] if 'items' in ret else []
    print(dirs)
    print(files)
    crumbs=[]
    tempPrefix=''
    for p in prefix.split('/')[0:-1]:
        tempPrefix+=p+'/'
        crumbs.append({
            'prefix': tempPrefix,
            'name': p
        })
    return render(request, 'disk/fileList.html',{
        'crumbs': crumbs,
        'prefix': prefix,
        'dirs': dirs,
        'files': files
    })