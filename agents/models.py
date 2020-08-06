from django.db import models
from django.contrib.auth.models import User
import datetime



class SiteIdAssign(models.Model):
    username=models.CharField(max_length=30)
    site_id = models.CharField(max_length=20)
    idsource = models.CharField(default='no',max_length=10) # neteller or skrill

    def __str__(self):
        return self.site_id


# Not using it anymore
class Agents(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    address =models.CharField(max_length=100)
    profile_picture= models.ImageField()
    designation = models.CharField(max_length=100)
    work_place = models.CharField(max_length=100)
    author_description = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    site_id = models.CharField(max_length=20)
    Assign_site_id = models.ForeignKey(SiteIdAssign, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name.username


class AgentList(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    username =models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(default=None, max_length=100, null=True)
    password = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateField()

    # Newly added
    balance_neteller = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    balance_skrill = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    commission = models.CharField(null=True, blank=True, max_length=15,default=0)
    AdminProfitIn1K = models.CharField(null=True, blank=True, max_length=15,default=0)
    commissionType = models.CharField(default='All', max_length=10)
    partner_code = models.CharField(max_length=100, null=True)
    neteller_email = models.EmailField(null=True, blank=True)
    skrill_email = models.EmailField(null=True, blank=True)
    refferded_by = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)
    deposit_target = models.CharField(max_length=100, null=True, blank=True)
    membership_status = models.IntegerField(default=0)
    priority_level = models.IntegerField(default=0)
    assigned_to = models.CharField(max_length=100, null=True, blank=True) # Add username here in db
    note = models.TextField(null=True, blank=True)

    RevShareCB = models.CharField(null=True, blank=True, max_length=15)
    RevShareAgent = models.CharField(null=True, blank=True, max_length=15)
    RevShareActDate= models.DateField(default=datetime.datetime.now())



class AllAgentsCommission(models.Model):
    username = models.CharField(max_length=100)
    adminCommissionIn1K = models.CharField(null=True, blank=True, max_length=15)
    commission = models.CharField(null=True, blank=True, max_length=15)
    applyrules = models.CharField(default='All', max_length=10)
    activationDate = models.DateField(default=datetime.datetime.now())
    updated = models.DateField()
    #RevShareCB = models.CharField(null=True, blank=True, max_length=15)
    #RevShareAgent = models.CharField(null=True, blank=True, max_length=15)




class SkrillSignUp(models.Model):
    Skrill_ID = models.CharField(max_length=20)
    Site_ID = models.CharField(max_length=50)
    Partner_code= models.CharField(max_length=50)
    VipStatus = models.IntegerField(default=0)
    Date = models.DateField(auto_now=False)

    def __str__(self):
        return self.Skrill_ID

class SkrillDeposit(models.Model):
    Skrill_ID = models.CharField(max_length=20)
    Site_ID = models.CharField(max_length=50)
    Deposite = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    Profit = models.DecimalField ( max_digits = 8, decimal_places=2)
    AgentProfit = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    AgentProfitType = models.CharField(default='All', max_length=10)
    FinalCommssion = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    AdminProfitIn1K =  models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    Date = models.DateField(auto_now=False)

    def __str__(self):
        return self.Skrill_ID


class NetellerSignUp(models.Model):
    Neteller_ID = models.CharField(max_length=20)
    Site_ID = models.CharField(max_length=50)
    Partner_code = models.CharField(max_length=50)
    VipStatus = models.IntegerField(default=0)
    VipStatusDate = models.DateField(default=datetime.datetime.now())
    Date = models.DateField(auto_now=False)

    def __str__(self):
        return self.Neteller_ID

class NetellerDeposit(models.Model):
    Neteller_ID = models.CharField(max_length=20)
    Site_ID = models.CharField(max_length=50)
    Deposite = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    Profit = models.DecimalField(max_digits=8, decimal_places=2)
    AgentProfit = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    AgentProfitType = models.CharField(default='All', max_length=10)
    FinalCommssion = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    AdminProfitIn1K =  models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    Date = models.DateField(auto_now=False)

    def __str__(self):
        return self.Site_ID

class test(models.Model):
    profit=models.DecimalField(max_digits=3, decimal_places=3 )

    def __str__(self):
        return self.profit


class Support(models.Model):
    agents_name = models.CharField(max_length=100)
    agents_email=models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    message= models.TextField()
    Submited_date=models.DateField(auto_now_add=True ,auto_now=False)

    def __str__(self):
        return self.agents_name




class PaymentRequests(models.Model):
    agent = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    amount = models.CharField(max_length=10)
    paymentPlatform =models.CharField(max_length=200) # the platform where he wants to take payemnt
    paymentEmail =models.CharField(max_length=200)
    status = models.IntegerField(default=0) # refund, during declination - 1: upcoming, 2: paid, 3 declined
    paymentDetails = models.TextField()
    paymentNote = models.TextField()
    afterPaymentNote = models.TextField()
    afterPaymentBalance = models.CharField(max_length=10)
    datecreation = models.DateField(auto_now_add=True ,auto_now=False)
    duedate = models.DateField()


class NetReceiables(models.Model):
    platform = models.CharField(max_length=100)
    amount = models.CharField(max_length=10)
    datecreation = models.DateField(auto_now_add=True ,auto_now=False)



