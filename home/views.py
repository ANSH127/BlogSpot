# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    posts=Post.objects.all().order_by('-views')[:3]
    params={'posts':posts}

    return render(request,'home/home.html',params)

def about(request):    
    return render(request,'home/about.html')

    
def contact(request): 
    if request.method=='POST':
        print('we are using post request')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        print(name,email,phone,desc)
        if len(name)<3 or len(email)<5 or len(phone)<10 or len(desc)<5:
            messages.error(request,'Please fill the from correctly')

        else:
            mycontact=Contact(name=name,email=email,phone=phone,desc=desc)
            mycontact.save()
            messages.success(request,'Contact Saved Successfully.We will get back to you')

        

    return render(request,'home/contact.html')

    
def search(request):
    quary=request.GET.get('quary','')
    print(quary)
    if len(quary)<50:
        allPostsTitle=Post.objects.filter(title__icontains=quary)
        allPostsContent=Post.objects.filter(content__icontains=quary)
        allPosts=allPostsTitle.union(allPostsContent)
    else:
        allPosts={}

    n=len(allPosts)
    params={'allPosts':allPosts,'totalresult':n}
    return render(request,"home/search.html",params)


def handleSignup(request):
    if request.method=='POST':
        # get the post parameter
        username=request.POST.get('username','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        password1=request.POST.get('password1','')
        print(username,name,email,password,password1)
        fname=name.split()[0]
        lname=name.split()[1]
        # username should be atleast 10 character long
        if len(username)>10:
            messages.error(request,'username must be under 10 characters')
            return redirect('/')
        # username should be alphanumeric
        
        if not  username.isalnum():
            messages.error(request,'username should only cantain letters and number')
            return redirect('/')
        # password should be match with confirm password field
        if password!=password1:
            messages.error(request,'Password does not match')
            return redirect('/')

        
        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your BlogCity account successfully created")
        return redirect('/')


    else:
        return render(request,'home/404.html')


def handleLogin(request):
    if request.method=='POST':
        loginusername=request.POST.get('username','')
        loginpassword=request.POST.get('password','')
        user=authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials, Please Try Again')
            return redirect('/')



        
    else:
        return render(request,'home/404.html')


def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logout')
    return redirect('/')
    


