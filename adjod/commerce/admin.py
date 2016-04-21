from django.contrib import admin
from commerce.models import Order, Transaction


class OrderAdmin(admin.ModelAdmin):
    fields = ['banner', 'banner_plan']
    list_display = ('id', 'banner_name', 'banner_plan_page',)
    list_filter = ['banner__admin_status', 'banner_plan__page','banner_plan__position']
    search_fields = ['banner__user']
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('banner', 'banner_plan')
        return self.readonly_fields

    def banner_name(self, obj):
        return obj.banner.user
    banner_name.short_description = 'User'

    def banner_plan_page(self, obj):
        return obj.banner_plan.page
    banner_plan_page.short_description = 'Page'


class TransactionAdmin(admin.ModelAdmin):
    fields = ['userprofile', 'transaction_mode', 'transaction_type', 'order', 'paypal', 'account_no', 'payment_status']
    list_display = ('id', 'userprofile', 'transaction_mode', 'transaction_type', 'order', 'paypal' , 'payment_status')
    list_filter = ['transaction_mode', 'transaction_type']
    search_fields = ['userprofile__username', 'order', 'paypal']
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('userprofile', 'transaction_mode', 'transaction_type', 'order', 'paypal')
        return self.readonly_fields

    def order_id(self, obj):
        return obj.order.banner_plan
    order_id.short_description = 'Order Number'


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
