from time import sleep
from curses import wrapper

import curses
import threading


class StopWatch(threading.Thread):
    seconds = 0
    minutes = 0
    hours = 0

    def run(self):
        while True:
            sleep(1)
            StopWatch.seconds = StopWatch.seconds + 1
            if StopWatch.seconds == 60:
                StopWatch.minutes = StopWatch.minutes + 1
                StopWatch.seconds = 1
            if StopWatch.minutes == 60:
                StopWatch.hours = StopWatch.hours + 1
                StopWatch.minutes = 1


def main(stdscr):
    curses.echo()
    StopWatch().start()
    while True:
        sleep(0.10)
        stdscr.clear()
        strToDisp = '{} Seconds | {} Minutes | {} Hours'
        strToDisp = strToDisp.format(StopWatch.seconds,
                                     StopWatch.minutes,
                                     StopWatch.hours)
        stdscr.addstr(0, 0, strToDisp)
        stdscr.refresh()
        c = stdscr.getch()
        if c == 27:
            break
    exit(stdscr)


def exit(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    wrapper(main)
