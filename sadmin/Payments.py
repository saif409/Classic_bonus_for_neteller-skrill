from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from agents.models import SkrillSignUp,SkrillDeposit,NetellerSignUp,NetellerDeposit,\
    Agents,Support,AgentList, SiteIdAssign, AllAgentsCommission,PaymentRequests
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
# from agents.forms import agentprofileedit
from django.db.models import Q
from django.db.models import Sum
from django.core.paginator import Paginator
import csv, io
import datetime
from django.db import models


def payments(request, status):

    if status == 'upcoming':
        allpayments = PaymentRequests.objects.filter(status=1)
    elif status == 'paid':
        allpayments = PaymentRequests.objects.filter(status=2)
    elif status == 'declined':
        allpayments = PaymentRequests.objects.filter(status=3)
    else:
        allpayments = PaymentRequests.objects.all()

    # Making Payment
    makePaymentReq = None
    if request.method == "POST":
        paymentdetails = request.POST.get('paymentdetails')
        paymentid = request.POST.get('paymentid')

        req = PaymentRequests.objects.filter(id=paymentid)
        req.update(afterPaymentNote=paymentdetails, status=2)
        makePaymentReq = "Payment request processed successfully!"


    context = {

        'isact_payments': 'active',
        'allpayments': allpayments,
        'makePaymentReq': makePaymentReq
    }

    return render(request, 'sadmintemplates/payments.html',context)



def allAgentsCommission(request):

    # Model AllAgentsCommission
    if request.user.is_authenticated:
        alldata = AllAgentsCommission.objects.all()
        message = None

        if request.method == "POST":
            commissionamount = float(request.POST.get('commissionamount'))
            admin_commissionamount = float(request.POST.get('admin_commissionamount'))
            applyrules = request.POST.get('applyrules')
            activationdate_html = request.POST.get('activationdate')
            # HTML input is YYYY-MM-DAY, model input is "2020-01-18" YYYY-MM-DAY

            #if activationdate == "2020-01-18":
            activationdate = datetime.datetime.strptime(activationdate_html, '%Y-%m-%d')
            # print(activationdate)
            # print('Activation date', activationdate,)
            # for i in NetellerDeposit.objects.filter(Date__gte=activationdate):
            #     print('Hola', i.Date)


            if applyrules == "on":
                rule = "All"
            else:
                rule = "Custom"

            insert = AllAgentsCommission(
                username=request.user,
                adminCommissionIn1K=admin_commissionamount,
                commission=commissionamount,
                applyrules=rule,
                activationDate = activationdate,
                updated=datetime.datetime.now())

            insert.save()
            message = 'Agent Payment Rule Added Successfully!'

            # Call method to change current database
            applyCommissionRules()

            message = 'Agent Payment Rule Added & Applied Successfully!'


        context = {

            'isact_agentscomission': 'active',
            'alldata': reversed(alldata),
            'comissionrulemessage': message,
            'lastest': AllAgentsCommission.objects.last()

        }

        return render(request, 'sadmintemplates/settings/agentpayments.html',context)

    else:
        return redirect('admin-login')



def applyCommissionRules():
    lastRule = AllAgentsCommission.objects.last()

    if lastRule.applyrules == "Custom":
        # this will skip all custom fields
        ndeps = NetellerDeposit.objects.filter(AgentProfitType="All",Date__gte=lastRule.activationDate)
        ndeps.update(AgentProfitType="All", AgentProfit=lastRule.commission,
                     AdminProfitIn1K=lastRule.adminCommissionIn1K)

        for eachDeposit in ndeps:
            if (float(eachDeposit.Profit)*1000)/float(eachDeposit.Deposite) < float(lastRule.commission):
                eachDeposit.FinalCommssion = (float(eachDeposit.Profit)/float(lastRule.adminCommissionIn1K))*float(lastRule.commission)
                eachDeposit.save()
            else:
                eachDeposit.FinalCommssion = float(eachDeposit.Deposite)*(float(lastRule.commission)/1000)
                eachDeposit.save()


        sdeps = SkrillDeposit.objects.filter(AgentProfitType="All",Date__gte=lastRule.activationDate)
        sdeps.update(AgentProfitType="All", AgentProfit=lastRule.commission,
                     AdminProfitIn1K=lastRule.adminCommissionIn1K)

        for eachSDeposit in sdeps:
            if (float(eachSDeposit.Profit)*1000)/float(eachSDeposit.Deposite) < float(lastRule.commission):
                eachSDeposit.FinalCommssion = (float(eachSDeposit.Profit)/float(lastRule.adminCommissionIn1K))*float(lastRule.commission)
                eachSDeposit.save()
            else:
                eachSDeposit.FinalCommssion = float(eachSDeposit.Deposite)*(float(lastRule.commission)/1000)
                eachSDeposit.save()

        # Updating Agents payment rules
        nagents = AgentList.objects.filter(commissionType="All")
        nagents.update(commissionType="All", commission=lastRule.commission,AdminProfitIn1K=lastRule.adminCommissionIn1K)

    elif lastRule.applyrules == "All":
        ndeps = NetellerDeposit.objects.filter(Date__gte=lastRule.activationDate)
        ndeps.update(AgentProfitType="All",AgentProfit = lastRule.commission,
                     AdminProfitIn1K=lastRule.adminCommissionIn1K)

        for eachDeposit in ndeps:
            if (float(eachDeposit.Profit)*1000)/float(eachDeposit.Deposite) < float(lastRule.commission):
                eachDeposit.FinalCommssion = (float(eachDeposit.Profit)/float(lastRule.adminCommissionIn1K))*float(lastRule.commission)
                eachDeposit.save()
            else:
                eachDeposit.FinalCommssion = float(eachDeposit.Deposite)*(float(lastRule.commission)/1000)
                eachDeposit.save()


        sdeps = SkrillDeposit.objects.filter(Date__gte=lastRule.activationDate)
        sdeps.update(AgentProfitType="All", AgentProfit=lastRule.commission,
                     AdminProfitIn1K=lastRule.adminCommissionIn1K)

        for eachSDeposit in sdeps:
            if (float(eachSDeposit.Profit)*1000)/float(eachSDeposit.Deposite) < float(lastRule.commission):
                eachSDeposit.FinalCommssion = (float(eachSDeposit.Profit)/float(lastRule.adminCommissionIn1K))*float(lastRule.commission)
                eachSDeposit.save()
            else:
                eachSDeposit.FinalCommssion = float(eachSDeposit.Deposite)*(float(lastRule.commission)/1000)
                eachSDeposit.save()


        # Updating Agents payment rules
        nagents = AgentList.objects.filter(commissionType="All")
        nagents.update(commissionType="All", commission=lastRule.commission,
                       AdminProfitIn1K=lastRule.adminCommissionIn1K)


def revenueShare(request, agent):
    if request.user.is_authenticated:
        # withdrawal neteller ammount
        singleUser = AgentList.objects.get(username=agent)
        responseupdate = None
        if request.method == "POST":

            update_activationdatecustom = request.POST.get('activationdatecustom')
            update_commission = float(request.POST.get('update_commission'))
            update_cb_commission = float(request.POST.get('update_cb_commission'))
            activationdate_gnt = datetime.datetime.strptime(update_activationdatecustom, '%Y-%m-%d')



            updts = AgentList.objects.filter(username=agent).update(RevShareCB=update_cb_commission,
                                                                    RevShareAgent=update_commission,
                                                                    RevShareActDate=activationdate_gnt,
                                                                    commissionType="Custom"
                                                                    )

            ##Update neteller/deposits , skrill/deoposits
            applyCustomCommissionRules(activationdate_gnt, update_commission, update_cb_commission,agent)

            if updts:
                responseupdate = "Successfully Update!"
            else:
                responseupdate = "Update Failed!"


        context = {
            "isact_agents": "active",
            "singleUser": singleUser,
            "responseupdate": responseupdate
        }

        return render(request, "sadmintemplates/admin_agents/revenue-share.html", context)
    else:
        return redirect('admin-login')


def applyCustomCommissionRules(thedate, commission, cb_commission,agent):

    siteids_neteller = SiteIdAssign.objects.filter(
        username=agent, idsource='neteller'
    ).values('site_id')

    siteids_skrill = SiteIdAssign.objects.filter(
        username=agent, idsource='skrill'
    ).values('site_id')


    ndeps = NetellerDeposit.objects.filter(Site_ID__in=siteids_neteller,Date__gte=thedate)
    for itemn in ndeps:
        itemn.AgentProfitType = "Custom"
        itemn.FinalCommssion = (float(itemn.Profit)/cb_commission)*commission
        itemn.save()


    sdeps = SkrillDeposit.objects.filter(Site_ID__in=siteids_skrill, Date__gte=thedate)
    for items in sdeps:
        items.AgentProfitType = "Custom"
        items.FinalCommssion = (float(items.Profit) / cb_commission) * commission
        items.save()

    #now update the balances
    AgentList.objects.filter(username=agent).update(
        balance_neteller=float(NetellerDeposit.objects.filter(Site_ID__in=siteids_neteller).aggregate(Sum('FinalCommssion'))['FinalCommssion__sum'])
        ,balance_skrill=float(SkrillDeposit.objects.filter(Site_ID__in=siteids_skrill).aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']))




