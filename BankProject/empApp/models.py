from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('manager', 'Manager'),
        ('assistanMgr', 'AssistanMgr'),
        ('employee', 'Employee'),
        ('customer','Customer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Adding unique related_name for groups
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Adding unique related_name for user_permissions
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

class Account(models.Model):
    SAVINGS = 'Savings'
    CHECKING = 'Checking'
    MONEY_MARKET = 'Money Market'
    LOAN = 'Loan'

    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings'),
        (CHECKING, 'Checking'),
        (MONEY_MARKET, 'Money Market'),
        (LOAN, 'Loan'),
    ]
    
    accno = models.AutoField(db_column='AccNo', primary_key=True)  # Field name made lowercase.
    balance = models.DecimalField(db_column='Balance', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=12, choices=ACCOUNT_TYPE_CHOICES, blank=True, null=True)  # Field name made lowercase.
    recentaccess = models.DateField(db_column='RecentAccess', blank=True, null=True)  # Field name made lowercase.
    interestsrate = models.DecimalField(db_column='InterestsRate', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    overdraft = models.DecimalField(db_column='OverDraft', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'


class AccOwner(models.Model):
    customerid = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='CustomerID', to_field='customerid')  # Field name made lowercase. The composite primary key (CSSN, AccNo) found, that is not supported. The first column is selected.
    accno = models.ForeignKey('Account', on_delete=models.CASCADE, db_column='AccNo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'acc_owner'
        unique_together = (('customerid', 'accno'),)


class AssistantMgr(models.Model):
    bid = models.OneToOneField('Branch', on_delete=models.CASCADE, db_column='BID', primary_key=True)  # Field name made lowercase.
    assistantmanager = models.ForeignKey('Employee', on_delete=models.SET_NULL, db_column='ASSISTANTMANAGER', to_field='ssn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assistant_mgr'


class Branch(models.Model):
    bid = models.IntegerField(db_column='BID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    assets = models.DecimalField(db_column='Assets', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'branch'


class Customer(models.Model):
    customerid = models.AutoField(db_column='CustomerID', primary_key=True)  # Field name made lowercase.
    cssn = models.IntegerField(db_column='CSSN', unique=True, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=100, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='Zipcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    streetno = models.CharField(db_column='StreetNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aptno = models.CharField(db_column='AptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class Employee(models.Model):
    empid = models.AutoField(db_column='EmpID', primary_key=True)  # Field name made lowercase.
    ssn = models.IntegerField(db_column='SSN', unique=True, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    teleno = models.CharField(db_column='TeleNo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dependentname = models.CharField(db_column='DependentName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bid = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='BID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Loans(models.Model):
    customerid = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='CustomerID', to_field='customerid', blank=True, null=True)  # Field name made lowercase.
    accno = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='AccNo', blank=True, null=True)  # Field name made lowercase.
    bid = models.ForeignKey(Branch, on_delete=models.SET_NULL, db_column='BID', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    loanno = models.IntegerField(db_column='LoanNo', primary_key=True)  # Field name made lowercase.
    monthlyrepayment = models.DecimalField(db_column='MonthlyRepayment', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loans'


class Manager(models.Model):
    bid = models.OneToOneField(Branch, on_delete=models.CASCADE, db_column='BID', primary_key=True)  # Field name made lowercase.
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, db_column='MANAGER', to_field='ssn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'manager'


class PersonalBanker(models.Model):
    customerid = models.OneToOneField(Customer, on_delete=models.CASCADE, db_column='CustomerID', to_field='customerid', primary_key=True)  # Field name made lowercase.
    bid = models.ForeignKey(Branch, on_delete=models.SET_NULL, db_column='BID', blank=True, null=True)  # Field name made lowercase.
    essn = models.ForeignKey(Employee, on_delete=models.SET_NULL, db_column='ESSN', to_field='ssn',blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'personal_banker'


class Transaction(models.Model):
    Credit = 'CD' 
    Withdraw = 'WD'


    Transaction_code_CHOICES = [
        (Credit, 'Credit'),
        (Withdraw, 'Withdraw'),
    ]

    tid = models.AutoField(db_column='TID', primary_key=True)  # Field name made lowercase. The composite primary key (TID, CSSN, AccNo) found, that is not supported. The first column is selected.
    cssn = models.IntegerField(db_column='CSSN')  # Field name made lowercase.
    accno = models.IntegerField(db_column='AccNo')  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=2, choices=Transaction_code_CHOICES, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    charge = models.DecimalField(db_column='Charge', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaction'
        unique_together = (('tid', 'cssn', 'accno'),)
