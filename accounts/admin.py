from django.contrib import admin
from .models import (DiseaseDoctor, Employee, UserProfile, Disease,
                     DiseaseCategory, Medicine, BalanceMedicine,
                     IssuedMedicine, CaseFile)
# Register your models here

admin.site.register(Employee)
admin.site.register(UserProfile)
admin.site.register(Disease)
admin.site.register(DiseaseCategory)
admin.site.register(Medicine)
admin.site.register(BalanceMedicine)
admin.site.register(IssuedMedicine)
admin.site.register(CaseFile)
admin.site.register(DiseaseDoctor)