
from django.contrib import admin
from django.urls import path
from.import views, MyData as mydadta
from . import Stats as stats
from . import AgentPayments as agntpays

urlpatterns = [

    path('', views.agentsindex, name="agentshome"),
    path('profile/', views.getProfile, name="profile"),
    path('stats/<str:page>/<str:subpage>/', stats.index, name="stats"),
    path('payreq/', agntpays.requestPayment, name="payreq"),
    path('viewdata/<str:agents_name>', views.ViewDataAgents, name="viewdata"),
    path('support/', views.AgentsSupport , name="support"),
    path('agent-net-dep-search/', mydadta.netellerdepositsearch , name="agent-net-dep-search"),
    path('agent-skrill-dep-search/', mydadta.skrilldepositsearch , name="agent-skrill-dep-search"),
    path('agent-net-signgup-search/', mydadta.netellersignupsearch , name="agent-net-signgup-search"),
    path('agent-skrill-signup-search/', mydadta.skrilsignupsearch , name="agent-skrill-signup-search"),

    path('mylinks/', mydadta.mylinks, name="mylinks"),
    path('inviteagent/', views.inviteagent, name="inviteagent"),
    path('sms-settings/', views.smssettings, name="sms-settings"),
    path('mydata/', mydadta.mydatas, name="mydata"),

]