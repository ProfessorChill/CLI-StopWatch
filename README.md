# CLI-StopWatch
Just a simple CLI StopWatch created in Python

##### Requirements
- Python 3
- Curses

##### Shortcuts
Key | Explination
------------ | -------------
ESC | You may have to press this multiple times however it will close.
UP ARROW | Move up stopwatch list
DOWN ARROW | Move down stopwatch list
RIGHT ARROW | Add stopwatch
LEFT ARROW | Remove selected stopwatch
P | Pause/Start selected stopwatch

###### Known Bugs
- Upon closing you must wait one second for the program to actually close, this is because of the sleep(1) in the StopWatch main loop.
