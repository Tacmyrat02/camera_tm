from django.contrib import admin
from .models import IPCamera , Switch,NVR,HardDisk

admin.site.register(IPCamera)

admin.site.register(Switch)
admin.site.register(HardDisk)
admin.site.register(NVR)