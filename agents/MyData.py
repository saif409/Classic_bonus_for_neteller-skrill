
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import test,Agents,Support,SiteIdAssign, AgentList
from.forms import createAgetns
from django.db.models import Sum
from django.contrib import messages
from agents.models import SkrillSignUp,SkrillDeposit,NetellerSignUp,NetellerDeposit,Agents,Support,AgentList
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import TruncMonth


# Search methods
def netellerdepositsearch(request):

    siteids = SiteIdAssign.objects.filter(
        username= request.session['agent_username'], idsource='neteller'
    ).values('site_id')

    post = NetellerDeposit.objects.filter(Site_ID__in=siteids)

    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_transactions = paginator.get_page(page)
    search = request.GET.get('q')

    context={
        "post":total_transactions,
        'isact_mydata': 'active'
    }
    return render(request, 'agenttemplates/search/deposit/netller_deposit_search.html', context)

def skrilldepositsearch(request):


    siteids = SiteIdAssign.objects.filter(
        username= request.session['agent_username'], idsource='skrill'
    ).values('site_id')

    post = SkrillDeposit.objects.filter(Site_ID__in=siteids)

    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    search = request.GET.get('q')

    context={
        "post":total_article,
        'isact_mydata': 'active'
    }
    return render(request, 'agenttemplates/search/deposit/skrill_deposit_search.html', context)

def netellersignupsearch(request):

    siteids = SiteIdAssign.objects.filter(
        username= request.session['agent_username'], idsource='neteller'
    ).values('site_id')

    post = NetellerSignUp.objects.filter(Site_ID__in=siteids)

    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    search = request.GET.get('q')

    context={
        "post":total_article,
        'isact_mydata': 'active'
    }
    return render(request, 'agenttemplates/search/skrill/neteller_signup_search.html', context)

def skrilsignupsearch(request):

    siteids = SiteIdAssign.objects.filter(
        username= request.session['agent_username'], idsource='skrill'
    ).values('site_id')

    post = SkrillSignUp.objects.filter(Site_ID__in=siteids)

    search = request.GET.get('q')
    paginator = Paginator(post, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)

    context={
        "post":total_article,
        'isact_mydata': 'active'
    }
    return render(request, 'agenttemplates/search/skrill/skrill_signup_search.html', context)



# Search methods end
def mylinks(request):
    agent = request.session['agent_username']
    if agent:

        net_siteids = SiteIdAssign.objects.filter(
            username=agent, idsource='neteller'
        ).values('site_id')

        skr_siteids = SiteIdAssign.objects.filter(
            username=agent, idsource='skrill'
        ).values('site_id')


        context = {
            'isact_mylinks': 'active',
            'net_siteids': net_siteids,
            'skr_siteids': skr_siteids
        }
        return render(request, 'agenttemplates/mylinks.html', context)

    else:
        return redirect('login')




def mydatas(request):
    agent = request.session['agent_username']
    if agent:

        net_siteids = SiteIdAssign.objects.filter(
            username=agent, idsource='neteller'
        ).values('site_id')

        skr_siteids = SiteIdAssign.objects.filter(
            username=agent, idsource='skrill'
        ).values('site_id')

        netellerMonthlyPayables = NetellerDeposit.objects.filter(Site_ID__in=net_siteids).annotate(month=TruncMonth('Date')). \
            values('month').annotate(c=Sum('FinalCommssion'),d=Sum('Deposite')).values('month', 'c','d').order_by('-month')

        skrillMonthlyPayables = SkrillDeposit.objects.filter(Site_ID__in=skr_siteids).annotate(month=TruncMonth('Date')). \
            values('month').annotate(c=Sum('FinalCommssion'),d=Sum('Deposite')).values('month', 'c','d').order_by('-month')


        context = {
            "isact_mydatas": "active",
            "bothSNLists": zip(netellerMonthlyPayables, skrillMonthlyPayables),
        }


        return render(request, 'agenttemplates/mydatas.html', context)

    else:
        return redirect('login')