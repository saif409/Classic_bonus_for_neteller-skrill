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



def vipaccess(request, type, state):

    vipaccessdata = None

    thestate = 4
    if state == "Pending":
        thestate = 1
    elif state == "Approved":
        thestate = 2
    elif state == "Rejected":
        thestate = 3

    if type == "NETELLER":
        vipaccessdata = NetellerSignUp.objects.filter(VipStatus=thestate)

    elif type == "SKRILL":
        vipaccessdata = SkrillSignUp.objects.filter(VipStatus=thestate)

    context = {
        'isact_vipaccess': 'active',
        'filter': state,
        'type': type,
        'vipaccessdata': vipaccessdata
    }

    return render(request, 'sadmintemplates/vipaccess.html',context)