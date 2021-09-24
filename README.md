## Beam me up, Snappy! - WIP Snapscore booster

**This is WIP!!**

### How does it work?
- Controls your smartphone's touchscreen via USB ADB
- Controls your snapchat application by continiously snap-spamming the users you last sent a snap to.
- Also, adds new friends to your account cus the more people you sent a snap to = the higher the snapscore gain.

## But..really, how does it work?
Ok you wanna get technical.. *\*clears throat\**

- Androd provides a UI automation framework embedded in the OS, called [uiautomator](https://stuff.mit.edu/afs/sipb/project/android/docs/tools/help/uiautomator/index.html)
- "Beam me up, Snappy" makes use of this framework to parse the current activity present on the screen and find the position bounds of certain buttons/fields in the snapchat application
- It does some basic vector math based on that and finally interacts with them to send a snap or add friends.

## Requirements
- [pure-python-adb](https://github.com/Swind/pure-python-adb)
- Python 3.8+
- Snapchat v11.17.0.37 (This is the version I tested it on. **May break in newer versions, use at your own risk!** )
- Brain

## What is working
- Sending (Spamming) a snap to the user you last sent a snap to. A 15s video is recorded and sent to the users in the `last snap` group for a given amount of cycles. _Default value of cycles is 2._
- Adding new friends based on usernames in a list (Snapbeam searches and adds ALL users with a given name). By default it will add users with names: `Robin, Clark, Chris`. You can change that in the `NAMES` variables of `main_payloads.py`

## What is NOT working _yet_
- Automatically sending a snap to all your friends. As of now, **you'll have to take a snap and manually select all your friends and send it BEFORE you run snapbeam.** Snapbeam will ONLY send a snap successfully to last snap users **if the last snap button exists**
- Automatically deleting all newly-added friends after you're satisfied with your snapscore.




