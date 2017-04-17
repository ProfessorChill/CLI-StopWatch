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
                    StopWatch.seconds[x] = 0
                if StopWatch.minutes[x] == 60:
                    StopWatch.hours[x] = StopWatch.hours[x] + 1
                    StopWatch.minutes[x] = 0


class MainProgram:
    running = True
    watchToControl = 0

    def run(stdscr):
        curses.echo()
        thread = StopWatch()
        thread.start()
        while True:
            sleep(0.10)
            stdscr.clear()
            for x in range(0, len(StopWatch.seconds)):
                if x == MainProgram.watchToControl:
                    strToDisp = '--> {} Seconds | {} Minutes | {} Hours'
                else:
                    strToDisp = '{} Seconds | {} Minutes | {} Hours'
                strToDisp = strToDisp.format(StopWatch.seconds[x],
                                             StopWatch.minutes[x],
                                             StopWatch.hours[x])
                stdscr.addstr(x, 0, strToDisp)
            stdscr.refresh()
            c = stdscr.getch()
            if c == 27:
                break
            elif c == 259:  # Up Arrow
                currNum = MainProgram.watchToControl
                if currNum > 0:
                    currNum = currNum - 1
                    MainProgram.watchToControl = currNum
            elif c == 258:  # Down Arrow
                currNum = MainProgram.watchToControl
                if currNum < len(StopWatch.seconds)-1:
                    currNum = currNum + 1
                    MainProgram.watchToControl = currNum
            elif c == 260:  # Left Arrow
                StopWatch.seconds.pop(MainProgram.watchToControl)
                StopWatch.minutes.pop(MainProgram.watchToControl)
                StopWatch.hours.pop(MainProgram.watchToControl)
            elif c == 261:  # Right Arrow
                StopWatch.seconds.append(0)
                StopWatch.minutes.append(0)
                StopWatch.hours.append(0)
        MainProgram.running = False
        sys.exit()


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    wrapper(MainProgram.run)
