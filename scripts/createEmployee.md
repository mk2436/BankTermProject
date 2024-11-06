from django.db import models
from empApp.models import CustomUser, Branch, Employee, Manager

newBranch = Branch.objects.create(bid=1, name='Main Branch', assets=1000000.00, city='New York', address= '123 Main St')
newBranch.save()

newEmployee = Employee.objects.create(ssn=123456789,name= 'John Doe', startdate='2020-01-15', teleno ='555-1234', dependentname= 'Jane Doe',bid= newBranch)
newEmployee.save()

newManager = Manager.objects.create(bid=newBranch,manager=newEmployee)
newManager.save()

newCustomUser = CustomUser.objects.create(username=newEmployee.empid,user_type='manager')
newCustomUser.set_password('John_Doe@123456789')
newCustomUser.save()