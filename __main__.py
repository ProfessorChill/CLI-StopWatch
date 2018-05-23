""" Just a simple CLI Stopwatch that supports multiple watches """
import sys
import threading
import curses

from time import sleep


class StopWatch(threading.Thread):
    """ The stopwatch class which handles the counting of all watches """
    seconds = []
    minutes = []
    hours = []
    paused = []
    seconds.append(0)
    minutes.append(0)
    hours.append(0)

    def run(self):
        while APP.running:
            sleep(1)
            for watch in range(0, len(StopWatch.seconds)):
                if watch not in StopWatch.paused:
                    StopWatch.seconds[watch] = StopWatch.seconds[watch] + 1
                    if StopWatch.seconds[watch] == 60:
                        StopWatch.minutes[watch] = StopWatch.minutes[watch] + 1
                        StopWatch.seconds[watch] = 0
                    if StopWatch.minutes[watch] == 60:
                        StopWatch.hours[watch] = StopWatch.hours[watch] + 1
                        StopWatch.minutes[watch] = 0


class MainProgram:
    """ The main program handler """
    def __init__(self):
        self.running = True
        self.watch_to_control = 0
        self.num_watches = 1

    def display(self, stdscr):
        """ Used to display the watches """
        for watch in range(0, len(StopWatch.seconds)):
            if watch == self.watch_to_control and watch in StopWatch.paused:
                str_to_disp = '--> {} Seconds | {} Minutes | {} Hours - P'
            elif watch == self.watch_to_control:
                str_to_disp = '--> {} Seconds | {} Minutes | {} Hours'
            elif watch in StopWatch.paused:
                str_to_disp = '{} Seconds | {} Minutes | {} Hours - P'
            else:
                str_to_disp = '{} Seconds | {} Minutes | {} Hours'

            str_to_disp = str_to_disp.format(StopWatch.seconds[watch],
                                             StopWatch.minutes[watch],
                                             StopWatch.hours[watch])
            stdscr.addstr(watch, 0, str_to_disp)

    def run(self, stdscr):
        """ The main run loop """
        curses.echo()
        thread = StopWatch()
        thread.start()
        while self.running:
            sleep(0.10)
            stdscr.clear()
            self.display(stdscr)
            stdscr.refresh()
            char = stdscr.getch()

            if char == 27:
                self.running = False
            elif char == 259 and self.watch_to_control > 0:  # Up Arrow
                self.watch_to_control -= 1
            elif char == 258 and self.watch_to_control + 1 < self.num_watches:  # Down Arrow
                self.watch_to_control += 1
            elif char == 260:  # Left Arrow
                StopWatch.seconds.pop(self.watch_to_control)
                StopWatch.minutes.pop(self.watch_to_control)
                StopWatch.hours.pop(self.watch_to_control)
                self.num_watches -= 1

                if self.watch_to_control > 0:
                    self.watch_to_control -= 1

                if self.watch_to_control in StopWatch.paused:
                    StopWatch.paused.remove(self.watch_to_control)
            elif char == 261:  # Right Arrow
                StopWatch.seconds.append(0)
                StopWatch.minutes.append(0)
                StopWatch.hours.append(0)
                self.num_watches += 1
            elif char == 112 and self.watch_to_control in StopWatch.paused:  # P
                StopWatch.paused.remove(self.watch_to_control)
            elif char == 112 and self.watch_to_control not in StopWatch.paused:  # P
                StopWatch.paused.append(self.watch_to_control)
        sys.exit()


if __name__ == '__main__':
    STDSCR = curses.initscr()
    APP = MainProgram()
    curses.noecho()
    curses.cbreak()
    STDSCR.keypad(True)
    STDSCR.nodelay(1)
    curses.wrapper(APP.run)
