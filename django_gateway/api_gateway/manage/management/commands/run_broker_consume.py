import asyncio

from django.core.management.base import BaseCommand

from api_gateway.message_broker.queue_consumer import rabbitmq_consumer


class Command(BaseCommand):
    help = 'Start broker consumer'

    def handle(self, *args, **options):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(rabbitmq_consumer())
