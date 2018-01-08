#!/usr/bin/env python3

import curses
import get

def count_char (str, chr):
    count = 0
    for c in str:
        if c == chr:
            count += 1
    return count

class JodelWindow:
    def __init__ (s, stdscr, jodel):
        my, mx = stdscr.getmaxyx ()
        
        s.msg = jodel["message"]
        s.height = max(3, count_char (s.msg, "\n")) + 2
        s.width = int(mx / 2)
        s.y, s.x = 4, 13
        s.win = curses.newwin (s.height, s.width, s.y, s.x)

        s.win.border ()
        s.win.vline (1, 6, curses.ACS_SBSB, s.height - 2)
        s.point_win = s.win.derwin (s.height - 2, 5, 1, 1)
        s.point_win.addch  (0, 2, ord ("^"))
        s.point_win.addstr (1, 0, str (jodel["vote_count"]).center(5))
        s.point_win.addch  (2, 2, ord ("V"))

        s.content_win = s.win.derwin (s.height - 2, s.width - 8, 1, 7)
        cw_h, cw_w = s.content_win.getmaxyx ()
        str_len = cw_h * cw_w
        s.content_win.addstr (s.msg [:str_len - 2])

        s.win.refresh ()

def main (stdscr):
    curses.noecho ()
    curses.cbreak ()
    stdscr.keypad (True)
    stdscr.refresh ()

    a = get.account
    status, posts = a.get_posts_recent ()
    jwin = JodelWindow(stdscr, posts["posts"][0])

    stdscr.refresh ()
    stdscr.getkey ()

    curses.endwin ()

if __name__ == "__main__":
    curses.wrapper (main)

    # stdscr = curses.initscr ()
