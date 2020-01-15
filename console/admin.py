from django.contrib.admin import register, ModelAdmin, StackedInline, SimpleListFilter, TabularInline, SimpleListFilter
from django.urls import path,reverse
from django.http import HttpResponseRedirect


from .models import (Publisher,EventType,Event,Subscriber,SubscribedEventType,SubscribedEvent,EventProcessingHistory)
from .forms import (PublisherEditForm,EventTypeEditForm,SubscriberEditForm,SubscribedEventTypeEditForm)

class EventTypeInline(TabularInline):
    model = EventType
    form = EventTypeEditForm
    readonly_fields=("register_time",)
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

@register(Publisher)
class PublisherAdmin(ModelAdmin):
    list_display = ('name', 'active','register_time')
    ordering = ('name',)
    readonly_fields=("active",)

    form = PublisherEditForm
    inlines = (EventTypeInline,)

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.is_editable:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@register(Event)
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
        
        extra_context['event_dispatch_enabled'] = Event.events[0].enabled
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
        Event.events[0].enable()
        url = reverse('admin:console_event_changelist')
        return HttpResponseRedirect(url)

    def disable_dispatch_event(self,request):
        Event.events[0].disable()
        url = reverse('admin:console_event_changelist')
        return HttpResponseRedirect(url)
    


class SubscribedEventTypeInline(TabularInline):
    model = SubscribedEventType
    form = SubscribedEventTypeEditForm
    readonly_fields=("managed","active","last_dispatched_event","last_dispatched_time","register_time")
    can_delete = False
    extra = 1


@register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ('name', 'active','register_time')
    ordering = ('name',)
    readonly_fields=("active",)

    form = SubscriberEditForm

    inlines = (SubscribedEventTypeInline,)

class EventProcessingHistoryInline(TabularInline):
    model = EventProcessingHistory
    readonly_fields = ('process_host','process_pid','status','process_start_time','process_end_time','result')
    can_delete = False
    can_add = False


@register(SubscribedEvent)
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

