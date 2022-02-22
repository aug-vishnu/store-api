from django.contrib import admin
from django.contrib.auth.models import Group
from auth_api.models import *
from core_api.models import *


# Register your models here.

admin.site.register(SubadminPermisionModel)
admin.site.register(Account)
admin.site.register(AdminModel)
admin.site.register(SubAdminModel)
admin.site.register(ShopModel)
admin.site.register(ShopPermissionModel)
admin.site.register(CustomerModel)
admin.site.register(BlendingOptionsModel)

admin.site.register(ForgotTokenModel)

admin.site.unregister(Group)