#from datetime import date
from django.db import models
#from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import date
#from django.db.models.fields import AutoField
#from django.db.models.fields.related import ForeignKey


class Hospital(models.Model):
    hos_ID = models.AutoField(primary_key=True)
    hos_name = models.CharField(max_length=35)
    hos_loc = models.CharField(max_length=35)
    director = models.OneToOneField('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        # Unique Constraint ensures combination is unique
        constraints = [
            models.UniqueConstraint(fields=['hos_name','hos_loc'], name='unique_hospital')
        ]

    def __str__(self):
        return str(self.hos_name) + " " + str(self.hos_loc)


class UserProfile(models.Model):
    CHOICES = ((0,'health_minister'),(1,'doctor'), (2,'staff'), (3,'director'),
                (4,'None'))
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.PositiveIntegerField(choices=CHOICES, default=4)
    
    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_person(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
    try:
        instance.userprofile.save()
    except:
        UserProfile.objects.create(user = instance)


class Employee(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, unique=True, 
                                default='1')
    hos = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    age = models.PositiveIntegerField(default=0)
    addr = models.CharField(max_length=35, blank=True,null=True)
    contact = models.CharField(max_length=13, blank=True,null=True)
    salary = models.PositiveIntegerField(default=0)
    position = models.CharField(max_length=35, blank=True,null=True) # specialization in case of Doctor
    #profile_pic = models.ImageField(default='blank-profile-picture-973460_640.png',blank=True)
    def __str__(self):
        return str(self.user.username)


# Merge Director with Hospital
#class Director(models.Model):
#    cnic = models.OnetoOneField(Employee,primary_key=True,on_delete=models.CASCADE)

class Medicine(models.Model):
    med_ID = models.AutoField(primary_key=True)
    med_name = models.CharField(max_length=35, unique=True)
    med_salt = models.CharField(max_length=35, blank=True, null=True)
    med_company = models.CharField(max_length=35, blank=True, null=True)
    
    def __str__(self):
        return str(self.med_name)+" "+str(self.med_salt)+ " "+ str(self.med_company)


class BalanceMedicine(models.Model):
    med = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    hos_ID = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    balance = models.PositiveIntegerField(default=0)
    class meta:
        # Unique Constraint ensures combination is unique
        UniqueConstraint(fields=['hos_ID','med_ID'], name='unique_med_hos')

    def __str__(self):
        return self.med

@receiver(post_save, sender=BalanceMedicine)
def check_quantity(sender, instance, created, **kwargs):
    if instance.balance==0:
        instance.delete()


# THis was not added 
class DiseaseCategory(models.Model):
    category = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return str(self.category)



class Disease(models.Model):
    dis_ID = models.AutoField(primary_key=True)
    dis_name = models.CharField(max_length=45, unique=True)
    dis_cat = models.ForeignKey(DiseaseCategory,on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return str(self.dis_name)+" "+str(self.dis_cat)


# class Patient(models.Model):
#     patient_ID = models.AutoField(primary_key=True)
#     age = models.PositiveIntegerField(default=0)
#     addr = models.CharField(max_length=35,blank=True,null=True)
#     contact = models.CharField(max_length=13,blank=True,null=True)
#     first_name = models.CharField(max_length=10,null=True)
#     last_name = models.CharField(max_length=10,blank=True,null=True)


class CaseFile(models.Model):
    STATUS_CHOICES = ((1,'Ongoing'), (2,'Solved'), (3,'Expired'))
    doc = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    dis = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)
    last_visit = models.DateField(default=date.today)
    treatment = models.CharField(max_length=500,blank=True,null=True)
    history = models.TextField(max_length=500,blank=True,null=True)
    age = models.PositiveIntegerField(default=0)
    addr = models.CharField(max_length=35,blank=True,null=True)
    contact = models.CharField(max_length=13,blank=True,null=True)
    first_name = models.CharField(max_length=10,null=True)
    last_name = models.CharField(max_length=10,blank=True,null=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES,default=1)
    def __str__(self):
        return str(self.dis)+" "+str(self.doc)+" "+str(self.status)

    #class meta:
    #    UniqueConstraint(fields=['doc_ID','dis_ID', 'patient_ID'], name='unique_casefile')


class IssuedMedicine(models.Model):
    casefile = models.ForeignKey(CaseFile, on_delete=models.SET_NULL, null=True)
    med = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    quant = models.PositiveIntegerField(default=0,blank=True)
    date_issued = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date_issued)+" "+str(self.casefile)

    #class meta:
    #    UniqueConstraint(fields=['med','casefile'], name='unique_med_casefile')


# Disease Recommendation Table
class DiseaseDoctor(models.Model):
    dis_name = models.CharField(max_length=45, unique=True)
    dis_cat = models.CharField(max_length=40, unique=True)
    doc = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)