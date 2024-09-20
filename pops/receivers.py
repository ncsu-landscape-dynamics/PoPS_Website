import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.mixins import LoginRequiredMixin
from channels.auth import login
from .models import Run, RunCollection
import channels.layers
from django.dispatch import receiver
from django.db.models import signals


@receiver(signals.post_save, sender=RunCollection, weak=False)
def new_run_collection(sender, instance, **kwargs):
    print('----NEW RUN COLLECTION CREATED----')
    print(instance)
    layer = channels.layers.get_channel_layer()
    group_name = "chat_%s" % instance.session.pk
    data = {
        "jsonrpc": "2.0",
        "method": "new_run_collection",
        "params": {
            "run_collection": str(instance.pk),
            "name": instance.name,
            "date": instance.date_created.strftime("%B %d, %Y, %X"),
            "description": instance.description,
        },
    }
    async_to_sync(layer.group_send)(
        group_name, {"type": "chat_message", "content": data}
    )


@receiver(signals.post_save, sender=Run, weak=False)
def run_status_change(sender, instance, **kwargs):
    print(sender)
    print(instance)
    print(instance.status)
    print(instance.run_collection.session.pk)
    if instance.status != "WRITING_R_DATA" and instance.status != "R_DATA_SUCCESS":
        print('Status is being sent as ' + instance.status)
        layer = channels.layers.get_channel_layer()
        group_name = "chat_%s" % instance.run_collection.session.pk
        data = {
            "jsonrpc": "2.0",
            "method": "run_status_update",
            "params": {
                "run_pk": instance.pk,
                "run_collection": instance.run_collection.pk,
                "status": instance.status,
                "year": instance.steering_year,
            },
        }
        async_to_sync(layer.group_send)(
            group_name, {"type": "chat_message", "content": data}
        )