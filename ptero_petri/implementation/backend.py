from . import exceptions
from .petri.builder import Builder
from .petri.net import Net
from .translator import Translator
import celery


class Backend(object):
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    def create_net(self, net_data):
        translator = Translator(net_data)
        builder    = Builder(self.redis_connection)
        stored_net = builder.store(translator.future_net, translator.variables,
                translator.constants)

        self._place_initial_tokens(stored_net.key,
                net_data.get('initialMarking'))

        return {
                'net_key': stored_net.key,
                'entry_place_info': stored_net.place_lookup.value
        }

    @property
    def put_token(self):
        return celery.current_app.tasks[
                'ptero_petri.implementation.celery_tasks.create_token.CreateToken']

        task.delay(net_key, place_idx=place_idx, color=color,
                color_group_idx=color_group_idx, data=data)


    def _place_initial_tokens(self, net_key, initial_marking):
        for place_name in initial_marking:
            self.put_token.delay(net_key, place_name=place_name)

    def cleanup(self):
        pass
