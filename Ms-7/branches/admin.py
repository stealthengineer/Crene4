from django.contrib import admin
from .models import (Branch,
                     Leaf,
                     Topic)

# Register your models here.
admin.site.register((Branch,Leaf,Topic))