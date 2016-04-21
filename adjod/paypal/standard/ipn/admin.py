#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from paypal.standard.ipn.models import PayPalIPN

class PayPalIPNAdmin(admin.ModelAdmin):
    date_hierarchy = 'payment_date'
    fieldsets = (
        (None, {
            "fields": [
                "flag", "txn_id", "txn_type", "payment_status", "payment_date",
                "pending_reason", "mc_gross", "mc_fee",
            ]
        }),
        ("Buyer", {
            "description": "The information about the Buyer.",
            'classes': ('collapse',),
            "fields": [
                "payer_first_name", "payer_last_name", "payer_business_name", "payer_email",
                "payer_id", "payer_status",
            ]
        }),
        ("Seller", {
            "description": "The information about the Seller.",
            'classes': ('collapse',),
            "fields": [
                "business", "quantity", 
                "receiver_email", "receiver_id", "custom", 
            ]
        }),
        ("Admin", {
            "description": "Additional Info.",
            "classes": ('collapse',),
            "fields": [
                "test_ipn", "ipaddress", "query", "response", "flag_code", 
                "flag_info"
            ]
        }),
    )
    list_display = [
        "__unicode__", "flag", "flag_info", "custom", 
        "payment_status", "created_at"
    ]
    search_fields = ["txn_id", "recurring_payment_id"]


admin.site.register(PayPalIPN, PayPalIPNAdmin)