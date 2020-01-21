from django.contrib.admin import register, ModelAdmin, StackedInline, SimpleListFilter, TabularInline, SimpleListFilter
from django.urls import path,reverse
from django.http import HttpResponseRedirect

from . import models
from . import forms


class EventTypeInline(TabularInline):
    model = models.EventType
    form = forms.EventTypeEditForm
    readonly_fields=("created",)
    can_delete = False
    extra = 1

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_add_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@register(models.Publisher)
class PublisherAdmin(ModelAdmin):
    list_display = ('name','category', 'active','created')
    ordering = ('name',)
    readonly_fields=("active",)

    form = forms.PublisherEditForm
    inlines = (EventTypeInline,)

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@register(models.Event)
class EventAdmin(ModelAdmin):
    list_display = ('publisher','event_type','source','payload','publish_time')

    actions = ('enable_event_dispatch',)
    change_list_template = "console/events_changelist.html"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        extra_context['event_dispatch_enabled'] = models.Event.events[0].enabled
        return super(EventAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            path('dispatch/enable', self.enable_dispatch_event,name="%s_%s_enable_dispatch_event" % info),
            path('dispatch/disable', self.disable_dispatch_event,name="%s_%s_disable_dispatch_event" % info),
        ]
        return my_urls + urls

    def enable_dispatch_event(self,request):
        models.Event.events[0].enable()
        url = reverse('admin:console_event_changelist')
        return HttpResponseRedirect(url)

    def disable_dispatch_event(self,request):
        models.Event.events[0].disable()
        url = reverse('admin:console_event_changelist')
        return HttpResponseRedirect(url)
    


class SubscribedEventTypeInline(TabularInline):
    model = models.SubscribedEventType
    readonly_fields=("active","last_dispatched_event","last_dispatched_time","created")
    can_delete = False
    extra = 1

    form = forms.SubscribedEventTypeEditForm

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_add_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@register(models.EventProcessingModule)
class EventProcessingModuleAdmin(ModelAdmin):
    list_display = ('name', 'active','created')
    ordering = ('name',)
    readonly_fields=("active",)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


@register(models.Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ('name','category', 'active','created')
    ordering = ('name',)
    readonly_fields=("active",)

    form = forms.SubscriberEditForm

    inlines = (SubscribedEventTypeInline,)

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_add_permission(self, request, obj=None):
        return True

class EventProcessingHistoryInline(TabularInline):
    model = models.EventProcessingHistory
    readonly_fields = ('process_host','process_pid','status','process_start_time','process_end_time','result')
    can_delete = False
    can_add = False


@register(models.SubscribedEvent)
class SubscribedEventAdmin(ModelAdmin):
    list_display = ('subscriber', 'publisher','event_type','event','status','process_start_time')
    readonly_fields = ('subscriber', 'publisher','event_type','event','status','process_start_time','process_end_time','result','process_host','process_pid','process_times')

    inlines = (EventProcessingHistoryInline,)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

