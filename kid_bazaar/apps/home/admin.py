from django.contrib import admin
from .models import Kid, Item, ItemRequest, KBUser

admin.site.register(Kid)
admin.site.register(Item)
admin.site.register(ItemRequest)
admin.site.register(KBUser)

