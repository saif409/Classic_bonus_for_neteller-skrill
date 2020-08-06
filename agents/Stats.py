from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import test,Agents,Support,SiteIdAssign, AgentList
from.forms import createAgetns
from django.db.models import Sum,Count
from django.contrib import messages
from agents.models import SkrillSignUp,SkrillDeposit,NetellerSignUp,NetellerDeposit,Agents,Support,AgentList
from django.core.paginator import Paginator
from django.db.models import Q
import datetime


# Search methods
def index(request,page,subpage):
    if request.session['agent_username']:

        if page == 'neteller':
            subpage_is = None
            neteller_deposits = None
            neteller_signups = None
            neteller_earnings = 0
            neteller_counts = 0
            neteller_applications = None
            neteller_acc_upgrade_status = None
            netellerID_groupBy = None
            siteID_groupBy = None

            if subpage == 'deposits':
                subpage_is = 'deposits'
                neteller_deposits, neteller_counts,neteller_earnings, netellerID_groupBy,siteID_groupBy \
                    = netellerDepositsFetch(request)



            elif subpage == 'applications':
                subpage_is = 'applications'
                neteller_applications = netellerApplications(request)

                if request.method == "POST" and request.POST.get("net_send_viopreq") == "net_send_vipreq_val":
                    netelelr_acc = request.POST.get('vipreq_neteller_acc')
                    neteller_acc_upgrade_status = vipAccReqHandle(netelelr_acc)

            elif subpage == 'registrations':
                subpage_is = 'registrations'
                neteller_signups = netellerSignupsFetch(request)


            context = {
                "isact_stats": "active",
                "netellerbuttionactive": "background: #DCDFFF;",
                "subpage_is": subpage_is,
                'page_is': page,
                'neteller_deposits': neteller_deposits,
                'neteller_earnings': neteller_earnings,
                'neteller_counts': neteller_counts,
                'neteller_applications': neteller_applications,
                'neteller_signups': neteller_signups,
                'neteller_acc_upgrade_status': neteller_acc_upgrade_status,
                "netellerID_groupBy": netellerID_groupBy,
                "siteID_groupBy":siteID_groupBy
            }

        elif page == 'skrill':
            context = {
                "isact_stats": "active",
                "skrillbuttionactive": "background: #DCDFFF;"
            }

        else:
            context = {}
        return render(request, 'agenttemplates/stats/index.html', context)



    else:
        return redirect('login')




def netellerDepositsFetch(request):
    agent = request.session['agent_username']

    if agent:
        netellerID_groupBy = None
        siteID_groupBy = None

        siteids = SiteIdAssign.objects.filter(
            username= agent, idsource='neteller'
        ).values('site_id')

        ## neteller filteringh
        if request.method == "POST" and request.POST.get("netteller_filtering") == "neteller_filtered":
            netellerid = request.POST.get("sb_net_netellerid")
            netidgroupby = request.POST.get("sb_net_groupby")
            datefrom_pre = request.POST.get("sb_net_datefrom")
            dateto_pre = request.POST.get("sb_net_dateto")
            siteid = (request.POST.get("sb_net_siteid"))
            siteidGroupBy = request.POST.get("sb_siteidgroupby")

            datefrom = datetime.datetime.strptime(datefrom_pre, '%Y-%m-%d')
            dateto = datetime.datetime.strptime(dateto_pre, '%Y-%m-%d')
            print('netteller_filtering', netellerid, netidgroupby, datefrom, dateto, siteid, siteidGroupBy)


            if netidgroupby == "on":
                data = NetellerDeposit.objects.filter(Site_ID__in=siteids, Date__gte=datefrom,Date__lte=dateto).values('Neteller_ID').\
                                                        annotate(DepositeCounts=Count('Neteller_ID'), FinalCommssion=Sum('FinalCommssion'),
                                                                 Deposite=Sum("Deposite")).values('Neteller_ID', 'DepositeCounts',
                                                                            'Deposite','FinalCommssion').order_by('-FinalCommssion')

                netellerID_groupBy = "Values Received"

            elif siteidGroupBy == "on":
                data = NetellerDeposit.objects.filter(Site_ID__in=siteids, Date__gte=datefrom,Date__lte=dateto).values('Site_ID').\
                    annotate(FinalCommssion=Sum('FinalCommssion'),Deposite=Sum("Deposite")).values('Site_ID',
                                                                'Deposite','FinalCommssion').order_by('-Deposite')

                siteID_groupBy = "Values Received"


            else:
                data = NetellerDeposit.objects.filter(
                    Q(Site_ID__in=siteids) &
                    Q(Date__gte=datefrom) &
                    Q(Date__lte=dateto) &
                    Q(Neteller_ID__icontains=netellerid) &
                    Q(Site_ID__icontains=siteid)
                )


            counts = data.count()
            earnings = data.aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']

        else:
            data = NetellerDeposit.objects.filter(Site_ID__in=siteids)
            counts = data.count()
            earnings = data.aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']

        paginator = Paginator(data, 500)  # Show 25 contacts per page
        page = request.GET.get('page')
        all_data = paginator.get_page(page)


        return all_data, counts, earnings, netellerID_groupBy, siteID_groupBy
    else:
        return redirect('login')


def netellerSignupsFetch(request):
    agent = request.session['agent_username']
    if agent:
        siteids = SiteIdAssign.objects.filter(
            username= agent, idsource='neteller'
        ).values('site_id')

        if request.method == "POST" and request.POST.get("net_reg_submit") == "net_reg_submit_val":
            net_reg_netellerid = request.POST.get("net_reg_netellerid")
            net_reg_siteid = request.POST.get("net_reg_siteid")
            net_reg_partnercode = request.POST.get("net_reg_partnercode")
            net_reg_datefrom = datetime.datetime.strptime(request.POST.get("net_reg_datefrom"), '%Y-%m-%d')
            net_reg_dateto = datetime.datetime.strptime(request.POST.get("net_reg_dateto"), '%Y-%m-%d')

            if len(net_reg_siteid) >3 and net_reg_siteid in siteids:
                siteids = [net_reg_siteid]

            data = NetellerSignUp.objects.filter(
                Q(Site_ID__in=siteids) &
                Q(Date__gte=net_reg_datefrom) &
                Q(Date__lte=net_reg_dateto) &
                Q(Neteller_ID__icontains=net_reg_netellerid) &
                Q(Partner_code__icontains=net_reg_partnercode)
            )



        else:
            data = NetellerSignUp.objects.filter(Site_ID__in=siteids).order_by("-Date")


        paginator = Paginator(data, 100)
        page = request.GET.get('page')
        all_data = paginator.get_page(page)

        return all_data
    else:
        return redirect('login')



def netellerApplications(request):
    agent = request.session['agent_username']

    if agent:
        siteids = SiteIdAssign.objects.filter(
            username= agent, idsource='neteller'
        ).values('site_id')

        if request.method == "POST" and request.POST.get("net_ap_submit") == "net_ap_submit_val":
            vipstatus = int(request.POST.get("net_ap_vipStatus"))
            net_ap_netellerid = request.POST.get("net_ap_netellerid")
            net_ap_partnercode = request.POST.get("net_ap_partnercode")
            net_ap_datefrom =  datetime.datetime.strptime(request.POST.get("net_ap_datefrom"), '%Y-%m-%d')
            net_ap_dateto =  datetime.datetime.strptime(request.POST.get("net_ap_dateto"), '%Y-%m-%d')


            data = NetellerSignUp.objects.filter(
                Q(Site_ID__in=siteids) &
                Q(VipStatusDate__gte=net_ap_datefrom) &
                Q(VipStatusDate__lte=net_ap_dateto) &
                Q(Neteller_ID__icontains=net_ap_netellerid) &
                Q(VipStatus__icontains=vipstatus) &
                Q(Partner_code__icontains=net_ap_partnercode)
            )

        else:
            data = NetellerSignUp.objects.filter(Site_ID__in=siteids)

        paginator = Paginator(data, 30)  # Show 25 contacts per page
        page = request.GET.get('page')
        all_data = paginator.get_page(page)

        return all_data
    else:
        return redirect('login')



def vipAccReqHandle(theaccc):
    result = NetellerSignUp.objects.filter(Neteller_ID=theaccc).update(VipStatus=1,VipStatusDate=datetime.datetime.now())
    if result == 1:
        return 'We have received your request for VIP Upgradation! Thank You!'
    else:
        return 'Something went wrong! Try again later!'