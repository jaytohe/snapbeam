#Needed Libraries
import sys
from ppadb.client import Client
import time
import json
from utilities.touch.ScreenReader import ScreenReader

class Display:
    def __init__(self, phys_size_str):
        self.width, self.height = [int(dimension) for dimension in phys_size_str.split()[-1].split("x")]
        self.middle = (self.width//2, self.height//2)

class Setup:

    def __init__(self, host, port, serial=None):
        client= (Client(host, port))
        if len(client.devices()) == 0:
            raise IOError("No device connected.")
        
        self.dev = client.devices()[0] if serial is None else (client).device(serial)
        self.usr = 10
        self.positions = dict()

        if not self.dev.shell(f"pm list packages --user {self.usr} | grep com.snapchat.android"):
            raise IOError("Snapchat not installed!")
            #sys.exit(1)
        
        #If checks passed, gather display info and start setup
        self.display = Display(self.dev.shell("wm size"))
        self.interactor = ScreenReader(self.dev)

    def open_snapchat(self):
        self.dev.shell(f"am start --user {self.usr} -n com.snapchat.android/com.snap.mushroom.MainActivity")

    def close_snapchat(self):
        self.dev.shell("am force-stop com.snapchat.android")

    def _check_found(self, dictionary):
        for key, val in dictionary.items():
            if not val:
                print("Failed!")
                raise RuntimeError(f"Couldn't find {key} element!")
                return False
        return True
            
    def setup_main_cam_page(self, dictionary):
        
        ''' Main camera page automation '''
        tmp = self.interactor.find_xpath_coords(
                camera='.//node[@resource-id="com.snapchat.android:id/camera_capture_button"]', 
                add_friend='.//node[@resource-id="com.snapchat.android:id/hova_header_add_friend_icon"]',
                midpoint=True,
                firstonly=True,
                )
        if self._check_found(tmp):
            dictionary.update(tmp)
    

    def setup_after_snap_page(self, dictionary):
        '''After Snap page automation'''
        #Unfortunately uiautomator gives erroneous coordinates for "Send To" button.
        #Hence, we approximate its position using the device's display coordinates.
        tmp = { 
            'send_to' : ((self.display.width-200, self.display.height-100),),
            'discard' : self.interactor.find_xpath_coords(discard='.//node[@resource-id="com.snapchat.android:id/preview_back_discard_button"]').get('discard')
        }
        if self._check_found(tmp):
            dictionary.update(tmp)

    def setup_send_to_page(self, dictionary):

        #Last snap button pos is indirectly found from the "Recents" element
        tmp = self.interactor.find_xpath_coords(r='.//node[@text="Recents"]', firstonly=True)

        if self._check_found(tmp):
           dictionary.update({
                'last_snap': (self.interactor.offset(tmp.get("r")[0][2:], (0, 100)),), #get second vector's coords and offset it.
                'commit' : dictionary.get('send_to')
            })

    def setup_friends_page(self, dictionary):
        tmp = self.interactor.find_xpath_coords(friends_txt_box=".//node[@resource-id='com.snapchat.android:id/input_field_edit_text']", firstonly=True, midpoint=True)
        
        if self._check_found(tmp):
            dictionary.update(tmp)


    def setup_automation_env(self, setup_mode, file_output=None):
        print("Please do NOT touch your device until instructed to do so!!")
        print("Setting up automation environment...", end="\t")
        self.open_snapchat()
        time.sleep(5)

        tmp = dict()

        #Setup main page
        self.setup_main_cam_page(tmp)

        if (setup_mode in {0, 1}): # 0: setup all, 1: setup boost, 2: setup friends
            #Move to after-snap page.
            self.interactor.tap(tmp.get('camera')[0])
            time.sleep(3)
            
            #Setup after-snap page
            self.setup_after_snap_page(tmp)

            ''' `Send To` page automation '''
            #Move to send-to page
            self.interactor.tap(tmp.get('send_to')[0])
            time.sleep(3)

            self.setup_send_to_page(tmp)

            #Go back to main page.
            self.interactor.swipe(self.display.middle, self.interactor.offset(self.display.middle, (400,0)), 600)
            time.sleep(2)
            self.interactor.tap(tmp.get('discard')[0])
            time.sleep(3)
            self.interactor.tap(self.display.middle)


        if (setup_mode in {0, 2}):
            ''' Friends Page Automation'''
            self.interactor.tap(tmp.get('add_friend')[0])
            time.sleep(2)
            self.setup_friends_page(tmp)

        self.close_snapchat()
        print("Finished Setup!")
        
        print(tmp)

        if file_output is None:
            self.positions = tmp.copy()
        else:
            positions_json = json.dumps(tmp, allow_nan=False, indent=4)
            with open(f'{file_output}.json', "w") as positions_file:
                positions_file.write(positions_json)


if __name__ == "__main__":
    s = Setup()

    s.setup_automation_env()
