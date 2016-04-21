from chat.models import *
from django.contrib import admin


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'product', 'message', 'received_at',
                    'is_read', 'created_date', 'sender_image', 'receiver_image')
    #list_filter = ['status', 'mode']
    #search_fields = ['amount', 'bank_code', 'band_ref_number', 'pg_type']
    list_per_page = 50
    date_hierarchy = "created_date"

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('sender', 'receiver', 'product', 'message', 'received_at',
                            'is_read', 'created_date', 'sender_image', 'receiver_image')
        return self.readonly_fields

class LastActiveAdmin(admin.ModelAdmin):
    list_display = ('user', 'received_at', 'session',)
    #list_filter = ['status', 'mode']
    #search_fields = ['amount', 'bank_code', 'band_ref_number', 'pg_type']
    list_per_page = 50
    date_hierarchy = "received_at"

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'received_at', 'session',)
        return self.readonly_fields
        
# admin.site.register(ChatMessage,ChatMessageAdmin)
# admin.site.register(LastActive)
