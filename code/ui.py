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
    def __init__ (s, scr, jodel, x=0, y=0):

        # Mostly for debugging
        s.jodel = jodel

        # I want types...
        if jodel.get("image_url"):
            type = "IMAGE"
            s.msg = "[IMAGE POST]\n" + jodel["message"]
        else:
            type = "TEXT"
            s.msg = jodel["message"]

        # ---------------------------------

        s.y, s.x = x, y

        my, mx = scr.getmaxyx ()
        
        s.height = max(3, count_char (s.msg, "\n")) + 2
        s.width = mx
        # [0, inf)
        s.win = scr.derwin (s.height, s.width, y, x)

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
    # wrapper does this
    #curses.noecho ()
    #curses.cbreak ()
    #stdscr.keypad (True)
    stdscr.refresh ()

    my, mx = stdscr.getmaxyx ()
    post_win = curses.newwin(my - 1, int (mx * 3/4), 0, 0)

    a = get.account
    status, posts = a.get_posts_recent ()

    total_height = 1
    post_windows = []
    for post in posts["posts"][:6]:
        jwin = JodelWindow (post_win, post, y=total_height)
        post_windows += [jwin]
        total_height += jwin.height

    current_post = 0
    current_jodel = 0

    #jwin = JodelWindow (post_win, (posts["posts"][current_jodel]))
    post_win.refresh ()
    stdscr.refresh ()

    while True:

        post_windows [current_jodel].win.standend ()

        c = stdscr.getkey ()
        if c == 'q':
            return
        if c == 'j':
            current_jodel += 1
        if c == 'k':
            current_jodel -= 1

        # Does this even do anything?
        post_windows [current_jodel].win.standout ()
        post_windows [current_jodel].win.refresh ()

        #post_win.mvwin (current_line, 0)
        #jwin.win.erase ()
        #jwin = JodelWindow (post_win, (posts["posts"][current_jodel]))
        post_win.refresh ()
    #curses.endwin ()

if __name__ == "__main__":
    curses.wrapper (main)

    # stdscr = curses.initscr ()
