from rp.events import events_host, events_emitter


@events_host
class Service2:

    @events_emitter
    def emit_on_start(self):
        pass

    @events_emitter
    def emit_on_stop(self, a_number: int, a_string: str, a_param):
        pass

    @events_emitter
    def emit_on_pause(self):
        pass

class Observer2:
    def on_started(self, service: Service2):
        print("OBJ: {}".format(self))
        print("     observer::on_started(")
        print("                      {}".format(service))
        print("                      )")

    def on_stopped(self, service: Service2, a_number: int, a_string: str, a_param):
        print("OBJ: {}".format(self))
        print("     observer::on_stopped(")
        print("                      {}".format(service))
        print("                      {}".format(a_number))
        print("                      {}".format(a_string))
        print("                      {}".format(a_param))
        print("                      )")

    def on_paused(self, service: Service2):
        print("OBJ: {}".format(self))
        print("     observer::on_paused(")
        print("                      {}".format(service))
        print("                      )")


if __name__ == "__main__":
    s2 = Service2()
    o2 = Observer2()

    s2.register_on_start(o2, 'on_started')
    s2.register_on_stop(o2, 'on_stopped')
    s2.register_on_pause(o2, 'on_paused')

    s2.emit_on_start()
    s2.emit_on_stop(1, "2", 3.0)
    s2.emit_on_pause()
