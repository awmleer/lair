from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from qiniu import Auth
from qiniu import BucketManager

q = Auth(settings.QINIU['accessKey'], settings.QINIU['secretKey'])
bucket = BucketManager(q)


@require_http_methods(['GET'])
def fileList(request, prefix):
    ret, eof, info = bucket.list(bucket=settings.QINIU['bucketName'], prefix=prefix, marker=None, delimiter='/')
    # print(ret)
    # print(info)
    dirs=[]
    if 'commonPrefixes' in ret:
        for commonPrefix in ret['commonPrefixes']:
            dirs.append({
                'wholePath': commonPrefix,
                'displayName': commonPrefix.replace(prefix,'',1)
            })
    files = ret['items'] if 'items' in ret else []
    # print(dirs)
    # print(files)
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


@require_http_methods(['GET'])
def fileUpload(request, prefix):
    return render(request, 'disk/fileUpload.html', {
        'prefix': prefix,
        'bucketDomain': settings.QINIU['bucketDomain']
    })


@require_http_methods(['GET'])
def uploadToken(request):
    upToken = q.upload_token(bucket=settings.QINIU['bucketName'], expires=3600)
    return JsonResponse({
        'uptoken': upToken
    })


@require_http_methods(['GET'])
def fileDownload(request, key):
    baseUrl = 'http://%s/%s' % (settings.QINIU['bucketDomain'], key)
    privateUrl = q.private_download_url(baseUrl, expires=3600)
    return HttpResponseRedirect(redirect_to=privateUrl)


@require_http_methods(['GET','POST'])
def fileRename(request, key):
    if request.method=='GET':
        return render(request,'disk/fileRename.html',{
            'key': key,
            'fileName': key.split('/')[-1]
        })
    else:
        path=''
        for k in key.split('/')[:-1]:
            path+=k+'/'
        bucket.move(settings.QINIU['bucketName'], key, settings.QINIU['bucketName'], path+request.POST['newName'])
        return HttpResponseRedirect(redirect_to='/disk/file/list/'+path)


@require_http_methods(['GET','POST'])
def folderCreate(request, prefix):
    if request.method=='GET':
        return render(request,'disk/folderCreate.html',{
            'prefix': prefix
        })
    else:
        folderName = request.POST.get('folderName')
        if folderName is None:
            return HttpResponseRedirect(redirect_to='/disk/file/list/' + prefix)
        else:
            # TODO add a '.' file
            return HttpResponseRedirect(redirect_to='/disk/file/list/' + prefix + folderName + '/')