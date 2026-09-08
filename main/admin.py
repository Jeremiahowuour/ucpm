import csv
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    Leader, Milestone, Value, Region, Event, EventRegistration, 
    Resource, ChapterReport, ContactMessage, DailyPrayerFocus, 
    Testimony, SiteStatistic, RegionalCoordinator, FAQ, 
    NewsletterSubscriber, NewsletterCampaign
)

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order')
    list_editable = ('order',)

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order')
    list_editable = ('order',)

@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'date', 'location', 'order')
    list_filter = ('region', 'date')
    search_fields = ('title', 'location', 'region__name')
    list_editable = ('order',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'institution_name', 'delegation_size', 'phone_number', 'registered_at')
    list_filter = ('event', 'institution_name')
    search_fields = ('full_name', 'institution_name', 'phone_number')

    actions = []
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_as_csv), name='main_eventregistration_export_csv'),
        ]
        return custom_urls + urls

    def export_as_csv(self, request):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in self.model.objects.all():
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at', 'order')
    search_fields = ('title', 'category', 'description')
    list_filter = ('category', 'uploaded_at')

@admin.register(ChapterReport)
class ChapterReportAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'secretary_name', 'email', 'submitted_at', 'file_download')
    list_filter = ('institution_name', 'submitted_at')
    search_fields = ('institution_name', 'secretary_name', 'email', 'testimony_notes')
    readonly_fields = ('submitted_at', 'file_download')
    
    actions = ['delete_selected']

    def file_download(self, obj):
        if obj.report_file:
            return format_html('<a href="{}" target="_blank" class="button">Download File</a>', obj.report_file.url)
        return "No File Uploaded"
    file_download.short_description = 'Report Document'

@admin.register(DailyPrayerFocus)
class DailyPrayerFocusAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_editable = ('is_active',)

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_role', 'is_approved')
    list_filter = ('is_approved',)

@admin.register(SiteStatistic)
class SiteStatisticAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteStatistic.objects.exists()

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'inquiry_type', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'inquiry_type', 'created_at')
    search_fields = ('full_name', 'email', 'message')
    list_editable = ('is_resolved',)

@admin.register(RegionalCoordinator)
class RegionalCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'coordinator_name', 'phone_number', 'email', 'order')
    list_editable = ('order',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    actions = ['send_quick_email']

    @admin.action(description="Send quick notice to selected subscribers")
    def send_quick_email(self, request, queryset):
        recipient_list = list(queryset.filter(is_active=True).values_list('email', flat=True))
        if not recipient_list:
            self.message_user(request, "No active subscribers selected.", level=messages.WARNING)
            return
        self.message_user(
            request, 
            f"Targeting {len(recipient_list)} selected subscriber(s). (To write full emails, use Newsletter Campaigns).", 
            level=messages.INFO
        )

@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent_at', 'created_at')
    readonly_fields = ('sent_at', 'created_at')
    actions = ['send_to_all_active']

    @admin.action(description="Send this campaign to ALL active subscribers")
    def send_to_all_active(self, request, queryset):
        active_subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        recipient_list = list(active_subscribers.values_list('email', flat=True))

        if not recipient_list:
            self.message_user(request, "No active subscribers found to send the newsletter to.", level=messages.WARNING)
            return

        success_count = 0
        for campaign in queryset:
            if campaign.sent_at:
                self.message_user(request, f"Campaign '{campaign.subject}' was already sent previously.", level=messages.WARNING)
                continue

            try:
                send_mail(
                    subject=campaign.subject,
                    message=campaign.content,
                    from_email=None, 
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                campaign.sent_at = timezone.now()
                campaign.save()
                success_count += 1
            except Exception as e:
                self.message_user(request, f"Error sending campaign: {e}", level=messages.ERROR)
                return

        if success_count > 0:
            self.message_user(request, f"Successfully sent newsletter to {len(recipient_list)} subscribers!", level=messages.SUCCESS)