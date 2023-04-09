from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.
def blogHome(request):
        allPosts=Post.objects.all()
        # print(allPosts)
        context={'allPosts':allPosts}
        return render(request,'blog/blogHome.html',context)


def blogPost(request,slug):
        post=Post.objects.filter(slug=slug).first()
        
        post.views=post.views+1
        post.save()
        comments=BlogComment.objects.filter(post=post,parent=None).order_by('-timestamp')
        replies=BlogComment.objects.filter(post=post).exclude(parent=None).order_by('-timestamp')
        repDict={}
        # print(replies)
        for reply in replies:
                if reply.parent.sno not in repDict.keys():
                        repDict[reply.parent.sno]=[reply]
                        
                else:
                        repDict[reply.parent.sno].append(reply)
        # print(repDict)
        context={'post':post,'comments':comments,'user':request.user,'replyDict':repDict}
        return render(request,'blog/blogPost.html',context)

def postcomment(request):
        if request.method=='POST':
                comment=request.POST.get("comment")
                user=request.user
                postSno=request.POST.get("postSno")
                post=Post.objects.get(sno=postSno) 
                parentSno=request.POST.get('parentSno')
                if parentSno=="": 
                        comment=BlogComment(comment=comment,user=user,post=post)
                        
                        comment.save()
                        messages.success(request,'Your Comment has been posted Sucssfully')
                else:
                        parent=BlogComment.objects.get(sno=parentSno)
                        comment=BlogComment(comment=comment,user=user,post=post,parent=parent)

                        comment.save()
                        messages.success(request,'Your Reply has been posted Sucssfully')
        
                return redirect(f'/blog/{post.slug}')

        else:
                return render(request,'home/404.html')




