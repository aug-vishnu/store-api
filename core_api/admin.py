from django.contrib import admin

# Register your models here.
# Register your models here.
from core_api.models import *


admin.site.register(ProductModel)
admin.site.register(RandomItemModel)
admin.site.register(OrderItemModel)
admin.site.register(OrderModel)
admin.site.register(CoupounModel)
