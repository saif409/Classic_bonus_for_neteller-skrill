from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from agents.models import SkrillSignUp,SkrillDeposit,NetellerSignUp,NetellerDeposit,Agents,Support,AgentList, SiteIdAssign,NetReceiables, PaymentRequests
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.core.paginator import Paginator
import csv, io
import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count



def netreceivables(request,platform):

    if request.user.is_authenticated:

        total_revenue_skrill_deposit = SkrillDeposit.objects.aggregate(Sum('Profit'))['Profit__sum']
        total_revenue_neteller_deposit = NetellerDeposit.objects.aggregate(Sum('Profit'))['Profit__sum']

        netellerMonthly = NetellerDeposit.objects.annotate(month=TruncMonth('Date')).\
            values('month').annotate(c=Sum('Profit'),d=Sum('Deposite')).values('month', 'c','d').order_by('-month')

        skrillMonthly = SkrillDeposit.objects.annotate(month=TruncMonth('Date')).\
            values('month').annotate(c=Sum('Profit'),d=Sum('Deposite')).values('month', 'c','d').order_by('-month')

        responsetext = None
        current_net_balance = 0.00
        current_skr_balance = 0.00
        net_rcv = 0.0


        net_rcv_total = 0.0
        for entry in NetReceiables.objects.filter(platform=platform):
            net_rcv_total = net_rcv_total+float(entry.amount)



        if platform == "Skrill":
            skrillbuttionactive=  "background: #DCDFFF;"
            netellerbuttionactive = None
            current_skr_balance = float(total_revenue_skrill_deposit) - net_rcv_total
            net_rcv = NetReceiables.objects.filter(platform="Skrill").order_by("-datecreation")

            if request.method == "POST" and request.POST.get('platform') == "Skrill":
                amount = float(request.POST.get('skrill_amount'))
                platform = request.POST.get('platform')
                NetReceiables(platform=platform, amount=amount, datecreation=datetime.datetime.now()).save()
                responsetext = "Successfully Added!"

        elif platform == "Neteller":
            netellerbuttionactive = "background: #DCDFFF;"
            skrillbuttionactive = None
            current_net_balance = float(total_revenue_neteller_deposit) - net_rcv_total
            net_rcv = NetReceiables.objects.filter(platform="Neteller").order_by("-datecreation")

            if request.method == "POST" and request.POST.get('platform') == "Neteller":
                amount = float(request.POST.get('neteller_amount'))
                platform = request.POST.get('platform')
                NetReceiables(platform=platform, amount=amount, datecreation=datetime.datetime.now()).save()
                responsetext = "Successfully Added!"

        context = {
            "isact_netreceivables": "active",
            "netellerMonthly": netellerMonthly,
            "skrillMonthly": skrillMonthly,
            "total_revenue_skrill_deposit": total_revenue_skrill_deposit,
            "total_revenue_neteller_deposit": total_revenue_neteller_deposit,
            'responsetext': responsetext,
            'net_rcv_all': net_rcv,
            'net_rcv_total': net_rcv_total,
            "current_net_balance": current_net_balance,
            "current_skr_balance": current_skr_balance,
            "netellerbuttionactive": netellerbuttionactive,
            "skrillbuttionactive": skrillbuttionactive,
            'platform': platform

        }
        return render(request, 'sadmintemplates/net/rcvls.html', context)
    else:
        return redirect('admin-login')



def netPaybles(request):

    netellerMonthlyPayables = NetellerDeposit.objects.annotate(month=TruncMonth('Date')). \
        values('month').annotate(c=Sum('FinalCommssion'), d=Sum("Deposite")).values('month', 'c', 'd').order_by('-month')

    skrillMonthlyPayables = SkrillDeposit.objects.annotate(month=TruncMonth('Date')). \
        values('month').annotate(c=Sum('FinalCommssion'), d=Sum("Deposite")).values('month', 'c', 'd').order_by('-month')


    #total balance
    net_rcv_total = round(float(NetellerDeposit.objects.aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']),2)
    skr_rcv_total = round(float(SkrillDeposit.objects.aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']),2)

    #Already Paid
    net_already_paid = 0.0
    for entry in PaymentRequests.objects.filter(platform="Neteller", status=2):
        net_already_paid = net_already_paid + float(entry.amount)

    skr_already_paid = 0.0
    for entry in PaymentRequests.objects.filter(platform="Skrill", status=2):
        skr_already_paid = skr_already_paid + float(entry.amount)

    # current balance
    net_cur_bal = round(net_rcv_total-net_already_paid,2)
    skr_cur_bal = round(skr_rcv_total-skr_already_paid,2)

    context = {
        "isact_NetPayables": "active",
        "bothSNLists": zip(netellerMonthlyPayables, skrillMonthlyPayables),
        "net_rcv_total": round(net_rcv_total,2),
        "skr_rcv_total": round(skr_rcv_total,2),
        "net_already_paid": net_already_paid,
        "skr_already_paid": skr_already_paid,
        "net_cur_bal": net_cur_bal,
        "skr_cur_bal": skr_cur_bal

    }

    if request.user.is_authenticated:
        return render(request, 'sadmintemplates/net/paybls.html', context)
    else:
        return redirect('admin-login')
