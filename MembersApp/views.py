from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import  CreateUserForm,ProfileForm,SavingsForm,MembersForm
from .models import Profile,Saving,Member
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
def registerPage(request):
    form =  CreateUserForm()
    contex = {'form':form}
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            return redirect('loginPage')
    return render(request, 'auth/register.html', contex)

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')
    contex = {}
    return render(request, 'auth/login.html', contex)

def logoutUser(request):
	logout(request)
	return redirect('loginPage')

@login_required(login_url='loginPage')
def index(request):
    context={}
    return render(request, 'index.html',context)

@login_required(login_url='loginPage')
def profilePage(request,user_id):
        profile=Profile.objects.get(id=user_id)
        contex = {'profile':profile}
        return render(request, 'profile.html', contex)
    
@login_required(login_url='loginPage')
def profileUpdates(request):
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    if request.method == 'POST':
        profileform = ProfileForm(request.POST,request.FILES,instance=profile)
        if  profileform.is_valid:
            profileform.save(commit=False)
            profileform.user=request.user
            profileform.save()
            return redirect('index')
    else:
        form=ProfileForm(instance=profile)
    return render(request,'editProfile.html',{'form':form})

@login_required(login_url='loginpage')
def savings(request):
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    savings=Saving.objects.all()
    if request.method == 'POST':
        form = SavingsForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.admin = request.user.profile
            form.save()
            return redirect('savings')
    else:
        form = SavingsForm()
    context={'savings':savings, 'form':form}
    return render(request,'saving.html',context)

@login_required(login_url='loginpage')
def members(request):
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    members=Member.objects.all()
    if request.method == 'POST':
        form = MembersForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.admin = request.user.profile
            form.save()
            return redirect('savings')
    else:
        form = MembersForm()
    context={'members':members, 'form':form}
    return render(request,'member.html',context)

def deleteMember(request, member_id):
    members=Member.objects.get(id=memberid)
    members.delete()
    return redirect('members')

# def deleteMember(request, member_id):
#     members = get_object_or_404(Member, id=member_id)
#     members.delete()
#     return redirect('member')
