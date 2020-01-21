import traceback

from django.db import models,connection
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from smart_selects.db_fields import ChainedForeignKey

import reversion

from utils import cachedclassproperty,classproperty
from project import loginuser

PROGRAMMATIC = 1
MANAGED = 2
SYSTEM = 999
TESTING = -1
UNITESTING = -2
    
CATEGORY_CHOICES = (
    (PROGRAMMATIC,"Programmatic"),
    (MANAGED,"Managed"),
    (SYSTEM,"System"),
    (TESTING,"Testing"),
    (UNITESTING,"Unitesting")
)

CATEGORIES = dict(CATEGORY_CHOICES)

EDITABLE_CATEGORY_CHOICES = (
    (MANAGED,"Managed"),
    (TESTING,"Testing")
)

try:
    User.PROGRAMMATIC,created = User.objects.get_or_create(username="Programattic",defaults={
        'password':'',
        'is_superuser':False,
        'is_staff':False,
        'first_name':'Programmatic',
        'last_name':'',
        'email':'',
    })
except:
    pass

class ModelEventMixin(object):
    @cachedclassproperty
    def events(cls):
        return None

class ModelEvent(object):
    """
    actions: table actions, a list of INSERT, UPDATE ,or DELETE
    table_name: table name
    event_name: event name
    payloads: the sql to return the payloads. default is "SELECT NEW.* "
    """
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELTE'

    EVENT_FUNC = """
    CREATE FUNCTION {funcname}() RETURNS trigger as $$
    DECLARE
      payload text;
    BEGIN
      payload := row_to_json(tmp)::text FROM ({payload}) tmp;
    
      PERFORM pg_notify({eventcolumn}, payload);

      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    CONDITIONAL_EVENT_FUNC = """
    CREATE FUNCTION {funcname}() RETURNS trigger as $$
    DECLARE
      payload text;
    BEGIN
      IF {condition} THEN
        payload := row_to_json(tmp)::text FROM ({payload}) tmp;
    
        PERFORM pg_notify({eventcolumn}, payload);
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    EVENT_TRIGGER = """
    CREATE TRIGGER {triggername}
    AFTER {actions}
    ON {tablename}
    FOR EACH ROW EXECUTE PROCEDURE {funcname}();
    """

    def __init__(self,model,actions,name=None,payload=None,condition=None,event_column=None):
        self.model = model
        self.name = name or "event"
        self.actions = actions
        self.condition = condition
        self.payload = payload or "SELECT NEW.*"
        self.event_column = event_column or name or self.table_name.lower()

    @property
    def table_name(self):
        return self.model._meta.db_table

    @property
    def is_active(self):
        return True

    @property
    def triggername(self):
        return "{}_{}_trig".format(self.table_name,self.name)

    @property
    def funcname(self):
        return "{}_{}_func".format(self.table_name,self.name)


    @property
    def event_func(self):
        if self.condition:
            return self.CONDITIONAL_EVENT_FUNC.format(tablename=self.table_name,name=self.name,payload=self.payload,eventcolumn = self.event_column,condition = self.condition,funcname=self.funcname)
        else:
            return self.EVENT_FUNC.format(tablename=self.table_name,name=self.name,payload=self.payload,eventcolumn = self.event_column,funcname=self.funcname)

    @property
    def event_trigger(self):
        return self.EVENT_TRIGGER.format(tablename=self.table_name,actions=" OR ".join(self.actions),name=self.name,funcname=self.funcname,triggername=self.triggername)

    @property
    def enabled(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(1) FROM pg_trigger WHERE tgname = '{}'".format(self.triggername))
            row = cursor.fetchone()
            return row[0] > 0


    def enable(self):
        #drop the func and trigger first
        self.disable()
        with connection.cursor() as cursor:
            cursor.execute(self.event_func)
            print(self.event_trigger)
            cursor.execute(self.event_trigger)

    def disable(self):
        with connection.cursor() as cursor:
            cursor.execute("DROP TRIGGER IF EXISTS {tablename}_{name}_trig ON {tablename} ".format(tablename=self.table_name,name=self.name))
            cursor.execute("DROP FUNCTION IF EXISTS {tablename}_{name}_func".format(tablename=self.table_name,name=self.name))

class AuditModel(models.Model):
    creator = models.ForeignKey(User,null=False,on_delete=models.PROTECT,editable=False,related_name='+')
    created = models.DateTimeField(auto_now_add=timezone.now)
    modifier = models.ForeignKey(User,null=False,on_delete=models.PROTECT,editable=False,related_name='+')
    modified = models.DateTimeField(auto_now=timezone.now)

    class Meta(object):
        abstract = True

class ActiveModel(AuditModel):
    active = models.BooleanField(editable=False,default=True)
    active_modifier = models.ForeignKey(User,null=False,on_delete=models.PROTECT,editable=False,related_name='+')
    active_modified = models.DateTimeField(null=True,editable=False)

    class Meta(object):
        abstract = True

class Publisher(ActiveModel):
    name = models.CharField(max_length=32,null=False,primary_key=True)
    category = models.SmallIntegerField(default=MANAGED,choices=CATEGORY_CHOICES)
    comments = models.TextField(null=True)


    @property
    def is_system_publisher(self):
        return self.category == SYSTEM

    @property
    def is_editable(self):
        return self.category in (MANAGED,TESTING)

    def __str__(self):
        return self.name

    class Meta(object):
        db_table = "publisher"

try:
    Publisher.EVENTHUB_CONSOLE = Publisher.objects.get_or_create(name="EventHubConsole",defaults={
        'comments':"Used by event hub console to manage publishers and subscribers",
        'category':SYSTEM,
        'active':True,
        'active_modifier':User.PROGRAMMATIC,
        'active_modified':timezone.now(),
        'creator':User.PROGRAMMATIC,
        'modifier':User.PROGRAMMATIC
    })[0]
except:
    traceback.print_exc()
    pass

class EventType(ActiveModel):
    name = models.CharField(max_length=32,null=False,primary_key=True)
    publisher = models.ForeignKey(Publisher,null=False,related_name="event_types",on_delete=models.PROTECT)
    category = models.SmallIntegerField(default=MANAGED,choices=CATEGORY_CHOICES)
    comments = models.TextField(null=True,blank=True)
    sample = JSONField(null=True,blank=True)

    @property
    def is_system_event_type(self):
        return self.publisher.is_system_publisher

    @property
    def is_editable(self):
        return self.category in (MANAGED,TESTING)

    def __str__(self):
        return "{}.{}".format(self.publisher,self.name)

    class Meta(object):
        db_table = "event_type"
        unique_together = [('publisher','name')]

class Event(ModelEventMixin,models.Model):
    publisher = models.ForeignKey(Publisher,null=False,related_name="publisher_events",on_delete=models.PROTECT,editable=False)
    event_type = models.ForeignKey(EventType,null=False,related_name="events",on_delete=models.PROTECT,editable=False)
    active = models.BooleanField(default=True,editable=False)
    source = models.CharField(max_length=128,null=False,unique=False,editable=False)
    publish_time = models.DateTimeField(auto_now_add=timezone.now,editable=False)
    payload = JSONField(null=False,editable=False)


    @cachedclassproperty
    def events(cls):
        return [
            ModelEvent(cls,
                actions=[ModelEvent.INSERT],
                name="event",
                event_column="NEW.publisher_id || '.' || NEW.event_type_id",
                payload="SELECT NEW.id,NEW.publisher_id,NEW.event_type_id"
                #condition="EXISTS(SELECT 1 FROM publisher a join event_type b on a.name = b.publisher_id where a.active and b.active and b.name = NEW.event_type_id)"
            )
        ]

    def __str__(self):
        return "{}({})".format(self.event_type,self.id)

    class Meta(object):
        db_table = "event"
        index_together = [
            ('publisher',),
            ('publisher','event_type')
        ]

class EventProcessingModule(ActiveModel):
    name = models.CharField(max_length=64,null=False,unique=True)
    code = models.TextField(null=True)
    parameters = models.TextField(null=True,blank=True)
    comments = models.TextField(null=True,blank=True)


    def __str__(self):
        return self.name

    class Meta(object):
        db_table = "event_processing_module"


class Subscriber(ActiveModel):
    name = models.CharField(max_length=32,null=False,primary_key=True)
    category = models.SmallIntegerField(default=MANAGED,choices=CATEGORY_CHOICES)
    comments = models.TextField(null=True,blank=True)

    @property
    def is_system_event_type(self):
        return self.category == SYSTEM

    @property
    def is_editable(self):
        return self.category in (MANAGED,TESTING)

    def __str__(self):
        return self.name

    class Meta(object):
        db_table = "subscriber"

class SubscribedEventType(ActiveModel):
    subscriber = models.ForeignKey(Subscriber,null=False,related_name="event_types",on_delete=models.PROTECT)
    publisher = models.ForeignKey(Publisher,null=False,related_name="subscribed_publisher_event_types",on_delete=models.PROTECT)
    event_type = ChainedForeignKey(EventType,
        chained_field="publisher", chained_model_field="publisher",
        show_all=False, auto_choose=True,  null=False,on_delete=models.PROTECT)

    category = models.SmallIntegerField(default=MANAGED,choices=CATEGORY_CHOICES)
    event_processing_module = models.ForeignKey(EventProcessingModule,null=True,on_delete=models.PROTECT,blank=True)
    parameters = JSONField(null=True,blank=True)
    last_dispatched_event = models.ForeignKey(Event,null=True,on_delete=models.PROTECT,editable=False)
    last_dispatched_time = models.DateTimeField(null=True,editable=False)

    @property
    def is_system_event_type(self):
        return self.category == SYSTEM

    @property
    def is_editable(self):
        return self.category in (MANAGED,TESTING)

    def __str__(self):
        return "{} subscribes {}".format(self.subscriber,self.event_type)

    class Meta(object):
        db_table = "subscribed_event_type"
        unique_together = [('subscriber','publisher','event_type')]

class SubscribedEvent(models.Model):
    PROCESSING = 0
    SUCCEED = 1
    FAILED = -1
    TIMEOUT = -2

    subscriber = models.ForeignKey(Subscriber,null=False,editable=False,related_name="events",on_delete=models.PROTECT)
    publisher = models.ForeignKey(Publisher,null=False,editable=False,related_name="subscribed_publisher_events",on_delete=models.PROTECT)
    event_type = models.ForeignKey(EventType,null=False,editable=False,related_name="subscribed_events",on_delete=models.PROTECT)
    event = models.ForeignKey(Event,null=True,editable=False,related_name="subscribed",on_delete=models.PROTECT)
    process_host = models.CharField(max_length=256,null=False,editable=False)
    process_pid = models.CharField(max_length=32,null=True,editable=False)
    process_times = models.IntegerField(default=1,editable=False)
    process_start_time = models.DateTimeField(auto_now_add=timezone.now)
    process_end_time = models.DateTimeField(null=True,editable=False)
    status = models.IntegerField(default=PROCESSING,editable=False)
    result = models.TextField(null=True,editable=False)

    class Meta(object):
        db_table = "subscribed_event"
        unique_together = [('subscriber','publisher','event_type','event')]
        index_together = [
            ('event',),
            ('publisher','event_type','status')
        ]


class EventProcessingHistory(models.Model):
    subscribed_event = models.ForeignKey(SubscribedEvent,null=False,editable=False,related_name="processing_history",on_delete=models.PROTECT)
    process_host = models.CharField(max_length=256,null=False,editable=False)
    process_pid = models.CharField(max_length=32,null=True,editable=False)
    process_start_time = models.DateTimeField(null=False,editable=False)
    process_end_time = models.DateTimeField(null=True,editable=False)
    status = models.IntegerField(null=False,editable=False)
    result = models.TextField(null=True,editable=False)

    class Meta(object):
        db_table = "event_processing_history"

class AuditModelListener(object):
    def set_user_and_time(sender,instance,update_fields=None,**kwargs):
        try:
            original_instance = instance.__class__.objects.get(pk = instance.pk)
        except models.ObjectDoesNotExist:
            original_instance = None

        AuditModelListener._set_user_and_time(instance)


    def _set_user_and_time(instance,update_fields,original_instance=None):
        if original_instance is None:
            #create
            instance.creator = loginuser.get()
            instance.modifier = loginuser.get()
        else:
            instance.modifier = loginuser.get()
            if update_fields is not None:
                if "modifier" not in update_fields:
                    update_fields.append("modifier")
                if "modified" not in update_fields:
                    update_fields.append("modified")

class ActiveModelListener(object):
    @staticmethod
    @receiver(pre_save, sender=Publisher)
    @receiver(pre_save, sender=EventType)
    @receiver(pre_save, sender=EventProcessingModule)
    @receiver(pre_save, sender=Subscriber)
    @receiver(pre_save, sender=SubscribedEventType)
    def set_user_and_time(sender,instance,update_fields=None,**kwargs):
        try:
            original_instance = instance.__class__.objects.get(pk = instance.pk)
        except models.ObjectDoesNotExist:
            original_instance = None

        ActiveModelListener._set_user_and_time(instance,update_fields,original_instance)

    def _set_user_and_time(instance,update_fields,original_instance=None):
        AuditModelListener._set_user_and_time(instance,update_fields,original_instance)
        if original_instance is None:
            #create
            instance.active_modifier = loginuser.get()
            instance.active_modified = timezone.now()
        else:
            if original_instance.active != instance.active:
                instance.active_modifier = loginuser.get()
                instance.active_modified = timezone.now()
                if update_fields is not None:
                    if "active_modifier" not in update_fields:
                        update_fields.append("active_modifier")
                    if "active_modified" not in update_fields:
                        update_fields.append("active_modified")


class PublisherListener(object):
    @staticmethod
    @receiver(post_save, sender=Publisher)
    def create_system_event_type(sender,instance,created,**kwargs):
        if not created:
            return
        if instance.is_system_publisher:
            return
        EventType(
            name="pub_{}".format(instance.name),
            publisher=Publisher.EVENTHUB_CONSOLE,
            category=SYSTEM,
            active=True,
            active_modifier=User.PROGRAMMATIC,
            active_modified=timezone.now(),
            modifier=User.PROGRAMMATIC,
            creator=User.PROGRAMMATIC,
            comments="Used by event hub console to manage publisher '{}'".format(instance.name),
            sample={
                "command":"active"
            }
        ).save()

class SubscriberListener(object):
    @staticmethod
    @receiver(post_save, sender=Subscriber)
    def create_system_event_type(sender,instance,created,**kwargs):
        if not created:
            return
        EventType(
            name="sub_{}".format(instance.name),
            publisher=Publisher.EVENTHUB_CONSOLE,
            category=SYSTEM,
            active=True,
            active_modifier=User.PROGRAMMATIC,
            active_modified=timezone.now(),
            modifier=User.PROGRAMMATIC,
            creator=User.PROGRAMMATIC,
            comments="Used by event hub console to manage subscriber '{}'".format(instance.name),
            sample={
                "command":"active"
            }
        ).save()


reversion.register(Publisher)
reversion.register(EventType)
reversion.register(Subscriber)
reversion.register(SubscribedEventType)
reversion.register(EventProcessingModule)
