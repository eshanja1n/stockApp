from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# admin.site.register(Account)




# Register your models here.
# from stock.models import Question

# admin.site.register(Question)




class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
    