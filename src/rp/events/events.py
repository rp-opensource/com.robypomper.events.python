"""
Helper module to manage Events (callbacks, signal/slots...).

This module is based on the main class `EventManager` that can be instantiated,
by a class, for any event provided by that class. So, the hosting class, can
provide the (public) `register_evA()` and `deregister_evA()` methods and the
(private) `emit()` method.

```python
class Button:

    def __init__(self):
        self._on_pressed = EventManager(self, 'on_pressed')

    def register_on_pressed(self, observer, method_name=None):
        self._on_pressed.register(observer, method_name)

    def deregister_on_pressed(self, observer):
        self._on_pressed.deregister(observer)

    def _emit_on_pressed(self, event):
        self._on_pressed.emit(event)

    def simulate_touch(self):
        self._emit_on_pressed("print_timestamp")


class Observer:

    def on_pressed(self, event_owner, event):
        button = event_owner
        print("I'm Observer::on_pressed({}, {})".format(button, event))


if __name__ == "__main__":
    button = Button()
    observer = Observer()

    button.register_on_pressed(observer)
    button.simulate_touch()
```

Previous code, will print \
`I'm Observer::on_pressed(<__main__.Button object at 0x7fb72e570450>, print_timestamp)`
More info on `register_evA()` and `deregister_evA()` methods in the next sections.

`EventManager` allows you to customise the event using following properties and methods:
* owner: if not set, then it will be the EventManager instance itself,
         otherwise it's used to be set as the hosting instance.
* default_method_name: it's a string that define which method the EventMager
                       looks for during observer registration. Normally it's
                       set using following format `on_{EVENT_NAME}`.
* emit(): this is the default method to trigger an event, from the hosting class.
          this method can call all registered observers using a single params
          (the EventManager's owner) or as many as the event's requires.

During the registration, also the observer can customise the EventMager behaviour.
With the `register(self, observer, method_name: str = None)`, the **observer
can use the `method_name` param to register a different method** than the one
defined by the `default_method_name` EventManager's property.

```python
class Observer2:

    def on_PLAY_pressed(self, button, event):
        print("I'm Observer2::on_PLAY_pressed({}, {})".format(button, event))

button.register_on_pressed(observer, 'on_PLAY_pressed')
```


# EventManager ownership

Normally, an EventManager is owner by the class that emit the events. \
The EventManager ownership means be the object passed to the observer methods
as owner of the event triggered.

If a class would not pass his reference to his observers, then the hosting
class can trigger the event using the `emit_no_owner()` method. Like
the `emit()` method, it support optional arguments, but the first one will
not the EventManager owner (as the ` emit()` method does).

This can be useful to emit events without any parameter, so observer's
methods will be called without arguments. Or to hide the real class
implementation and trigger events using the public interface as event's
owner.


# Register and deregister method

The `register_evA()` and `deregister_evA()` are the classic method exposed by
a class used by an Observer to register himself to a class event. We suggest to
use the following convention on define your register/deregister methods:

* `register_{EVENT_NAME}()`
* `deregister_{EVENT_NAME}()`

There is also an experimental method, the `register_owner_methods()`. This
method is designed to be called during EventManager initialization and his
purpose is to automatically add the register and deregister methods. \
For now it's still as experimental feature because this approach is not
supported by linters.

```python
class Student:

    def __init__(self):
        self._on_start = EventManager(self, 'on_start')
        self._on_start.register_owner_methods()

class Observer:

    def on_start(self):
        print("I-m Observer::on_start")


if __name__ == "__main__":
    student = Student()
    obs1 = Observer()
    student.register_on_start(obs1)
```

Warning:
* this class do not implement any error handling
  * that means any error will be trowed along the stack
    * deregister an unregistered observer
    * trigger an event to a method with the wrong number of arguments
* this class do not support the registration of more than one method per observer
  * for any observer register multiple times, will be keep the last registration
* this class can have an unpredictable behavior if
  * an observer call register/deregister methods during events triggering
    (concurrent access on observers' dictionary)

"""


class EventManager:
    """
    Main class for event management. It can be instantiated, by a class, for
    any event provided by that class. So, the hosting class, can provide the
    (public) `register_evA()` and `deregister_evA()` methods and the (private)
    `emit()` method.
    """

    def __init__(self, owner=None, default_method_name: str = 'on_event'):
        """
        EventManager constructor.

        :param owner: set the event's owner, if `None` the owner will be the EventManager instance himself.
        :param default_method_name: the method name used to trigger the events to the registered observers,
        unless specified otherwise during observer registration. By default, his value is `on_event`.
        """
        self._owner = owner if owner else self
        self._observers = {}
        self._default_method = default_method_name

    def register(self, observer, method_name: str = None):
        """
        Register given observer. The observer must implement a method named as
        the event's default method, otherwise it can specify another method,
        from the observer, using the `method_name` arg.

        Warning: this class do not support the registration of multiple methods
        per observer. When called multiple times, this method override previous
        observer's registration.

        :param observer: the observer's object.
        :param method_name: the name of the method to call to trigger the event to the `observer`.
        """
        if not method_name:
            method_name = self._default_method
        try:
            method = getattr(observer, method_name)
        except AttributeError as e:
            raise ValueError("observer ({}) must have the method_name ({}) attribute".format(observer, method_name)) \
                from e

        if observer in self._observers.keys():
            raise ValueError("observer ({}) already registered to current EventManager".format(observer))

        self._observers[observer] = method

    def deregister(self, observer):
        """
        Deregister given observer.

        If observer was not registered then this method throws a `KeyError`.

        :param observer: the observer's object.
        """
        del self._observers[observer]

    def emit(self, *args):
        """
        Method used to trigger the event to all registered observers.

        This method has to be called by the hosting class when the event
        managed occurs.

        This method can be called with or without any parameter. The event's
        owner and all `emit()` parameters are forwarded to the registered
        observer's methods.

        To forward only given arguments, use the `emit_no_owner()` method.

        :param args: optional and variable list of arguments.
        """
        for observer in self._observers.keys():
            method = self._observers[observer]
            method(self._owner, *args)

    def emit_no_owner(self, *args):
        """
        Method used to trigger the event to all registered observers.

        This method has to be called by the hosting class when the event
        managed occurs.

        This method can be called with or without any parameter. All
        `emit_no_owner()` parameters are forwarded to the registered
        observer's methods.

        To forward the event's owner and all given arguments, use the
        `emit()` method.

        :param args: optional and variable list of arguments.
        """
        for observer in self._observers.keys():
            method = self._observers[observer]
            method(*args)

    def __str__(self) -> str:
        """
        :return: a string representation of the EventManager.
        """
        if self == self._owner:
            return "<{}::{}>".format(self.__class__.__name__, self._default_method)
        return "<{} for {}::{}>".format(self.__class__.__name__, self._owner, self._default_method)

    def register_owner_methods(self):
        """
        Method to add the `register_{EVENT_NAME}` and the `deregister_{EVENT_NAME}`
        method to the owner class.

        As `EVENT_NAME` is used the `default_method` value.
        """
        if self == self._owner:
            raise ReferenceError("can't register event's methods if no owner has been set")

        self._owner.__setattr__("register_{}".format(self._default_method), self.register)
        self._owner.__setattr__("deregister_{}".format(self._default_method), self.deregister)
        self._owner.__setattr__("_emit_{}".format(self._default_method), self.emit)


def extract_event_name(attr_name: str) -> str:
    event_name = attr_name.replace('emit', '')
    return event_name.strip(' -_')


def events_emitter(func):
    def inner_emitter(*args, **kwargs):
        _events_manager = inner_emitter.events_manager
        _events_manager.emit_no_owner(*args, **kwargs)
        # func(*args, **kwargs)

    inner_emitter.event_name = extract_event_name(func.__name__)
    return inner_emitter


def events_host(cls):
    def register_method(instance_events_manager, register_method_name):
        def wrapper(self, *args, **kwargs):
            # (self, observer, method_name: str = None):
            observer = args[0]
            method_name = args[1] if len(args) == 2 else None
            instance_events_manager._owner = self
            instance_events_manager.register(observer, method_name)

        return wrapper

    def deregister_method(instance_events_manager, deregister_method_name):
        def wrapper(self, *args, **kwargs):  # (self, observer):
            observer = args[0]
            instance_events_manager.deregister(observer)

        return wrapper

    for attr_name in dir(cls):
        attr_value = getattr(cls, attr_name)
        if hasattr(attr_value, "event_name"):
            event_name = attr_value.event_name

            field_name = "_{}".format(event_name)
            register_name = "register_{}".format(event_name)
            deregister_name = "deregister_{}".format(event_name)

            events_manager = EventManager(None, event_name)
            register_method_closure = register_method(events_manager, register_name)
            deregister_method_closure = deregister_method(events_manager, deregister_name)

            attr_value.events_manager = events_manager
            register_method_closure.events_manager = events_manager
            register_method_closure.__name__ = register_name
            deregister_method_closure.events_manager = events_manager
            deregister_method_closure.__name__ = deregister_name
            setattr(cls, field_name, events_manager)
            setattr(cls, register_name, register_method_closure)
            setattr(cls, deregister_name, deregister_method_closure)

    return cls
