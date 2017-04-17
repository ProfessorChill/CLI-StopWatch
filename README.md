# CLI-StopWatch
Just a simple CLI StopWatch created in Python

##### Requirements
- Python 3
- Curses

##### Shortcuts
ESC - You may have to press this multiple times however it will close.
UP ARROW - Add a watch
DOWN ARROW - Deletes most recent watch
  - NOTE: This is temporary and will be updated to delete specific watches

###### Known Bugs
- Upon closing you must wait one second for the program to actually close, this is because of the sleep(1) in the StopWatch main loop.
