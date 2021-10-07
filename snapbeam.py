import argparse
from automator_setup import Setup
from main_payloads import PayloadRunner
'''
-h / --help : show help message

--setup [savename] : Setup automation environment; Optionally save automation settings in a file.

--boost [n]: Run boost score routine for n cycles

--add name1 name2 ...    Add all people with said names

--removeall     Remove all friends present in the Chat section.


'''
parser = argparse.ArgumentParser(description="SnapBeam: A Snapscore booster")

parser.add_argument(
    '--setup',
    dest='setupfname',
    action="store",
    metavar="savename",
    nargs="?",
    default=None,
    const="",
    help="Setup automation env by finding the positions of buttons in Snapchat."
)

parser.add_argument(
    '--file',
    dest='filename',
    action='store',
    metavar='filename',
    default=None,
    type=str,
    help="Name of JSON file that contains the positions of screen elements."
)


parser.add_argument(
    '--boost',
    dest='cycles',
    action='store',
    metavar='N',
    default=None,
    type=int,
    help="Num of times to take a snap and send it to others."
)


parser.add_argument(
    '--add',
    dest='usernames',
    action='store',
    metavar='name',
    nargs='+',
    default=None,
    help="Usernames to search and add as friends"

)

parser.add_argument(
    '--removeall',
    action='store_true',
    help="Remove all friends via the Chat section."
)

args = parser.parse_args()

if (args.setupfname is not None):
            if (args.cycles is None
            and args.usernames is None
            and not args.removeall
            ):
                env_prepper = Setup(host="127.0.0.1", port=5037)
                env_prepper.setup_automation_env(setup_mode=0, file_output=args.setupfname)

            if (args.cycles is not None
                    and args.usernames is None
                    and not args.removeall
            ):
                if not args.setupfname: # If string is indeed empty
                        env_prepper = Setup(host="127.0.0.1", port=5037)
                        env_prepper.setup_automation_env(setup_mode=1)

                        runner = PayloadRunner("127.0.0.1", 5037, env_prepper.positions)
                        runner.boost_score_routine(args.cycles)

            if (args.cycles is None
            and args.usernames is not None
            and not args.removeall
            ):
                if not args.setupfname: # If string is indeed empty
                    env_prepper = Setup(host="127.0.0.1", port=5037)
                    env_prepper.setup_automation_env(setup_mode=2)

elif (args.removeall 
        and args.setupfname is None
        and args.cycles is None
        and args.usernames is None
        ):
            runner = PayloadRunner("127.0.0.1", 5037, dict()) #removeall friends is purely hardcoded atm so no known positions are provided.
            runner.delete_all_friends_routine()

elif(args.cycles
        and args.setupfname is None
        and args.usernames is None
        and args.filename is not None
        ):
            runner = PayloadRunner("127.0.0.1", 5037, args.filename)
            runner.boost_score_routine(args.cycles)

elif(args.usernames
        and args.setupfname is None
        and args.cycles is None
        and args.filename is not None
        ):
            runner = PayloadRunner("127.0.0.1", 5037, args.filename)
            runner.add_friends_routine(args.usernames)


