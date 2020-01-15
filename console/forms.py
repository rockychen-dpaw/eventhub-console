from django import forms

from .models import (Publisher,EventType,Subscriber,SubscribedEventType,EDITABLE_CATEGORY_CHOICES)

from utils.widgets import (text_readonly_widget,boolean_readonly_widget)

class PublisherEditForm(forms.ModelForm):
    category = forms.TypedChoiceField(choices=EDITABLE_CATEGORY_CHOICES,coerce=lambda val:int(val) if val else None)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.register_time and "name" in self.fields:
                self.fields["name"].widget = text_readonly_widget
            
    class Meta:
        model = Publisher
        fields = "__all__"


class EventTypeEditForm(forms.ModelForm):
    category = forms.TypedChoiceField(choices=EDITABLE_CATEGORY_CHOICES,coerce=lambda val:int(val) if val else None)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.name and self.instance.register_time:
                self.fields["name"].widget = text_readonly_widget


    class Meta:
        model = EventType
        fields = "__all__"


class SubscriberEditForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.name and self.instance.register_time:
                self.fields["name"].widget = text_readonly_widget

    class Meta:
        model = Subscriber
        fields = "__all__"


class SubscribedEventTypeEditForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.register_time:
                self.fields["subscriber"].widget = text_readonly_widget
                self.fields["publisher"].widget = text_readonly_widget
                self.fields["event_type"].widget = text_readonly_widget


    class Meta:
        model = SubscribedEventType
        fields = "__all__"

