import jodel_api
import os
import os.path

import crayons

import pprint

pp = pprint.PrettyPrinter(indent=4)

# Rate Limits:
# * 200 new accounts / 30 min
# * 200 upvotes / min
# * 100 captcha / min

# HTTP 403 means banned

def closest_color (rgb):
    colors = \
    [ (0x000000, "black"),
      (0x0000FF, "blue"),
      (0x00FFFF, "cyan"),
      (0x00FF00, "green"),
      (0xFF00FF, "magenta"),
      (0xFF0000, "red"),
      (0xFFFFFF, "white"),
      (0x00FFFF, "yellow") ]

    color_diffs = [(abs (rgb - c), n) for (c, n) in colors]

    return min(color_diffs, key=lambda a: a[0])

lat, lng, city = 58.410807, 15.621373, "Linköping"

path_prefix = os.environ.get("XDG_DATA_HOME") or \
        os.path.join(os.environ.get("HOME"), ".local/share/")

def setup_account (lat, lng, city) -> jodel_api.JodelAccount:

    account_filename = os.path.join (path_prefix, "jodel/account_data")

    try:
        if os.path.isfile (account_filename):
            with open (account_filename, "r") as account_file:
                account_data = eval(account_file.read())
                account = jodel_api.JodelAccount(
                        lat=lat,
                        lng=lng,
                        city=city,
                        **account_data)
        else:

            path = os.path.dirname(account_filename)
            if not os.path.exists (path):
                os.makedirs (path)

            with open (account_filename, "w") as account_file:
                account = jodel_api.JodelAccount(
                        lat=lat,
                        lng=lng,
                        city=city);
                account_data = account.get_account_data()
                account_file.write (str(account_data))

    except Exception as e:
        print ("Something went wrong with loading or creating the account")
        print ("Try removing " + account_filename)
        print ("and run the program again")
        print ("-" * 50)
        print (e)
        exit (1)

    os.chmod (account_filename, 0o600)

    return account


def printf_postlist(plist):
    for post in plist:
        color = eval ("0x" + post ["color"])
        cfunc = getattr (crayons, closest_color (color)[1])
        if post.get("image_approved"):
            msg = "{} | IMAGE POST".format (post["vote_count"])
        else:
            msg = "{} | {}".format (
                post ["vote_count"],
                post ["message"])
        print (cfunc (msg))
        print ("-" * 80)

account = setup_account (lat, lng, city)
#status, posts = account.get_posts_recent ()
#status, posts = account.get_posts_top ()
#printf_postlist (posts["posts"])
# status == 200 or fail
# posts["max"] is something


#def do(account):
#main():
        #status, data = account.get_posts_recent()
        #return status, data
