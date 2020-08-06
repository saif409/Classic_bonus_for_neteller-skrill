from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import test,Agents,Support,SiteIdAssign, AgentList
from.forms import createAgetns
from django.db.models import Sum
from django.contrib import messages
from agents.models import SkrillSignUp,SkrillDeposit,NetellerSignUp,NetellerDeposit,Agents,Support,AgentList, PaymentRequests
from django.core.paginator import Paginator
from django.db.models import Q
import datetime



def requestPayment(request):
    agent = request.session['agent_username']
    if agent:

        agnet = AgentList.objects.get(username=agent)
        nettellerpaymentreq_response = None

        payment_history= PaymentRequests.objects.filter(agent=agent).order_by('datecreation')

        # withdrawal neteller ammount
        if request.method == "POST":
            net_amount = request.POST.get('neteller_with_amount')
            net_email = request.POST.get('agentz_net_email')
            net_amount_dcml = float(net_amount)
            print('netterler amount for withdraweal ', net_amount_dcml)


            if net_amount_dcml > float(agnet.balance_neteller):
                nettellerpaymentreq_response = "Your do not have that amount of balance!"

            elif net_amount_dcml <= float(agnet.balance_neteller):
                duedate30 = datetime.datetime.now() + datetime.timedelta(days=30)
                net_new_bal = round(float(agnet.balance_neteller) - net_amount_dcml, 2)

                req = PaymentRequests(agent=agent,platform='Neteller',amount=net_amount_dcml,paymentPlatform="Neteller",
                                      paymentEmail=net_email,status=1, paymentDetails= '', paymentNote = '', afterPaymentNote='',
                                      afterPaymentBalance=net_new_bal,datecreation=datetime.datetime.now(),
                                      duedate=duedate30)
                req.save()

                # update balance
                AgentList.objects.filter(username=agent).update(balance_neteller=net_new_bal)

                nettellerpaymentreq_response = "We have received your withdrawal request! Thank You."



        context={
            "isact_payments":"active",
            "agent_net_bal": agnet.balance_neteller,
            "agent_skr_bal": agnet.balance_skrill,
            "agent_net_email": agnet.neteller_email,
            "agent_skr_email": agnet.skrill_email,
            'payment_history': payment_history,
            "nettellerpaymentreq_response": nettellerpaymentreq_response
        }

        return render(request, "agenttemplates/payments/req-payment.html", context)
    else:
        return redirect('login')
