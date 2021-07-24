# Client code

## Micropython (REPL) commands

### Workflow

Copy code to the microcontroller

`boot.py` and `main.py` are required files.

* `cp boot.py /pyboard`
* `cp main.py /pyboard`
* `cp Interact.py /pyboard`

Copy local wifi information to microcontroller

* `cp config.json /pyboard`

__Soft reset of microcontroller__

__Boots to connect to local wifi from boot.py__

__Jumps to main.py__


### Touch implementations

- Click
- Smart click
- Long click
