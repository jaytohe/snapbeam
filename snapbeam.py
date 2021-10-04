import argparse
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
    '--boost',
    dest='cycles',
    action='store',
    metavar='N',
    default=None,
    type=int,
    help="Num of times to take a snap and send it to others."
)