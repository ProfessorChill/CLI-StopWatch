""" Just a simple CLI Stopwatch that supports multiple watches """
import sys
import threading
import curses
import curses.ascii

from time import sleep


class StopWatch(threading.Thread):
    """ The stopwatch class which handles the counting of all watches """

    def __init__(self):
        super().__init__(daemon=True)
        self.seconds = []
        self.minutes = []
        self.hours = []
        self.watches = 0
        self.add()
        self.paused = set()

    def add(self):
        """ Append a stopwatch that is set to 0 """
        for time in self.seconds, self.minutes, self.hours:
            time.append(0)
        self.watches += 1

    def remove(self, watch_index):
        """ Remove a stopwatch at given index """
        for time in self.seconds, self.minutes, self.hours:
            time.pop(watch_index)
        self.watches -= 1

    def run(self):
        while self.watches:
            sleep(1)
            for watch in range(0, self.watches):
                if watch not in self.paused:
                    self.seconds[watch] = self.seconds[watch] + 1
                    if self.seconds[watch] == 60:
                        self.minutes[watch] = self.minutes[watch] + 1
                        self.seconds[watch] = 0
                    if self.minutes[watch] == 60:
                        self.hours[watch] = self.hours[watch] + 1
                        self.minutes[watch] = 0


def display(screen, stop_watch, selected):
    """ Used to display the watches """
    for watch in range(0, stop_watch.watches):
        line = '{:02d} Seconds | {:02d} Minutes | {:02d} Hours'\
            .format(stop_watch.seconds[watch],
                    stop_watch.minutes[watch],
                    stop_watch.hours[watch])
        if watch in stop_watch.paused:
            line += " - P"
        screen.addstr(watch, 0, line, curses.A_REVERSE if watch == selected else 0)


def run(screen):
    """ The main run loop """
    curses.echo()
    stop_watch = StopWatch()
    stop_watch.start()
    selected = 0
    while stop_watch.watches:
        sleep(1/20)
        screen.clear()
        display(screen, stop_watch, selected)
        screen.refresh()
        char = screen.getch()

        if char == curses.ascii.ESC:
            stop_watch.watches = 0
        elif char == curses.KEY_UP and selected > 0:
            selected -= 1
        elif char == curses.KEY_DOWN and selected + 1 < stop_watch.watches:
            selected += 1
        elif char == curses.KEY_LEFT:
            stop_watch.remove(selected)
            if selected > 0:
                selected -= 1
            if selected in stop_watch.paused:
                stop_watch.paused.remove(selected)
        elif char == curses.KEY_RIGHT:
            stop_watch.add()
        elif char == ord('p'):
            stop_watch.paused ^= {selected}  # add/remove
    sys.exit()


if __name__ == '__main__':
    standard_screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)  # no cursor
    standard_screen.keypad(True)
    standard_screen.nodelay(True)
    curses.wrapper(run)
