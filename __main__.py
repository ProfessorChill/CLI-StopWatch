import sys
import threading
import curses

from time import sleep
from curses import wrapper


class StopWatch(threading.Thread):
    seconds = []
    minutes = []
    hours = []
    seconds.append(0)
    minutes.append(0)
    hours.append(0)

    def run(self):
        while MainProgram.running:
            sleep(1)
            for x in range(0, len(StopWatch.seconds)):
                StopWatch.seconds[x] = StopWatch.seconds[x] + 1
                if StopWatch.seconds[x] == 60:
                    StopWatch.minutes[x] = StopWatch.minutes[x] + 1
                    StopWatch.seconds = 1
                if StopWatch.minutes[x] == 60:
                    StopWatch.hours[x] = StopWatch.hours[x] + 1
                    StopWatch.minutes = 1


class MainProgram:
    running = True

    def run(stdscr):
        curses.echo()
        thread = StopWatch()
        thread.start()
        while True:
            sleep(0.10)
            stdscr.clear()
            for x in range(0, len(StopWatch.seconds)):
                strToDisp = '{} Seconds | {} Minutes | {} Hours'
                strToDisp = strToDisp.format(StopWatch.seconds[x],
                                             StopWatch.minutes[x],
                                             StopWatch.hours[x])
                stdscr.addstr(x, 0, strToDisp)
            stdscr.refresh()
            c = stdscr.getch()
            if c == 27:
                break
            elif c == 259:
                StopWatch.seconds.append(0)
                StopWatch.minutes.append(0)
                StopWatch.hours.append(0)
            elif c == 258:
                StopWatch.seconds.pop(len(StopWatch.seconds)-1)
                StopWatch.minutes.pop(len(StopWatch.minutes)-1)
                StopWatch.hours.pop(len(StopWatch.hours)-1)
        MainProgram.running = False
        sys.exit()


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    wrapper(MainProgram.run)
