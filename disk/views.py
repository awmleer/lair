from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from qiniu import Auth
from qiniu import BucketManager

q = Auth(settings.QINIU['accessKey'], settings.QINIU['secretKey'])
bucket = BucketManager(q)
bucketName = 'lair-test'
bucketDomain = 'oz52zraao.bkt.clouddn.com'


def fileList(request, prefix):
    ret, eof, info = bucket.list(bucket=bucketName, prefix=prefix, marker=None, delimiter='/')
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
    crumbs=[{
        'prefix': '',
        'name': '/'
    }]
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


def fileUpload(request, prefix):
    return render(request, 'disk/fileUpload.html', {
        'prefix': prefix
    })


def fileDownload(request, key):
    baseUrl = 'http://%s/%s' % (bucketDomain, key)
    privateUrl = q.private_download_url(baseUrl, expires=3600)
    return HttpResponseRedirect(redirect_to=privateUrl)

