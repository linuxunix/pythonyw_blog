import models
from blogs import settings

class ArticleGen(object):
    def __init__(self,request):
        self.request = request

    def parse_data(self):
        form_data = {
        'title' : self.request.POST.get('title'),
        'content' : self.request.POST.get('content'),
        'type':self.request.POST.get('type'),
        'category_id': self.request.POST.get('category'),
        'summary' : self.request.POST.get('summary'),
        'author_id': self.request.user.userprofile.id,
        'head_img':'',
        }
        return form_data

    def create(self):
        self.data = self.parse_data()
        bbs_obj=models.Article(**self.data)
        # print bbs_obj
        # bbs_obj.save()
        filename = handle_upload_file(self.request,self.request.FILES['head_img'])
        bbs_obj.head_img = 'static/imgs/upload/%s' % filename
        bbs_obj.save()
        return  bbs_obj



def handle_upload_file(request,file_obj):
    upload_dir = "static/imgs/upload"
    with open('%s/%s' %(upload_dir,file_obj.name),'wb') as destination :
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return   file_obj.name

