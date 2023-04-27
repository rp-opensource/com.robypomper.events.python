import pytest

from rp.events import EventManager, events_host, events_emitter


# Test's classes

class ObserverStandard:
    """ Observer with standard method(emitter) """

    def __init__(self):
        self.registered_event_param1 = None

    def on_event(self, event_owner):
        # print("ObserverStandard::on_event {}".format(event_owner))
        self.registered_event_param1 = event_owner


class ObserverCustomMethod:
    """ Observer with standard method(emitter) """

    def __init__(self):
        self.registered_event_param1 = None
        self.registered_event_param2 = None
        self.registered_event_param3 = None

    def method_custom(self, event_owner):
        # print("ObserverCustomMethod::method_custom {}".format(event_owner))
        self.registered_event_param1 = event_owner

    def method_custom_with_owner_and_2_args(self, event_owner, a, b):
        # print("ObserverCustomMethod::method_custom_with_owner_and_2_args ({}, {}, {})".format(event_owner, a, b))
        self.registered_event_param1 = event_owner
        self.registered_event_param2 = a
        self.registered_event_param3 = b

    def method_custom_with_2_args(self, a, b):
        # print("ObserverCustomMethod::method_custom_with_2_args ({}, {})".format(a, b))
        self.registered_event_param2 = a
        self.registered_event_param3 = b


class Observable:

    def __init__(self):
        self._on_event = EventManager(self)


class ObservableNoOwner:

    def __init__(self):
        self._on_event = EventManager()


@events_host
class ObservableDecorated:

    @events_emitter
    def on_decorated_event(self):
        pass


# Test's methods

def test_str__():
    ev = EventManager()
    assert str(ev) == "<EventManager::on_event>"

    ev = EventManager(default_method_name='on_custom_event')
    assert str(ev) == "<EventManager::on_custom_event>"

    owner = object
    ev = EventManager(owner)
    assert str(ev) == "<EventManager for {}::on_event>".format(owner)


def test_standard():
    ev = EventManager()
    obs_std = ObserverStandard()
    ev.register(obs_std)
    ev.emit()
    assert obs_std.registered_event_param1 == ev, "default event_owner is not the EventManager"
    # ObserverStandard::on_event <EventManager::on_event>


def test_standard_with_owner():
    ev_owner = str("object that own the event")
    ev = EventManager(ev_owner)
    obs_std = ObserverStandard()
    ev.register(obs_std)
    ev.emit()
    assert obs_std.registered_event_param1 == ev_owner, "event_owner is not the owner set at the initialization"
    # ObserverStandard::on_event object that own the event


def test_standard_multiple():
    ev = EventManager()
    obs_std = ObserverStandard()
    obs_cust = ObserverCustomMethod()
    ev.register(obs_std)
    ev.register(obs_cust, 'method_custom')
    ev.emit()
    assert obs_std.registered_event_param1 == ev, "event not triggered on obs_std"
    assert obs_cust.registered_event_param1 == ev, "event not triggered on obs_cust"
    # ObserverStandard::on_event <EventManager::on_event>
    # ObserverCustomMethod::method_custom <EventManager::on_event>


def test_standard_multiple_already_registered():
    ev = EventManager()
    obs_std = ObserverStandard()
    ev.register(obs_std)

    # try:
    # ev.register(obs_std)
    # except ValueError as err:
    # print(err)
    # observer (<__main__.ObserverStandard object at 0x7fee5fabb2d0>) already registered to current EventManager
    with pytest.raises(ValueError):
        ev.register(obs_std)


def test_standard_deregistration():
    ev = EventManager()
    obs_std = ObserverStandard()
    obs_cust = ObserverCustomMethod()
    ev.register(obs_std)
    ev.register(obs_cust, 'method_custom')
    ev.deregister(obs_std)
    ev.emit()
    assert obs_std.registered_event_param1 is None, "event triggered on obs_std"
    assert obs_cust.registered_event_param1 == ev, "event not triggered on obs_cust"
    # ObserverCustomMethod::method_custom <EventManager::on_event>


def test_method_name():
    ev = EventManager()
    obs_cust = ObserverCustomMethod()
    ev.register(obs_cust, 'method_custom')
    ev.emit()
    assert obs_cust.registered_event_param1 == ev, "event not triggered on obs_cust"
    # ObserverCustomMethod::method_custom <EventManager::on_event>


def test_method_name_not_exist():
    ev = EventManager()
    obs_cust = ObserverCustomMethod()
    # try:
    # ev.register(obs_cust, 'method_that_not_exist')
    # except ValueError as err:
    # print(err)
    # observer (<__main__.ObserverCustomMethod object at 0x7f821cda2210>) must have the method_name \
    # (method_that_not_exist) attribute
    with pytest.raises(ValueError):
        ev.register(obs_cust, 'method_that_not_exist')


def test_emit_params():
    ev = EventManager()
    obs_cust = ObserverCustomMethod()
    ev.register(obs_cust, 'method_custom_with_owner_and_2_args')
    p1 = 123
    p2 = 'a string'
    ev.emit(p1, p2)
    assert obs_cust.registered_event_param1 == ev, "first event's param is not the event's owner"
    assert obs_cust.registered_event_param2 == p1, "second event's param is not the given one"
    assert obs_cust.registered_event_param3 == p2, "third event's param is not the given one"
    # ObserverCustomMethod::method_custom_with_owner_and_2_args (<EventManager::on_event>, 123, a string)


def test_emit_params_without_owner():
    ev = EventManager()
    obs_cust = ObserverCustomMethod()
    ev.register(obs_cust, 'method_custom_with_2_args')
    p1 = 123
    p2 = 'a string'
    ev.emit_no_owner(p1, p2)
    assert obs_cust.registered_event_param1 is None, "first event's param is the event's owner"
    assert obs_cust.registered_event_param2 == p1, "second event's param is not the given one"
    assert obs_cust.registered_event_param3 == p2, "third event's param is not the given one"
    # ObserverCustomMethod::method_custom_with_2_args (123, a string)


def test_register_owner_methods():
    observable = Observable()
    events_manager = observable._on_event
    events_manager.register_owner_methods()

    obs_std = ObserverStandard()
    observable.register_on_event(obs_std, 'on_event')

    events_manager.emit()
    assert obs_std.registered_event_param1 == observable, "event_owner is not the Observable object"


def test_register_owner_methods_no_owner():
    observable = ObservableNoOwner()
    events_manager = observable._on_event

    with pytest.raises(ReferenceError):
        events_manager.register_owner_methods()


def test_decorators():
    observable = ObservableDecorated()

    obs_std = ObserverStandard()

    observable.register_on_decorated_event(obs_std, 'on_event')

    observable.on_decorated_event()
    assert obs_std.registered_event_param1 == observable, "event_owner is not the Observable object"


def test_decorators_deregister():
    observable = ObservableDecorated()

    obs_std = ObserverStandard()

    observable.register_on_decorated_event(obs_std, 'on_event')
    observable.deregister_on_decorated_event(obs_std)

    observable.on_decorated_event()
    assert obs_std.registered_event_param1 is None, "event_owner is set regardless the observer was deregistered"
