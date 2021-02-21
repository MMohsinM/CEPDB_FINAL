from accounts.views import home_page

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import BalanceMedicine, Employee, Hospital, UserProfile, CaseFile, IssuedMedicine, Medicine
from django.forms import BaseModelFormSet


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username','first_name','last_name' ,'email', 'password1', 'password2')
        widgets = {
            'username' : widgets.TextInput(attrs={'placeholder': 'Enter cnic only numbers'})
        }
        labels = {
            'username': 'CNIC'
        }
    def password_match(self,*args,**kwargs):
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')
        if password1 is not password2: 
            raise forms.ValidationError("Passwords do not match")
        else:
            return password1
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control',
                                                    'maxlength':13, 'min':0, 'pattern':r'[0-9]*'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})

        for field in ('username','first_name','last_name' ,'email', 'password1', 'password2'):
            self.fields[field].help_text = None





class DirectorSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username','first_name','last_name' ,'email', 'password1', 'password2')
        widgets = {
            'username' : widgets.TextInput(attrs={'placeholder': 'Enter cnic only numbers'})
        }
        labels = {
            'username': 'Director CNIC'
        }
    def password_match(self,*args,**kwargs):
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')
        if password1 is not password2: 
            raise forms.ValidationError("Passwords do not match")
        else:
            return password1
    def __init__(self, *args, **kwargs):
        super(DirectorSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control',
                                                    'maxlength':13, 'min':0, 'pattern':r'[0-9]*'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})

        for field in ('username','first_name','last_name' ,'email', 'password1', 'password2'):
            self.fields[field].help_text = None


'''class UserEditForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username','first_name','last_name' ,'email', 'password1', 'password2')
        widgets = {
            'username' : widgets.TextInput(attrs={'placeholder': 'Enter cnic only numbers'})
        }
    def password_match(self,*args,**kwargs):
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')
        if password1 is not password2: 
            raise forms.ValidationError("Passwords do not match")
        else:
            return password1
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control',
                                                    'maxlength':13, 'min':0, 'pattern':r'[0-9]*'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})

        for field in ('username','first_name','last_name' ,'email', 'password1', 'password2'):
            self.fields[field].help_text = None
'''
class HospitalCreateForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ('hos_name', 'hos_loc')
    
    def __init__(self, *args, **kwargs):
        super(HospitalCreateForm, self).__init__(*args, **kwargs)
        self.fields['hos_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['hos_loc'].widget.attrs.update({'class' : 'form-control'})


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('salary','contact','age','addr')

    def __init__(self, *args, **kwargs):
        super(EmployeeCreateForm, self).__init__(*args, **kwargs)
        self.fields['salary'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact'].widget.attrs.update({'class' : 'form-control',
                                                    'placeholder':"+92xxxxxxxxxx",
                                                    'maxlength':13, 'pattern':r'\+*[0-9]*'})
        self.fields['age'].widget.attrs.update({'class' : 'form-control'})
        self.fields['addr'].widget.attrs.update({'class' : 'form-control'})
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs.update({'class' : 'form-control'})

class UserProfileEmpForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=((1,'doctor'), (2,'staff')))
    class Meta:
        model = UserProfile
        fields = ('user_type',)

    def __init__(self, *args, **kwargs):
        super(UserProfileEmpForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs.update({'class' : 'form-control'})


class CaseFileCreateForm(forms.ModelForm):
    class Meta:
        model = CaseFile
        fields = ('first_name','last_name', 'age', "dis", 'age','treatment','history',
                'addr', 'contact','status')

    def __init__(self, *args, **kwargs):
        super(CaseFileCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact'].widget.attrs.update({'class' : 'form-control',
                                                    'placeholder':"+92xxxxxxxxxx",
                                                    'maxlength':13, 'pattern':r'\+*[0-9]*'})
        self.fields['age'].widget.attrs.update({'class' : 'form-control'})
        self.fields['addr'].widget.attrs.update({'class' : 'form-control'})
        self.fields['dis'].widget.attrs.update({'class' : 'form-control'})
        self.fields['treatment'].widget.attrs.update({'class' : 'form-control'})
        self.fields['history'].widget.attrs.update({'class' : 'form-control'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})
        
        
class BalanceMedicineCreateForm(forms.ModelForm):
    class Meta:
        model = BalanceMedicine
        fields = ('med','balance')

    def __init__(self, *args, **kwargs):
        super(BalanceMedicineCreateForm, self).__init__(*args, **kwargs)
        self.fields['med'].widget.attrs.update({'class' : 'form-control'})
        self.fields['balance'].widget.attrs.update({'class' : 'form-control'})
       # self.fields['med_ID'].widget.attrs.update({'class' : 'form-control'})

class CaseFileEditForm(forms.ModelForm):
    class Meta:
        model = CaseFile
        fields = ('first_name','last_name', 'age', "dis",'treatment','history',
                'addr', 'contact', 'last_visit','status')

    def __init__(self, *args, **kwargs):
        super(CaseFileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact'].widget.attrs.update({'class' : 'form-control',
                                                    'placeholder':"+92xxxxxxxxxx",
                                                    'maxlength':13, 'pattern':r'\+*[0-9]*'})
        self.fields['age'].widget.attrs.update({'class' : 'form-control'})
        self.fields['addr'].widget.attrs.update({'class' : 'form-control'})
        self.fields['dis'].widget.attrs.update({'class' : 'form-control'})
        self.fields['treatment'].widget.attrs.update({'class' : 'form-control'})
        self.fields['history'].widget.attrs.update({'class' : 'form-control'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})
    
    
class IssuedMedicineForm(forms.ModelForm):
    class Meta:
        model = IssuedMedicine
        fields = ('med','quant')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("request_user")
        super(IssuedMedicineForm, self).__init__(*args, **kwargs)
        self.fields['med'].widget.attrs.update({'class' : 'form-control'})
        self.fields['med'].queryset = Medicine.objects.filter(
            balancemedicine__hos_ID = self.user.employee.hos_id)
        self.fields['quant'].widget.attrs.update({'class' : 'form-control'})


class EditIssuedMedicineForm(forms.ModelForm):
    class Meta:
        model = IssuedMedicine
        fields = ('quant',)
    def __init__(self, *args, **kwargs):
        super(EditIssuedMedicineForm, self).__init__(*args, **kwargs)
        self.fields['quant'].widget.attrs.update({'class' : 'form-control'})