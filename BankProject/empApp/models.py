from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)



class AccOwner(models.Model):
    cssn = models.OneToOneField('Customer', models.DO_NOTHING, db_column='CSSN', primary_key=True)  # Field name made lowercase. The composite primary key (CSSN, AccNo) found, that is not supported. The first column is selected.
    accno = models.ForeignKey('Account', models.DO_NOTHING, db_column='AccNo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'acc_owner'
        unique_together = (('cssn', 'accno'),)


class Account(models.Model):
    accno = models.IntegerField(db_column='AccNo', primary_key=True)  # Field name made lowercase.
    balance = models.DecimalField(db_column='Balance', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=12, blank=True, null=True)  # Field name made lowercase.
    recentaccess = models.DateField(db_column='RecentAccess', blank=True, null=True)  # Field name made lowercase.
    interestsrate = models.DecimalField(db_column='InterestsRate', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    overdraft = models.DecimalField(db_column='OverDraft', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'


class AssistantMgr(models.Model):
    bid = models.OneToOneField('Branch', models.DO_NOTHING, db_column='BID', primary_key=True)  # Field name made lowercase.
    assistantmanager = models.ForeignKey('Employee', models.DO_NOTHING, db_column='ASSISTANTMANAGER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assistant_mgr'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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
    cssn = models.IntegerField(db_column='CSSN', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=100, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='Zipcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    streetno = models.CharField(db_column='StreetNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aptno = models.CharField(db_column='AptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    ssn = models.IntegerField(db_column='SSN', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    teleno = models.CharField(db_column='TeleNo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dependentname = models.CharField(db_column='DependentName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Loans(models.Model):
    cssn = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CSSN', blank=True, null=True)  # Field name made lowercase.
    accno = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccNo', blank=True, null=True)  # Field name made lowercase.
    bid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BID', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    loanno = models.IntegerField(db_column='LoanNo', primary_key=True)  # Field name made lowercase.
    monthlyrepayment = models.DecimalField(db_column='MonthlyRepayment', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loans'


class Manager(models.Model):
    bid = models.OneToOneField(Branch, models.DO_NOTHING, db_column='BID', primary_key=True)  # Field name made lowercase.
    manager = models.ForeignKey(Employee, models.DO_NOTHING, db_column='MANAGER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'manager'


class PersonalBanker(models.Model):
    cssn = models.OneToOneField(Customer, models.DO_NOTHING, db_column='CSSN', primary_key=True)  # Field name made lowercase. The composite primary key (CSSN, BID, ESSN) found, that is not supported. The first column is selected.
    bid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BID')  # Field name made lowercase.
    essn = models.ForeignKey(Employee, models.DO_NOTHING, db_column='ESSN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'personal_banker'
        unique_together = (('cssn', 'bid', 'essn'),)


class Transaction(models.Model):
    tid = models.IntegerField(db_column='TID', primary_key=True)  # Field name made lowercase. The composite primary key (TID, CSSN, AccNo) found, that is not supported. The first column is selected.
    cssn = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CSSN')  # Field name made lowercase.
    accno = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccNo')  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=2, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    charge = models.DecimalField(db_column='Charge', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaction'
        unique_together = (('tid', 'cssn', 'accno'),)
