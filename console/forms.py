from django import forms

from . import models

from utils.widgets import (text_readonly_widget,boolean_readonly_widget,ReadonlyWidget)

category_readonly_widget = ReadonlyWidget(lambda value: models.CATEGORIES.get(value,''))

class PublisherEditForm(forms.ModelForm):
    category = forms.TypedChoiceField(choices=models.EDITABLE_CATEGORY_CHOICES,coerce=lambda val:int(val) if val else None)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.created:
                if "name" in self.fields :
                    self.fields["name"].widget = text_readonly_widget
                if "category" in self.fields :
                    self.fields["category"].widget = category_readonly_widget
            
    class Meta:
        model = models.Publisher
        fields = "__all__"
        widgets = {
            "comments":forms.Textarea(attrs={"style":"height:80px;width:80%"})
        }


class EventTypeEditForm(forms.ModelForm):
    category = forms.TypedChoiceField(choices=models.EDITABLE_CATEGORY_CHOICES,coerce=lambda val:int(val) if val else None)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.created:
                if "name" in self.fields:
                    self.fields["name"].widget = text_readonly_widget
                if "category" in self.fields :
                    self.fields["category"].widget = category_readonly_widget


    class Meta:
        model = models.EventType
        fields = "__all__"


class SubscriberEditForm(forms.ModelForm):
    category = forms.TypedChoiceField(choices=models.EDITABLE_CATEGORY_CHOICES,coerce=lambda val:int(val) if val else None)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.created:
                if "name" in self.fields:
                    self.fields["name"].widget = text_readonly_widget
                if "category" in self.fields :
                    self.fields["category"].widget = category_readonly_widget

    class Meta:
        model = models.Subscriber
        fields = "__all__"
        widgets = {
            "comments":forms.Textarea(attrs={"style":"height:80px;width:80%"})
        }


class SubscribedEventTypeEditForm(forms.ModelForm):
    publisher = forms.ModelChoiceField(queryset=models.Publisher.objects.filter(category__in=(models.MANAGED,models.TESTING)))
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance :
            if self.instance.created:
                if "subscriber" in self.fields:
                    self.fields["subscriber"].widget = text_readonly_widget
                if "publisher" in self.fields:
                    self.fields["publisher"].widget = text_readonly_widget
                if "event_type" in self.fields:
                    self.fields["event_type"].widget = text_readonly_widget


    class Meta:
        model = models.SubscribedEventType
        fields = "__all__"
        widgets = {
            "parameters":forms.Textarea(attrs={"style":"height:80px"})
        }

