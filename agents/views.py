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



def agentsindex(request):
    if request.session['agent_username']:

        siteids_neteller = SiteIdAssign.objects.filter(
            username=request.session['agent_username'], idsource='neteller'
        ).values('site_id')

        siteids_skrill = SiteIdAssign.objects.filter(
            username=request.session['agent_username'], idsource='skrill'
        ).values('site_id')

        total_revenue_neteller_deposit = NetellerDeposit.objects.filter(Site_ID__in=siteids_neteller).aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']
        total_revenue_skrill_deposit = SkrillDeposit.objects.filter(Site_ID__in=siteids_skrill).aggregate(Sum('FinalCommssion'))['FinalCommssion__sum']

        #
        # # processing neteller part
        # total_revenue_neteller_deposit_pre = NetellerDeposit.objects.filter(Site_ID__in=siteids_neteller).aggregate(Sum('Profit'))['Profit__sum']
        # net_commission = AgentList.objects.get(username = request.session['agent_username'])
        # if total_revenue_neteller_deposit_pre != None:
        #     total_neteller_amount = (float(total_revenue_neteller_deposit_pre)*float(net_commission.commission))/100
        #     # updating amount to database
        #     AgentList.objects.filter(username = request.session['agent_username']).update(balance_neteller=total_neteller_amount)
        #     total_revenue_neteller_deposit = AgentList.objects.get(username = request.session['agent_username']).balance_neteller
        # else:
        #     total_revenue_neteller_deposit = 0
        #
        #
        #
        # # processing skrill part
        # total_revenue_skrill_deposit_pre = SkrillDeposit.objects.filter(Site_ID__in=siteids_skrill).aggregate(Sum('Profit'))['Profit__sum']
        # skr_commission = AgentList.objects.get(username = request.session['agent_username'])
        # if total_revenue_skrill_deposit_pre != None:
        #     total_skrill_amount = (float(total_revenue_skrill_deposit_pre)*float(skr_commission.commission))/100
        #     # updating amount to database
        #     AgentList.objects.filter(username=request.session['agent_username']).update(
        #         balance_skrill=total_skrill_amount)
        #     total_revenue_skrill_deposit = AgentList.objects.get(
        #         username=request.session['agent_username']).balance_skrill
        # else:
        #     total_revenue_skrill_deposit = 0
        #



        total_skrill_signups = SkrillSignUp.objects.filter(Site_ID__in=siteids_skrill).count()
        total_neteller_signups = NetellerSignUp.objects.filter(Site_ID__in=siteids_neteller).count()

        context = {
            "total_revenue_skrill_deposit": total_revenue_skrill_deposit,
            "total_revenue_neteller_deposit": total_revenue_neteller_deposit,
            'isact_dashboard': 'active',
            'total_skrill_signups': total_skrill_signups,
            'total_neteller_signups': total_neteller_signups

        }
        return render(request, 'agenttemplates/dash.html', context)
    else:

        return redirect('login')



def getProfile(request):
    agentusername = request.session['agent_username']
    if agentusername:
        agents_profile = get_object_or_404(AgentList, username=request.session['agent_username'])

        if request.method == "POST":
            update_fname = request.POST.get('update_firstname')
            update_lname = request.POST.get('update_lastname')
            update_email = request.POST.get('update_email')
            update_contactno = request.POST.get('update_contactno')
            update_newpass = request.POST.get('update_newpass')

            update_neteller_email = request.POST.get('update_neteller_email')
            update_skrill_email = request.POST.get('update_skrill_email')
            update_address = request.POST.get('update_address')
            update_city = request.POST.get('update_city')
            update_country = request.POST.get('update_country')
            update_telegram = request.POST.get('update_telegram')
            update_facebook = request.POST.get('update_facebook')
            update_skype = request.POST.get('update_skype')

            print('Agent profiel data', update_neteller_email,update_skrill_email, update_address, update_city,
            update_country, update_telegram, update_facebook, update_skype)


            returns = AgentList.objects.filter(username=agentusername).update(fname=update_fname,
                                                                         lname=update_lname,
                                                                         email=update_email,
                                                                         phone=update_contactno,
                                                                         password=update_newpass,
                                                                        neteller_email = update_neteller_email,
                                                                              skrill_email = update_skrill_email,
                                                                              address = update_address,
                                                                              city = update_city,
                                                                              country = update_country,
                                                                              telegram = update_telegram,
                                                                              facebook = update_facebook,
                                                                              skype = update_skype

                                                                         )

            if returns:
                userupdateresponse = 'Successfully Updated!'
            else:
                userupdateresponse = 'Update failed!'

            singleUser = AgentList.objects.get(username=agentusername)

            return render(request,
                          'agenttemplates/profile/agents_profile.html',
                          {'agents_profile': singleUser, 'userupdateresponse': userupdateresponse})




        return render(request, 'agenttemplates/profile/agents_profile.html',
                      {"agents_profile": agents_profile, 'isact_profile': 'active'})
    else:
        return redirect('login')




def AgentsSupport(request):
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            user = Support(agents_name =name, agents_email=email, subject=subject, message=message)
            user.save()
            messages.add_message(request, messages.INFO, 'Your message has been send to our support team please wait for our response !!')
            return redirect('support')
        return render(request, "agenttemplates/supportagents.html")



def ViewDataAgents(request, agents_name):
    post_author = get_object_or_404(User, username=agents_name)
    auth = get_object_or_404(Agents, name=post_author.id)
    post = SiteIdAssign.objects.filter(username=auth.id)
    context={
        "auth":auth,
        "post":post
    }
    return render(request, "agenttemplates/viewdata.html", context)







def inviteagent(request):
    if request.session['agent_username']:


        context = {
            'isact_invite': 'active',

        }
        return render(request, 'agenttemplates/inviteagent.html', context)
    else:

        return redirect('login')



def smssettings(request):
    if request.session['agent_username']:


        context = {
            'isact_sms': 'active',

        }
        return render(request, 'agenttemplates/smssettings.html', context)
    else:

        return redirect('login')


