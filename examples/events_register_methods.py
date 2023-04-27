from rp.events import EventManager


class Service:

    def __init__(self):
        self._on_start = EventManager(self, 'on_start')
        self._on_start.register_owner_methods()


class Observer:

    def on_start(self, service: Service):
        print("Im Observer::on_start {}".format(self))


s1 = Service()
o1 = Observer()

s1.register_on_start(o1)

s1._emit_on_start()
