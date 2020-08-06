from django.contrib import admin
from .models import Agents,NetellerDeposit,SkrillDeposit,Support,SkrillSignUp,NetellerSignUp,SiteIdAssign

# Register your models here.
admin.site.register(Agents)
admin.site.register(NetellerDeposit)
admin.site.register(SkrillDeposit)
admin.site.register(Support)
admin.site.register(SkrillSignUp)
admin.site.register(NetellerSignUp)
admin.site.register(SiteIdAssign)


