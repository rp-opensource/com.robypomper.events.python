# rp.events

A tiny Python library for adding events to your classes also as decorators.

**Version:** 0.0.1 \
**Author:** Roberto Pompermaier <robypomper@johnosproject.org> \
**License:** Apache License, Version 2.0 \
**Language:** Python 3 \
**Distribution repository:** [https://pypi.org/project/rp.events]() \
**Source:** [https://github.com/rp-opensource/com.robypomper.events.python]()

---

## What is it?

This is a small module that provide the ability to create custom events. Events
can be declared using the class `EventManager` that provide the method to
register/deregister event's observer but also the method to emit the event.

The `EventManager` class is quite flexible and allows to create events
configuring the observer's called method and his parameters. More info on the
`events.py` inline docs.

`EventManager` objects are commonly used in classes. Those classes that must
declare the register/deregister/emit methods and forward their calls to the
corresponding `EventManager` instance. \
In order to avoid repetitive code, this module provides the `register_owner_methods()`
method that adds the event's specific methods to the event's owner (normally the
hosting class itself). More info on this method can be found at `events_with_decorators.py`
example.

---

## How to use it?

### Install rp.events

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/rp.events).

To install it please execute the following command:

```sh
pip install rp.events
```

### Add an event into a class

#### Manual method

This module is based on the main class `EventManager` that can be instantiated,
by a class, for any event provided by that class. So, the hosting class, can
provide the (public) `register_evA()` and `deregister_evA()` methods and the
(private) `emit()` method.

```python
from rp.events import EventManager

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

#### Register owner's methods

There is also an experimental method, the `register_owner_methods()`. This
method is designed to be called during EventManager initialization and his
purpose is to automatically add the register and deregister methods.

```python
from rp.events import EventManager

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

#### Using decorators

The last method to define an event is using decorators. This is the most elegant
way to use this module because reduce the repetitive code. Event's default method
and params are defined by the method decorated with the `@events_emitter`. So in
the following example the Service2 class define 3 different events

```python
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
```

---

## Documentation

More info about how to use the EventManager and the other methods from this
module please see his [source repository](https://github.com/rp-opensource/com.robypomper.events.python).
