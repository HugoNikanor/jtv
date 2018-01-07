import jodel_api
import os
import os.path 

# Rate Limits:
# * 200 new accounts / 30 min
# * 200 upvotes / min
# * 100 captcha / min

# HTTP 403 means banned

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

#def do(account):
#main():
        #status, data = account.get_posts_recent()
        #return status, data
