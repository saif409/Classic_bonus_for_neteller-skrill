
from . import adminhome as adminhome
from django.contrib import admin
from django.urls import path,include
from . import VIPAccess as vipacc
from . import Payments as paymnt
from . import NetRecPays as nrp
from django.conf import settings
from django.conf.urls.static import static
from . import AdminStats as adstats


urlpatterns = [
    path('login', adminhome.getlogin, name='login'),
    path('logout/', adminhome.getlogout, name="logout"),
    path('admin/', admin.site.urls),
    path('agents/', include('agents.urls')),
    path('admin-control/', adminhome.home, name='home'),
    path('admin-login/', adminhome.getAdminlogin, name='admin-login'),
    path('admin-logout/', adminhome.getAdminlogout, name='admin-logout'),





    path('skrill_sign_up/', adminhome.SkrillSignsUp, name="Skrillsignsup"),
    path('neteller_sign_up/', adminhome.NetellerSignsUp, name="netellersignsup"),


    path('skrill_deposite/', adminhome.SkrillDeposite, name="skrildeposite"),
    path('neteller_deposite/', adminhome.NetellerDeposite, name="netellerdeposit"),




# signup_list_start
    path('skrill_signup/', adminhome.skrillsignupslist, name='skrill_signup'),
    path('neteller_signup/', adminhome.Netellersignuplist, name='neteller_signup'),
# signup_list_end


# Deposit_list_start
    path('skrill_deposits/', adminhome.Skrilldepositlist, name='skrill_deposits'),
    path('neteller_deposits/', adminhome.Netellerdepositslist, name='neteller_deposits'),
# Deposit_list_end

# signup_search_start
    path('skrill_signup_search/', adminhome.skrilsignupsearch, name="skrillsignupsearch"),
    path('neteller_signup_search/', adminhome.netellersignupsearch, name="netellersignupsearch"),
# # signup_search_end


# deposit_search_start
    path('skrill_deposit_search/', adminhome.skrilldepositsearch, name="skrilldepositsearch"),
    path('neteller_deposit_search/', adminhome.netellerdepositsearch, name="netellerdepositsearch"),
# deposit_search_end


# user registration
 path('', adminhome.getRegister, name="userregistration"),

# agents_list
    path('Agents_list/<str:filter>', adminhome.Agentslist, name="Agents_list"),
    path('admin_support/', adminhome.getsupport, name="adminsupport"),
    path('admin_support_details/<int:id>', adminhome.GetSupportDetails, name="admin_support_details"),

# agents_profile
    path('Agents_profile/<int:id>/', adminhome.GetAgentsProfile, name="agentsprofile"),
    path('profile_edit_agent/<str:username>/', adminhome.GetAgentsProfileEdit, name="profile_edit_agent"),
    path('set-siteid/<str:agent>/', adminhome.setsiteid, name="set-siteid"),

    path('payments/<str:status>/', paymnt.payments, name="payments"),

    path('vip-accesses/<str:type>/<str:state>/', vipacc.vipaccess, name="vip-accesses"),

    path('agent-commission/', paymnt.allAgentsCommission, name="agent-commission"),

    path('revenueShare/<str:agent>', paymnt.revenueShare, name="revenueShare"),

    path('netreceivables/<str:platform>', nrp.netreceivables, name="netreceivables"),

    path('netPaybles/', nrp.netPaybles, name="netPaybles"),

    path('adminstats/<str:page>/<str:subpage>/', adstats.index, name="adminstats"),

]
