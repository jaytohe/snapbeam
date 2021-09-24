#Needed Libraries
import sys
from ppadb.client import Client
import time
from utilities.touch.ScreenReader import ScreenReader

class Display:
    def __init__(self, phys_size_str):
        self.width, self.height = [int(dimension) for dimension in phys_size_str.split()[-1].split("x")]
        self.middle = (self.width//2, self.height//2)


class Setup:

    def __init__(self, mode=0):
        self.dev = (Client()).devices()[0]
        self.usr = 10
        self.positions = dict()

        if not self.dev:
            print("No device connected.")
            sys.exit(1)
            
        elif not self.dev.shell(f"pm list packages --user {self.usr} | grep com.snapchat.android"):
            print("Snapchat not installed!")
            sys.exit(1)
        
        #If checks passed, gather display info and start setup
        self.display = Display(self.dev.shell("wm size"))
        self.interactor = ScreenReader(self.dev)

    def open_snapchat(self):
        self.dev.shell(f"am start --user {self.usr} -n com.snapchat.android/com.snap.mushroom.MainActivity")

    def close_snapchat(self):
        self.dev.shell("am force-stop com.snapchat.android")


    def setup_automation_env(self):
        print("Please do NOT touch your device until instructed to do so!!")
        print("Setting up automation environment...", end="\t")
        self.open_snapchat()
        time.sleep(5)
        
        ''' Main camera page automation '''
        tmp = self.interactor.find_xpath_coords(
                camera='.//node[@resource-id="com.snapchat.android:id/camera_capture_button"]', 
                add_friend='.//node[@resource-id="com.snapchat.android:id/hova_header_add_friend_icon"]',
                midpoint=True,
                firstonly=True,
                )

        #Check if coordinates were found successfully.
        for key, val in tmp.items():
            if not val:
                print("Failed!")
                print(f"Couldn't find {key} button!")
                return -1
        
        '''After taking snap page automation '''
        #Move to after-snap page.
        self.interactor.tap(tmp.get('camera')[0])
        time.sleep(1)
        #Unfortunately uiautomator gives erroneous coordinates for "Send To" button.
        #Hence, we approximate its position using the device's display coordinates.
        tmp.update({
            'send_to' : ((self.display.width-200, self.display.height-100),),
            })
        tmp.update(self.interactor.find_xpath_coords(discard='.//node[@resource-id="com.snapchat.android:id/preview_back_discard_button"]')) #TODO: Unsafe check for null.
        ''' `Send To` page automation '''
        #Move to send-to page
        self.interactor.tap(tmp.get('send_to')[0])        
        time.sleep(1)
        #Last snap button pos is indirectly found from the "Recents" element
        recents = self.interactor.find_xpath_coords(r='.//node[@text="Recents"]', firstonly=True)
        if not recents:
            print("Could not find recents element.")
            return -1
        tmp.update({
            'last_snap': (self.interactor.offset(recents.get("r")[0][2:], (0, 100)),), #get second vector's coords and offset it.
            'commit' : tmp.get('send_to')
        })
        print(tmp)

        #self.interactor.tap(tmp.get('last_snap')[0])
        #self.interactor.tap(tmp.get('commit')[0])

        #Go back to main page.
        self.interactor.swipe(self.display.middle, self.interactor.offset(self.display.middle, (400,0)), 600)
        self.interactor.tap(tmp.get('discard')[0])
        time.sleep(2)
        self.interactor.tap(self.display.middle)

        ''' Friends Page Automation'''
        self.interactor.tap(tmp.get('add_friend')[0])
        time.sleep(2)
        tmp.update(self.interactor.find_xpath_coords(friends_txt_box=".//node[@resource-id='com.snapchat.android:id/input_field_edit_text']", firstonly=True, midpoint=True)) #TODO: Unsafe. Check if element null.

        self.close_snapchat()
        print("Finished Setup!")
        
        print(tmp)

        self.positions = tmp.copy() 
        
if __name__ == "__main__":
    s = Setup()

    s.setup_automation_env()

    (Friends(s.auto_elements_xpaths, s.diplay))
