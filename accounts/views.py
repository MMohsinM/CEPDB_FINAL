from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, logout
#from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required



# ###########################
# from .models import Employee
# from .forms import EmployeeCreateForm
# # Create your views here.

@login_required(login_url='/accounts/login')
def home_page(request):
    if request.user.is_authenticated:
        # Check User Type
        user_type = request.user.userprofile.user_type
        if user_type == 0: # Health Minister
            return redirect("/hospital/health_minister/")
        elif user_type == 1 or user_type==2 or user_type==3: # EMployee
            hos_id = request.user.employee.hos_id
            return redirect('/hospital/'+str(hos_id)+'/employee/'+str(request.user.id))
        else: # Neither
            return render(request, 'home.html')


def userloginview(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        error = ""
        if user:
            auth_login(request,user)
            # Check User Type
        else:
            error = "Username or password incorrect" 
            return render(request,"login.html",{'username':username,"error":error})
    if request.user.is_authenticated:
        user_type = request.user.userprofile.user_type
        if user_type == 0:
            return redirect("/hospital/health_minister")
        elif user_type == 1:
            hos_id = request.user.employee.hos_id
            return redirect('/hospital/'+str(hos_id)+'/employee/'+str(request.user.id))
        else:
            return redirect("/")
    template_name = "login.html"
    return render(request, template_name)


@login_required(login_url='/accounts/login')
def userlogoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

'''
def signup(request):
    template_name = 'signup.html'
    if request.method == 'POST':
        form = SignupForm(request.POST)
        userform = UserProfileForm(request.POST,request.FILES)#Get data from Request.POST and FILES
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # User is not activated till it is validated
            user.save() # this sends the signal for user profile features
            userf = UserProfile.objects.get(user=user)
            if userform.is_valid():
                userf.can_upload = userform.cleaned_data['can_upload']
                userf.profile_pic = userform.cleaned_data['profile_pic']
                userf.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
        userform = UserProfileForm()
    return render(request, template_name, {'form': form,'userform':userform})
    '''

def activate(request, uidb64, token):
    pass
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         auth_login(request, user)
#         return redirect('/')
#     else:
#         return HttpResponse('Activation link is invalid!')

# #################### APPROVAL LIST ##################################
# def approve_list(request):
#     if not request.user.is_superuser:
#         return redirect('/')
#     else:
#         request.user.can_upload=True
#         request.user.unchecked=False
#         users = userProfile.objects.filter(unchecked=True,can_upload=True)
#         context = {'users':users}
#         template = 'approve-list.html'
#         return render(request,template,context)


# def approve(request,message):
#     if not request.user.is_superuser:
#         return redirect('/')
#     ml = message.split(',')
#     id = ml[0]
#     option = ml[1]
#     user = userProfile.objects.get(id=id)
#     if option == '1':
#         user.can_upload = True
#         user.unchecked = False
#         user.save()
#     elif option == '2':
#         user.can_upload = False
#         user.unchecked = False
#         user.save()
#     return redirect('/accounts/approve-list/')
        

# def about(request,id):
#     user = userProfile.objects.get(id=id)
#     context = {'userpro':user}
#     template = "about-user.html"
#     return render(request,template,context) 


# ############## EMPLOYEE LIST #################
# def make_employee(request):
#     template_name = 'create-employee.html'
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         userform=EmployeeCreateForm(request.POST,request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()           
#             if userform.is_valid():
#                 employee=userform.save(commit=False)
#                 employee.person = user
                
#                 employee.save()
#                 return redirect("/accounts/about-us/")
#     else:
#         form = SignupForm()
#         userform = EmployeeCreateForm()
#     return render(request, template_name, {'form': form,'userform':userform})
    

# def employee_list(request):
#     template = 'employee-list.html'
#     e = Employee.objects.all()
#     context = {'employees':e}
#     return render(request,template,context)






