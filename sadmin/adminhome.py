from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from agents.models import SkrillSignUp,SkrillDeposit,NetellerSignUp,NetellerDeposit,Agents,Support,AgentList, SiteIdAssign
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
# from agents.forms import agentprofileedit
from django.db.models import Q
from django.db.models import Sum
from django.core.paginator import Paginator
import csv, io
import datetime



def home(request):
    if request.user.is_authenticated:
        total_revenue_skrill_deposit = SkrillDeposit.objects.aggregate(Sum('Profit'))['Profit__sum']
        total_revenue_neteller_deposit = NetellerDeposit.objects.aggregate(Sum('Profit'))['Profit__sum']

        total_skrill_signups = SkrillSignUp.objects.all().count()
        total_neteller_signups = NetellerSignUp.objects.all().count()



        context={
            "total_revenue_skrill_deposit":total_revenue_skrill_deposit,
            "total_revenue_neteller_deposit": total_revenue_neteller_deposit,
            'isact_dashboard': 'active',
            'total_skrill_signups': total_skrill_signups,
            'total_neteller_signups': total_neteller_signups

        }
        return render(request, 'sadmintemplates/main.html',context)
    else:

        return redirect('admin-login')

def getAdminlogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(username=username, password=password)
            if auth is not None:
                login(request, auth)
                if request.user.is_superuser:
                    return redirect('home')
                else:
                    return redirect('agentshome')
            else:
                messages.add_message(request, messages.INFO, 'Username or password missmatch !!')

    return render(request, 'sadmintemplates/login.html')


def getlogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('user')
            password = request.POST.get('pass')
            auth = AgentList.objects.filter(username=username, password=password).exists()
            print('login auth', auth)
            if auth:
                statuscheck = AgentList.objects.filter(username=username, status=1).exists()
                if statuscheck:
                    request.session['agent_username'] = username
                    return redirect('agentshome')
                else:
                    messages.add_message(request, messages.INFO, 'Your account is not active! Contact Admin!')

            else:
                messages.add_message(request, messages.INFO, 'Username or password missmatch !!')

    return render(request, 'agenttemplates/login.html')


def getRegister(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            email = request.POST.get('email')
            user = AgentList(username=username, fname=first_name, lname=last_name, email=email,password=password, status=0, created= datetime.datetime.now() )
            user.save()

            return redirect('login')
        return render(request, "agenttemplates/user_registration.html")

def getlogout(request):
    request.session['agent_username'] = None
    return redirect('login')




def getAdminlogout(request):
    logout(request)
    return redirect('admin-login')





def skrillsignupslist(request):
    skrillsignups = SkrillSignUp.objects.all()

    paginator = Paginator(skrillsignups, 100)
    page = request.GET.get('page')
    all_skrillsignups = paginator.get_page(page)
    context={
        "skrillsignups": all_skrillsignups,
        'isact_signups': 'active'
    }
    return render(request,'sadmintemplates/list/skrillsignupslist.html',context )



def SkrillSignsUp(request):
    template = "sadmintemplates/depositskrill/skrill_signup.html"
    prompt = {
        'order': 'Order of the CSV should be Neteller_ID, Site_ID, Partner_code, Date',
    }
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = SkrillSignUp.objects.update_or_create(
            Skrill_ID=column[0],
            Site_ID=column[1],
            Partner_code=column[2],
            Date=column[3]
        )
    messages.add_message(request, messages.INFO, 'Your File Has Been Uploaded!')
    return render(request, template)


def Netellersignuplist(request):

    netellerSignups = NetellerSignUp.objects.all()
    paginator = Paginator(netellerSignups, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_netellerSignups = paginator.get_page(page)
    context = {
        "netellerSignups": total_netellerSignups,
        'isact_signups':'active'
    }
    return render(request, 'sadmintemplates/list/Neteller_signup_list.html', context)

def NetellerSignsUp(request):
    template = "sadmintemplates/depositskrill/neteller_signup.html"
    prompt = {
        'order': 'Order of the CSV should be Neteller_ID, Site_ID, Partner_code, Date',
    }
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = NetellerSignUp.objects.update_or_create(

            Neteller_ID=column[0],
            Site_ID=column[1],
            Partner_code=column[2],
            Date=column[3]
        )
    messages.add_message(request, messages.INFO, 'Your File Has Been uploaded!!')
    return render(request, template)

def Skrilldepositlist(request):
    skrdeposits = SkrillDeposit.objects.all()
    paginator = Paginator(skrdeposits, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_skrdeposits = paginator.get_page(page)
    context = {
        "skrdeposits": total_skrdeposits,
        'isact_deposits': 'active'
    }
    return render(request, 'sadmintemplates/list/Skrill_deposit_list.html', context)

def SkrillDeposite(request):
    template = "sadmintemplates/depositskrill/skrill_deposite.html"
    prompt = {

        'order': 'Order of the CSV should be Neteller_ID, Site_ID, Deposite, Profit, Date',
    }
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = SkrillDeposit.objects.update_or_create(

            Skrill_ID=column[0],
            Site_ID=column[1],
            Deposite=column[2],
            Profit=column[3],
            Date=column[4]
        )
    messages.add_message(request, messages.INFO, 'Your File Has Been uploaded!!')
    return render(request, template)

def Netellerdepositslist(request):
    data = NetellerDeposit.objects.all()
    paginator = Paginator(data, 100)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "data": total_article,
        'isact_deposits': 'active'
    }
    return render(request, 'sadmintemplates/list/Netellerdepositslist.html', context)

def NetellerDeposite(request):
        template = "sadmintemplates/depositskrill/netellerdeposite.html"
        prompt = {
            'order': 'Order of the CSV should be Neteller_ID, Site_ID, Deposite, Profit, Date',
        }
        if request.method == "GET":
            return render(request, template, prompt)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = NetellerDeposit.objects.update_or_create(

                Neteller_ID=column[0],
                Site_ID=column[1],
                Deposite=column[2],
                Profit=column[3],
                Date=column[4]
            )
        messages.add_message(request, messages.INFO, 'Your File Has Been uploaded!!')
        return render(request, template)



# Search methods
def netellerdepositsearch(request):
    post= NetellerDeposit.objects.all()
    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(id__icontains=search) |
            Q(Neteller_ID__icontains=search) |
            Q(Site_ID__icontains=search) |
            Q(Profit__icontains=search) |
            Q(Deposite__icontains=search)|
            Q(Date__icontains=search)
        )
    context={
        "post":total_article,
        'isact_search': 'active'
    }
    return render(request, 'sadmintemplates/search/deposit/netller_deposit_search.html', context)

def skrilldepositsearch(request):
    post= SkrillDeposit.objects.all()
    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(id__icontains=search) |
            Q(Neteller_ID__icontains=search) |
            Q(Site_ID__icontains=search) |
            Q(Profit__icontains=search) |
            Q(Deposite__icontains=search) |
            Q(Date__icontains=search)
        )
    context={
        "post":total_article,
        'isact_search': 'active'
    }
    return render(request, 'sadmintemplates/search/deposit/skrill_deposit_search.html', context)

def netellersignupsearch(request):
    post= NetellerSignUp.objects.all()
    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(Neteller_ID__icontains=search) |
            Q(Site_ID__icontains=search) |
            Q(Partner_code__icontains=search) |
            Q(Date__icontains=search)
        )
    context={
        "post":total_article,
        'isact_search': 'active'
    }
    return render(request, 'sadmintemplates/search/skrill/neteller_signup_search.html', context)

def skrilsignupsearch(request):
    post= SkrillSignUp.objects.all()
    search = request.GET.get('q')
    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    if search:
        post = post.filter(
            Q(Neteller_ID__icontains=search) |
            Q(Site_ID__icontains=search)|
            Q(Partner_code__icontains=search)|
            Q(Date__icontains=search)
        )
    context={
        "post":total_article,
        'isact_search': 'active'
    }
    return render(request, 'sadmintemplates/search/skrill/skrill_signup_search.html', context)

# Search methods end



def Agentslist(request, filter):
    agents = None

    if filter == 'None':
        agents = AgentList.objects.all()
    elif filter == 'active':
        agents = AgentList.objects.filter(status=1)
    elif filter == 'inactive':
        agents = AgentList.objects.filter(status=0)

    context={
        "agents":agents,
        'isact_agents': 'active'
    }
    return render(request, 'sadmintemplates/admin_agents/agents_list.html',context)




def getsupport(request):
    user_request = Support.objects.all()
    context={
        "user_request":user_request
    }
    return render(request, 'sadmintemplates/admin_agents/support.html', context)



def GetSupportDetails(request):

    return render(request, 'sadmintemplates/admin_agents/support.html')



def GetAgentsProfile(request, id):
    singleagent = get_object_or_404(Agents, id=id)
    context = {
        "singleagent": singleagent,
    }
    return render(request, 'sadmintemplates/admin_agents/agents_profile.html', context)


def GetAgentsProfileEdit(request,username):

    if request.user.is_authenticated:
        if request.method == "POST":
            update_fname = request.POST.get('update_firstname')
            update_lname = request.POST.get('update_lastname')
            update_email = request.POST.get('update_email')
            update_status = request.POST.get('update_status')
            update_contactno = request.POST.get('update_contactno')
            update_newpass = request.POST.get('update_newpass')

            returns = AgentList.objects.filter(username=username)\
                .update(fname = update_fname,lname=update_lname,email=update_email,
                        phone=update_contactno,password=update_newpass,status=update_status)


            if returns:
                userupdateresponse = 'Successfully Updated!'
            else:
                userupdateresponse = 'Update failed!'

            singleUser = AgentList.objects.get(username=username)

            return render(request,
                          'sadmintemplates/admin_agents/agents_edit_Profile.html',
                          { 'singleUser': singleUser, 'userupdateresponse': userupdateresponse})

        else:

            singleUser = AgentList.objects.get(username=username)
            return render(request,
                          'sadmintemplates/admin_agents/agents_edit_Profile.html',
                          { 'singleUser': singleUser})

    else:
        return redirect('admin-login')


def setsiteid(request,agent):

    thesiteids = SiteIdAssign.objects.filter(username=agent)

    message =''
    if request.method == "POST":
        siteid = request.POST.get('siteid')
        siteidtype = request.POST.get('siteidtype')
        if SiteIdAssign.objects.filter(site_id=siteid,idsource=siteidtype).exists():
            message = 'Failed! Site ID is assigned already!'
        else:
            insert = SiteIdAssign(username=agent, site_id=siteid,idsource=siteidtype)
            insert.save()
            message = 'Site ID added successfully!'

    context = {
            "theagent": agent,
            "siteidaddingmessage": message,
            'thesiteids': thesiteids
    }
    return render(request, 'sadmintemplates/setsiteid.html', context)





