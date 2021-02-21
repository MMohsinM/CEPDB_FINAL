from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import query
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from accounts.forms import (EmployeeCreateForm, IssuedMedicineForm, HospitalCreateForm, 
                            SignupForm,UserProfileEmpForm, CaseFileCreateForm, DirectorSignupForm,
                            CaseFileEditForm, BalanceMedicineCreateForm, EditIssuedMedicineForm)
from accounts.models import (BalanceMedicine, CaseFile, Disease, DiseaseCategory, 
                            DiseaseDoctor, UserProfile, IssuedMedicine)
from django.contrib.auth.models import User
from django.db import connection
from collections import namedtuple
from datetime import datetime
# Create your views here.

from accounts.models import  Hospital, Employee

###########################  USER CHECKS  ##########################

def check_hospital(user,hos_id):
    try:
        if hos_id == user.employee.hos_id:
            return True
        else:
            return False
    except ObjectDoesNotExist:
        return False


def is_hospital_doctor(user, hos_id):
    if check_hospital(user,hos_id):
        if user.userprofile.user_type==1:
            return True
        else:
            return False
    else:
        return False


def is_hospital_staff(user,hos_id):
    if check_hospital(user,hos_id):
        if user.userprofile.user_type==2:
            return True
        else:
            return False
    else:
        return False


def is_hospital_director(user, hos_id):
    if check_hospital(user, hos_id):
        hospital = Hospital.objects.get(hos_ID=hos_id)
        if hospital.director_id == user.id:
            return True
        else:
            return False
    else:
        return False


def is_casefile_doctor(user, casefile):
    if user.id == casefile.doc_id:
        return True
    else:
        return False


def is_doctor(user):
    if user.userprofile.user_type==1:
        return True
    else:
        return False
############################# EMPLOYEEE SECTION  ####################################

############## MAke STATS NOW ###################
############## DOCTOR STATS #####################
# Count Patient Dealt With 
# Monthly Patients
# Diseases seen #Pie Chart


############# Director Stats
# Total Patients
# Total Month Patients
# Disease Line chart Trend / per diesease per hospital


############## Health Minister STats ##########
# Pie CHart of total Diseases
# Disease Line chart Trend / per diesease

@login_required(login_url='/accounts/login')
def health_minister_dashboard(request):
    if request.user.userprofile.user_type == 0:
        context = {}
        context['chartBarX'] = []
        context['chartBarY'] = []
        context['chartPieX'] = []
        context['chartPieY'] = []
        context['chartAreaX'] = []
        context['chartAreaY'] = []
        context['cards'] = []
        sum_ = 0
        # Get total patient
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as dis_count, D.dis_name\
                FROM accounts_casefile as C, accounts_disease as D \
                WHERE D.dis_ID=C.dis_id \
                    GROUP BY C.dis_id ")
            #nt_result = namedtuple('Result', [col[0] for col in cursor.description])
            for row in cursor.fetchall():
                context['chartBarX'].append(row[1])
                context['chartBarY'].append(row[0])
                sum_ += row[0]    
        # GET TOTAL CASE STATUS 
        with connection.cursor() as cursor:
            cursor.execute("SELECT C.status, COUNT(*) as dis_count\
                    FROM accounts_casefile as C\
                    GROUP BY C.status")
            for row in cursor.fetchall():
                context['chartPieY'].append(row[1])
                if row[0] == 1 and 'Ongoing' not in context['chartPieX']:
                    context['chartPieX'].append('Ongoing')
                elif row[0] == 2 and "Solved" not in context['chartPieX']:
                    context['chartPieX'].append('Solved')
                elif row[0] == 3 and "Expired" not in context['chartPieX']:
                    context['chartPieX'].append('Expired')
        # GET MONTHLY COUNT OF DISEASE
        with connection.cursor() as cursor:
            cursor.execute("\
                    SELECT  Concat(YEAR(C.last_visit),'-', MONTH(C.last_visit)), COUNT(*) \
                    FROM    accounts_casefile as C\
                    WHERE   C.last_visit >= '%s-01-01' \
                    AND     C.last_visit <= '%s-12-31' \
                    GROUP BY YEAR(C.last_visit), MONTH(C.last_visit)", 
                    [datetime.now().year, datetime.now().year])
            for row in cursor.fetchall():
                context['chartAreaX'].append(row[0])
                context['chartAreaY'].append(row[1])
        context['cards'].append(('Diseases Count', sum_, 'primary'))
        return render(request, template_name='dashboard.html', context=context)
    else:
        return redirect("/")

@login_required(login_url='/accounts/login')
def dashboard(request, hos_id, u_id):
    # Check if director
    #director = is_hospital_director(request.user,hos_id)
    # Check if doctor
    #doctor = is_hospital_doctor(request.user,hos_id)
    #staff = False
    #if not doctor: # Staff and doctor are disjoint
        # Check if Staff 
    #    staff = is_hospital_staff(request.user,hos_id)
    #context = {'director': director, 'doctor': doctor, 'staff':staff, 'hos_id':hos_id}
    if not check_hospital(request.user,hos_id):
        return redirect("/")
    if not request.user.id == u_id:
        return redirect("/")
    context = {'hos_id':int(hos_id)}
    context['chartBarX'] = []
    context['chartBarY'] = []
    context['chartPieX'] = []
    context['chartPieY'] = []
    context['chartAreaX'] = []
    context['chartAreaY'] = []
    context['cards'] = []
    
    ########## Doctor ###########
    if request.user.userprofile.user_type == 1:
        # Get All Diseases dealt count
        sum_ = 0
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as dis_count, D.dis_name\
                FROM accounts_casefile as C, accounts_employee as E, accounts_disease as D \
                    WHERE C.doc_id=E.user_id and D.dis_ID=C.dis_id and E.user_id=%s \
                    GROUP BY C.dis_id ", [u_id])
            #nt_result = namedtuple('Result', [col[0] for col in cursor.description])
            for row in cursor.fetchall():
                context['chartBarX'].append(row[1])
                context['chartBarY'].append(row[0])
                sum_ += row[0]
        # Get Case Status 
        with connection.cursor() as cursor:
            cursor.execute("SELECT C.status, COUNT(*) as dis_count\
                    FROM accounts_casefile as C, accounts_employee as E \
                    WHERE C.doc_id=E.user_id and E.user_id=%s \
                    GROUP BY C.status", [u_id])
            for row in cursor.fetchall():
                context['chartPieY'].append(row[1])
                if row[0] == 1 and 'Ongoing' not in context['chartPieX']:
                    context['chartPieX'].append('Ongoing')
                elif row[0] == 2 and "Solved" not in context['chartPieX']:
                    context['chartPieX'].append('Solved')
                elif row[0] == 3 and "Expired" not in context['chartPieX']:
                    context['chartPieX'].append('Expired')
        # Monthly Disease Count 
        with connection.cursor() as cursor:
            cursor.execute("SELECT  CONCAT(YEAR(C.last_visit),'-', MONTH(C.last_visit)), COUNT(*) \
                    FROM    accounts_casefile as C, accounts_employee as E \
                    WHERE   C.last_visit >= '%s-01-01' \
                    AND     C.last_visit <= '%s-12-31' \
                    AND 	C.doc_id=E.user_id and E.user_id=%s\
                    GROUP BY YEAR(C.last_visit), MONTH(C.last_visit)",
                    [datetime.now().year,datetime.now().year,u_id])
            for row in cursor.fetchall():
                context['chartAreaX'].append(row[0])
                context['chartAreaY'].append(row[1])
        context['cards'].append(('Diseases Count', sum_, 'primary'))
    ########### DIRECTOR ###########
    elif request.user.userprofile.user_type == 3:
        sum_ = 0
        # Get total patient
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as dis_count, D.dis_name\
                FROM accounts_casefile as C, accounts_employee as E, accounts_disease as D, \
                    accounts_hospital as H \
                    WHERE C.doc_id=E.user_id and D.dis_ID=C.dis_id and H.hos_ID=%s and H.hos_ID=E.hos_id\
                    GROUP BY C.dis_id ", [hos_id])
            #nt_result = namedtuple('Result', [col[0] for col in cursor.description])
            for row in cursor.fetchall():
                context['chartBarX'].append(row[1])
                context['chartBarY'].append(row[0])
                sum_ += row[0]    
        # GET TOTAL CASE STATUS 
        with connection.cursor() as cursor:
            cursor.execute("SELECT C.status, COUNT(*) as dis_count\
                    FROM accounts_casefile as C, accounts_employee as E, accounts_hospital as H \
                    WHERE C.doc_id=E.user_id and H.hos_ID=E.hos_id and H.hos_ID=%s  \
                    GROUP BY C.status", [hos_id])
            for row in cursor.fetchall():
                context['chartPieY'].append(row[1])
                if row[0] == 1 and 'Ongoing' not in context['chartPieX']:
                    context['chartPieX'].append('Ongoing')
                elif row[0] == 2 and "Solved" not in context['chartPieX']:
                    context['chartPieX'].append('Solved')
                elif row[0] == 3 and "Expired" not in context['chartPieX']:
                    context['chartPieX'].append('Expired')
        #context['chartPieX'] = ['Ongoing','Solved','Terminated']
        # GET MONTHLY COUNT OF DISEASE
        with connection.cursor() as cursor:
            cursor.execute("\
                    SELECT  Concat(YEAR(C.last_visit),'-', MONTH(C.last_visit)), COUNT(*) \
                    FROM    accounts_casefile as C, accounts_employee as E, accounts_Hospital as H \
                    WHERE   C.last_visit >= '%s-01-01' \
                    AND     C.last_visit <= '%s-12-31' \
                    AND 	C.doc_id=E.user_id AND H.hos_Id=E.hos_id and H.hos_ID=%s \
                    GROUP BY YEAR(C.last_visit), MONTH(C.last_visit)", 
                    [datetime.now().year,datetime.now().year, hos_id])
            for row in cursor.fetchall():
                context['chartAreaX'].append(row[0])
                context['chartAreaY'].append(row[1])
        context['cards'].append(('Diseases Count', sum_, 'primary'))
    context['cards'].append(('Employee Salary', "PKR "+str(request.user.employee.salary), 'success'))
    return render(request, template_name='dashboard.html', context=context)

########### Create Employee #####################
@login_required(login_url='/accounts/login')
def create_employee(request, hos_id):
    if not is_hospital_director(request.user, hos_id):
        return redirect("/")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        user_form = UserProfileEmpForm(request.POST)
        emp_form = EmployeeCreateForm(request.POST)
        if form.is_valid() and user_form.is_valid() and emp_form.is_valid():
            user = form.save() # Base User Is created
            up = UserProfile.objects.get(user=user)
            userf = user_form.save(commit=False)
            up.user_type = userf.user_type
            up.save() #User Profile Class tuple Is created
            emp = emp_form.save(commit=False)
            emp.hos_id = hos_id
            emp.user = user
            emp.save() #Employee Tuple is created
            messages.add_message(request, messages.SUCCESS, "Employee Created")
            return redirect("/")
        else:
            messages.add_message(request, messages.WARNING, "Employee not Created")
            context = {'form':form, 'emp_form': emp_form,'user_form':user_form, 'hos_id':hos_id}
            return render(request, 'create_employee.html', context)
    else:
        form = SignupForm()
        emp_form = EmployeeCreateForm()
        user_form = UserProfileEmpForm()
        context = {'form':form, 'emp_form': emp_form,'user_form':user_form, 'hos_id':hos_id}
        return render(request, 'create_employee.html', context)

############### LIST EMPLOYEE ###############
@login_required(login_url='/accounts/login')
def list_employee(request,hos_id):
    if not check_hospital(request.user, hos_id):
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT U.first_name,U.last_name,U.id ,E.age, E.position,E.salary, A.user_type \
                        FROM accounts_employee E, auth_user U, accounts_userprofile A\
                        WHERE hos_id=%s  and E.user_id=U.id and A.user_id=U.id and\
                        A.user_id = E.user_id", [hos_id])
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context={'employees':[nt_result(*row) for row in cursor.fetchall()],'hos_id':hos_id}
    return render(request, 'list_employee.html',context)

################# DELETE EMPLOYEE ##############

@login_required(login_url='/accounts/login')
def delete_employee(request, hos_id, u_id):
    if not is_hospital_director(request.user, hos_id):
        return redirect("/")
    if request.user.id == u_id:
        return redirect("/")
    obj =  get_object_or_404(User, id=u_id)
    obj.delete()
    messages.add_message(request, messages.SUCCESS, "Deleted Employee")
    return redirect("/hospital/"+str(hos_id)+"/list-employee/")


############## Edit Employee ###############
def edit_employee(request, hos_id, u_id):
    if not is_hospital_director(request.user, hos_id):
        return redirect("/")
    if request.user.id == u_id:
        return redirect("/")
    obj =  get_object_or_404(User, id=u_id)
    user_form = UserProfileEmpForm(request.POST or None, instance=obj.userprofile)
    emp_form = EmployeeCreateForm(request.POST or None, instance=obj.employee)
    if user_form.is_valid() and emp_form.is_valid():
        user_form.save()
        emp_form.save()
        messages.add_message(request, messages.SUCCESS, "Employee Edited")
    template_name="edit_employee.html"
    context = {'emp_form': emp_form,'user_form':user_form,'obj':obj}
    return render(request,template_name,context)


@login_required(login_url='/accounts/login')
def read_employee(request, hos_id, u_id):
    if not check_hospital(request.user, hos_id):
        return redirect("/")
    context={}
    with connection.cursor() as cursor:
        cursor.execute("SELECT U.username,U.first_name,U.last_name,U.id ,E.age, E.position,E.salary, A.user_type \
                        FROM accounts_employee E, auth_user U, accounts_userprofile A\
                        WHERE U.id=%s and E.user_id=U.id and A.user_id=U.id and\
                        A.user_id = E.user_id", [u_id])
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context['employee']= [nt_result(*row) for row in cursor.fetchall()][0]
    context['hos_id'] = hos_id
    return render(request, 'employee_info.html', context=context)
    # Dont SHow CNIC to anyone except self


@login_required(login_url='/accounts/login')
def update_doctor_self(request, hos_id, doc_id):
    if not is_hospital_director(request.user, hos_id):
        return redirect("/")
    pass


################### Disease Recommend #####################
@login_required(login_url='/accounts/login')
def recommend_disease_doctor(request):
    # Form Disease
    # Check if disease already exists 
    # If disease Not Found Send to director
    if is_doctor(request.user):
        if request.POST:
            dis_name = request.POST.get('dis_name')
            dis_cat = request.POST.get('dis_cat')
            doc_id = request.user.id
            ## Check if a disease like this already exists or not ##
            with connection.cursor() as cursor:
                cursor.execute("SELECT D.dis_name, C.category \
                    FROM accounts_disease as D, accounts_diseasecategory as C \
                        WHERE D.dis_name=%s and C.category=%s and D.dis_cat_id=C.id",[dis_name, dis_cat])
                present_dis = len(cursor.fetchall())
            if present_dis>0:
                messages.add_message(request, messages.ERROR, "Disease already exists")
                return redirect("/hospital/"+str(request.user.employee.hos_id)+"/employee/"+str(request.user.id)+"/")
            ## Check if the request already exists or not ##
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) \
                    FROM accounts_diseasedoctor as D \
                    WHERE D.dis_name=%s and D.dis_cat=%s \
                    GROUP BY D.dis_name, D.dis_cat", [dis_name,dis_cat])
                present_req = len(cursor.fetchall())
            if present_req > 0:
                messages.add_message(request, messages.WARNING, "Request already exists from some Hospital")
                return redirect("/hospital/"+str(request.user.employee.hos_id)+"/employee/"+str(request.user.id)+"/")
            # Redirect has not happened meaning the disease request does not exit
            # and No similar requests are there in any hospital
            DiseaseDoctor.objects.create(dis_name=dis_name, dis_cat=dis_cat, doc_id=doc_id, approved=False)
            messages.add_message(request, messages.SUCCESS, "Request Sent")
            return redirect("/hospital/"+str(request.user.employee.hos_id)+"/employee/"+str(request.user.id)+"/")
        else:
            return render(request, 'recommend_disease_doctor.html')
        

@login_required(login_url='/accounts/login')
def disease_list_director(request,hos_id):
    # Approve Button with Recommended Disease View
    if not is_hospital_director(request.user,hos_id):
        return redirect("/")
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT DD.id, DD.dis_name, DD.dis_cat, A.username, A.id as user_id, A.first_name, A.last_name \
                        FROM accounts_diseasedoctor as DD, accounts_employee as E, accounts_hospital as H, auth_user as A \
                        WHERE H.hos_ID=%s and DD.approved=false and DD.doc_id=E.user_id and E.hos_id=H.hos_ID and A.id=E.user_id", [hos_id])
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context['diseases']= [nt_result(*row) for row in cursor.fetchall()]
    return render(request,'disease_list_director.html',context)
    

@login_required(login_url='/accounts/login')
def recommend_disease_director(request,hos_id, dd_id, action):
    if not is_hospital_director(request.user,hos_id):
        return redirect("/")
    # Create Admin Approved Disease
    obj = get_object_or_404(DiseaseDoctor, pk=dd_id)
    if action == 'reject':
        obj.delete()
        messages.add_message(request, messages.WARNING, "Request Deleted")
    elif action=='accept':
        obj.approved=True
        obj.save()
        messages.add_message(request, messages.SUCCESS, "Request Forwarded to Admin")
    return redirect("/hospital/disease-list/"+str(request.user.employee.hos_id)+"/")


@login_required(login_url='/accounts/login')
@staff_member_required
def disease_list_admin(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT DD.id, DD.dis_name, DD.dis_cat, A.first_name, A.last_name, \
                            H.hos_name, H.hos_loc \
                        FROM accounts_diseasedoctor as DD, accounts_employee as E, \
                            accounts_hospital as H, auth_user as A \
                        WHERE DD.approved=true and DD.admin_approved=false and DD.doc_id=E.user_id \
                            and E.hos_id=H.hos_ID and A.id=E.user_id")
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context['diseases']= [nt_result(*row) for row in cursor.fetchall()]
    return render(request,'disease_list_director.html',context)

@staff_member_required(login_url='/')
def admin_create_hospital(request):
    # Get all forms
    # Hospital Create Form 
    # UserCreateForm
    # UserprofileForm
    # EmployeeForm
    user_create_form = DirectorSignupForm(request.POST or None)
    emp_form = EmployeeCreateForm(request.POST or None)
    hos_form = HospitalCreateForm(request.POST or None)
    if request.method == 'POST':
        if user_create_form.is_valid() and\
            emp_form.is_valid() and hos_form.is_valid():
            # Saving Hospital First
            hospital = hos_form.save()
            # Base User Is created
            user = user_create_form.save() 
            # UserType Is created
            up = UserProfile.objects.get(user=user)
            up.user_type = 3
            up.save() #User Profile Class tuple Is created
            # Creating Director Employee
            emp = emp_form.save(commit=False)
            emp.hos_id = hospital.hos_ID
            emp.user = user
            emp.save() #Employee Tuple is created
            # Adding Hospital Director
            hospital.director_id = user.id
            hospital.save()
            messages.add_message(request, messages.SUCCESS, "Hospital Created")
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR, "Hospital Creation Failed")
    context = {'user_create_form': user_create_form,
                'emp_form':emp_form,'hos_form':hos_form}
    return render(request, 'admin_create_hospital.html',context)

@staff_member_required(login_url='/')
def admin_action_disease(request,dd_id,action):
    # Approve Button with Recommended Disease View
    # IF approved Create Disease
    obj = get_object_or_404(DiseaseDoctor, pk=dd_id)
    if action == 'reject':
        obj.delete()
        messages.add_message(request, messages.WARNING, "Request Deleted")
    elif action=='accept':
        obj.admin_approved=True
        ## Check If category exists
        dis_cat = obj.dis_cat
        with connection.cursor() as cursor:
            cursor.execute("SELECT C.category \
                        From accounts_diseasecategory as C\
                        WHERE C.category=%s", [dis_cat])
            category_len = len(cursor.fetchall())
        if category_len == 0:
            DiseaseCategory.objects.create(category=dis_cat)
        dis_cat = DiseaseCategory.objects.get(category=dis_cat)
        Disease.objects.create(dis_name=obj.dis_name,dis_cat=dis_cat)
        messages.add_message(request, messages.SUCCESS, "Disease Created")
        obj.delete()
    return redirect("/admin-disease-list/")

########################## CASEFILE SECTION ###################################
########## CASEFILE CREATE ###################
@login_required(login_url='/accounts/login')
def create_casefile(request, doc_id):
    if not is_doctor(request.user):
        return redirect("/")    
    # medicine_issue_formset = modelformset_factory(IssuedMedicine,
    #                        form=IssuedMedicineForm,
    #                        fields=('med','quant'),extra=0)
    # med_issue_form = medicine_issue_formset(request.POST or None,form_kwargs={'request_user': request.user})
    casefile_form = CaseFileCreateForm(request.POST or None)
    if request.method == 'POST':
        
        # Create FormSet
        if casefile_form.is_valid():# and med_issue_form.is_valid():
            casefile = casefile_form.save(commit=False)
            casefile.doc = request.user.employee
            casefile.save()
            # instances = med_issue_form.save(commit=False)
            # print(instances)
            # for instance in instances:
            #     instance.casefile_id = casefile.id
            #     print(instance)
            #     # Change Medicines before committing results
            #     with connection.cursor() as cursor:
            #         cursor.execute("UPDATE accounts_balancemedicine \
            #                         SET balance = balance - %s\
            #                         WHERE med_id=%s and hos_ID_id = \
            #                                             (SELECT hos_id \
            #                                             FROM accounts_employee \
            #                                             WHERE user_id=%s)", 
            #                     [instance.quant,instance.med_id, request.user.id])
            #     instance.save()
            messages.add_message(request, messages.SUCCESS, "Casefile Created")
        # Patient Create Form
            return redirect("/hospital/doctor-casefile/")
        else:
            messages.add_message(request, messages.WARNING, "Casefile NOT Created")        
    context = {'doc_id':doc_id,'casefile_form':casefile_form,}# 'med_issue_form':med_issue_form}
    return render(request, 'create_casefile.html', context=context)


########## CASEFILE UPDDATE ###################
@login_required(login_url='/accounts/login')
def edit_casefile(request, case_id):
    obj = get_object_or_404(CaseFile, pk=case_id)
    if not is_casefile_doctor(request.user,obj):
        return redirect("/")
    casefile_form = CaseFileEditForm(request.POST or None, instance=obj)
    if request.POST:
        casefile_form.save()
        messages.add_message(request, messages.SUCCESS, "Casefile Edited")
    context = {'casefile_form':casefile_form, 'obj':obj}
    return render(request, 'edit_casefile.html', context=context)


########### CASEFILE READ ##################
@login_required(login_url='/accounts/login')
def read_casefile(request, case_id):
    obj = get_object_or_404(CaseFile, pk=case_id) # GOT CASEFILE
    # If the user is not a doctor of the case file then redirect.
    issued_meds = IssuedMedicine.objects.filter(casefile=obj)
    print(issued_meds)
    if not is_casefile_doctor(request.user, obj):
        return redirect("/")
    context = {'casefile':obj, 'issued_meds':issued_meds}
    return render(request, 'casefile_info.html', context)
       

########## CASEFILE LIST ####################
@login_required(login_url='/accounts/login')
def list_casefile(request):
    if not is_doctor(request.user):
        return redirect("/")
    context={}
    with connection.cursor() as cursor:
        cursor.execute("SELECT C.id, C.first_name, C.last_name, C.age, D.dis_name, DC.category\
                        FROM accounts_casefile C, accounts_disease as D, accounts_diseasecategory as DC\
                        WHERE C.doc_id=%s and C.dis_id = D.dis_Id and D.dis_cat_id=DC.id", [request.user.id])
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context['patients']= [nt_result(*row) for row in cursor.fetchall()]
    return render(request, 'list_casefile.html', context)
    

################# DELETE CASEFILE ##############
@login_required(login_url='/accounts/login')
def delete_casefile(request, case_id):
    obj =  get_object_or_404(CaseFile, pk=case_id)
    if not is_casefile_doctor(request.user, obj):
        return redirect("/")
    obj.delete()
    messages.add_message(request, messages.WARNING, "Casefile Deleted")
    return redirect("/hospital/doctor-casefile/")

def update_balance(issued,user,diff):
        # Change Medicines before committing results
    with connection.cursor() as cursor:
        cursor.execute("UPDATE accounts_balancemedicine \
                        SET balance = balance - %s\
                        WHERE med_id=%s and hos_ID_id = \
                                        (SELECT hos_id \
                                        FROM accounts_employee \
                                        WHERE user_id=%s)", 
                                        [diff,issued.med_id,user.id])    
                    

################## ISSUE MEDICINE ######################
################## CREATE ISSUE ##################
@login_required(login_url='/accounts/login')
def issue_medicine(request, case_id):
    obj = get_object_or_404(CaseFile, pk=case_id)
    if not is_casefile_doctor(request.user,obj):
        return redirect("/")
    med_issue_form = IssuedMedicineForm(request.POST or None,request_user= request.user)
    if request.method == 'POST':
        if med_issue_form.is_valid():
            instance = med_issue_form.save(commit=False)
            instance.casefile_id = obj.id
            # Change Medicines before committing results
            update_balance(instance,request.user,instance.quant)
            instance.save()
            messages.add_message(request, messages.WARNING, "MEDICINE ADDED")
            return redirect('/hospital/casefile/'+str(case_id)+'/')
    template_name="create_issue_medicine.html"
    context = {'med_issue_form': med_issue_form}
    return render(request,template_name,context)

############### EDIT ISSUE ########################
@login_required(login_url='/accounts/login')
def edit_issue_medicine(request, issue_id):
    obj = get_object_or_404(IssuedMedicine, pk=issue_id)
    casefile = get_object_or_404(CaseFile, pk=obj.casefile_id)
    if not is_casefile_doctor(request.user,casefile):
        return redirect("/")
    med_issue_form = EditIssuedMedicineForm(request.POST or None,instance=obj)
    if request.method == 'POST':
        original = int(request.POST.get('original'))
        if med_issue_form.is_valid():
            instance = med_issue_form.save(commit=False)
            diff = instance.quant - original
            instance.casefile_id = casefile.id
            # Change Medicines before committing results
            if diff != 0:
                update_balance(instance,request.user,diff)
            instance.save()
            messages.add_message(request, messages.WARNING, "MEDICINE RECORD UPDATED")
            return redirect('/hospital/casefile/'+str(casefile.id)+'/')
    template_name="create_issue_medicine.html"
    context = {'med_issue_form': med_issue_form, 'original':obj.quant,'med_name':obj.med}
    return render(request,template_name,context)

############### DELETE ISSUE ################
@login_required(login_url='/accounts/login')
def delete_issue_medicine(request, issue_id):
    obj = get_object_or_404(IssuedMedicine, pk=issue_id)
    quant = -obj.quant
    casefile = get_object_or_404(CaseFile, pk=obj.casefile_id)
    if not is_casefile_doctor(request.user,casefile):
        return redirect("/")
    update_balance(obj, request.user, quant)
    with connection.cursor() as cursor:
        cursor.execute("Delete FROM accounts_issuedmedicine  \
                        WHERE id=%s", [obj.id])
    
    messages.add_message(request, messages.SUCCESS, "Medicine Record Deleted")
    return redirect('/hospital/casefile/'+str(casefile.id)+'/')

################# Medicine ############################
################# Medicine LIST #######################
@login_required(login_url='/accounts/login')
def list_medicine(request,hos_id):
    if not check_hospital(request.user, hos_id):
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT M.med_name,M.med_salt,M.med_company,M.med_ID, B.balance  \
                        FROM accounts_medicine as M, accounts_balancemedicine B \
                        WHERE B.med_id=M.med_ID and B.hos_ID_id=%s",[hos_id])
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context={'medicines':[nt_result(*row) for row in cursor.fetchall()]}
        context['hos_id']=hos_id
    return render(request, 'list_medicine.html',context)


################# Medicine Create #######################
@login_required(login_url='/accounts/login')
def create_medicine(request, hos_id):
    if not check_hospital(request.user, hos_id):
        return redirect("/")
    if request.method == 'POST':
        medicine_form = BalanceMedicineCreateForm(request.POST)
        if medicine_form.is_valid():
            casefile = medicine_form.save(commit=False)
            casefile.hos_ID_id = request.user.employee.hos_id
            qs = BalanceMedicine.objects.filter(hos_ID_id = request.user.employee.hos_id,
                                                med=casefile.med)
            qs.exclude(pk = casefile.pk)
            if qs.exists():
                messages.add_message(request, messages.WARNING, "Medicine Already Exists")
            else:
                casefile.save()
                messages.add_message(request, messages.SUCCESS, "Medicine Created")
        # Patient Create Form
            return redirect("/hospital/"+str(hos_id)+"/list-medicine/")
        else:
            messages.add_message(request, messages.WARNING, "Medicine Record Not Created")
            context = {'hos_id':hos_id,'medicine_form':medicine_form}
            return render(request, 'create_medicine.html', context=context)
    else:
        medicine_form = BalanceMedicineCreateForm()
    context = {'hos_id':hos_id,'medicine_form':medicine_form}
    return render(request, 'create_medicine.html', context=context)


################# Medicine Delete #######################
@login_required(login_url='/accounts/login')
def delete_medicine(request, hos_id, med_ID):
    if not is_hospital_director(request.user, hos_id):
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("Delete FROM accounts_balancemedicine  \
                        WHERE med_ID=%s", [med_ID])
    messages.add_message(request, messages.SUCCESS, "Medicine Record Deleted")
    return redirect("/hospital/"+str(hos_id)+"/list-medicine/")


################ Medicine Read #####################
@login_required(login_url='/accounts/login')
def read_medicine(request, hos_id, med_ID):
    if not check_hospital(request.user, hos_id):
        return redirect("/")
    context={}
    with connection.cursor() as cursor:
        cursor.execute("SELECT M.med_name,M.med_salt,M.med_company,M.med_ID, B.balance \
                        FROM accounts_medicine as M, accounts_balancemedicine B \
                        WHERE M.med_ID=%s and B.med_id=M.med_ID", [med_ID])
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        context['medicine']= [nt_result(*row) for row in cursor.fetchall()][0]
    context['hos_id'] = hos_id
    return render(request, 'medicine_info.html', context=context)


################ Medicine Edit  #####################
def edit_medicine(request, hos_id, med_ID):
    if not check_hospital(request.user, hos_id):
        return redirect("/")
    obj =  get_object_or_404(BalanceMedicine, id=med_ID)
    medicine_form = BalanceMedicineCreateForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if medicine_form.is_valid():
            medicine_form.save()
            messages.add_message(request, messages.SUCCESS, "Employee Edited")
        else:
            messages.add_message(request, messages.WARNING, "Employee Editing Faild")
    context = {'medicine_form'}
    context = {'hos_id':hos_id,'medicine_form':medicine_form}
    return render(request, 'create_medicine.html', context=context)