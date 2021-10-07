from automator_setup import Setup
from InteractorClass import Interactor
import time
import sys
import json

class PayloadRunner(Interactor):

    def __init__(self, host, port, positions=None):
        
        super().__init__(host, port)
        
        #if not skipSetup:
        #    if(super().setup_automation_env() == -1):
        #        sys.exit(1) #TODO: Better way to exit script more gracefully.

        if isinstance(positions, dict):
            self.positions = positions
        elif isinstance(positions, str):
            with open(positions, "r") as json_positions:
                self.positions = json.loads(json_positions.read()) #read json file positions into dictionary

    def open_snapchat(self):
        self.interactor.open_snapchat(usr=10)

    def close_snapchat(self):
        self.interactor.close_snapchat()

    def add_friends_routine(self, names):
        
        self.open_snapchat()
        time.sleep(5)
        #names=("John", "Jennifer", "Mary") #User names to search and add.
        self.interactor.tap(self.positions.get("add_friend")[0])
        time.sleep(1)
        for i, name in enumerate(names):
            self.interactor.tap(self.positions.get('friends_txt_box')[0])
            if i>0:
                for _ in range(len(names[i-1])): #Clear text box for next name
                        self.interactor.kbpress("DEL")
            
            self.interactor.type(name)
            self.interactor.kbpress("ENTER")
            #print(self.interactor.search_xpath(n=".//node[@resource-id='com.snapchat.android:id/no_friends_text']", firstonly=True))
            while(self.interactor.search_xpath(n=".//node[@resource-id='com.snapchat.android:id/no_friends_text']", firstonly=True).get("n")[0] is None): #While there are still search results

                _usr_element_dict = self.interactor.find_xpath_coords(usr_box_points = ".//*[@resource-id='com.snapchat.android:id/add_friends_recycler_view']/node")

                usr_box_points = _usr_element_dict.get("usr_box_points")
                print(usr_box_points)
                if(len(usr_box_points) % 2 != 0):
                    usr_box_points = usr_box_points[:-1]

                add_button_positions=[]
                for k in range(len(usr_box_points)):

                    if len(usr_box_points)-1 == k:
                        break
                    
                    #Midpoint of above and below usr element coords - x_offset == `Add User` button; Done this way since uiautomator doesn't show `add user` coords.
                    mid = self.interactor.midpoint( (usr_box_points[k][2:] + usr_box_points[k+1][2:],) )[0]
                    #print(mid)
                    add_button_positions.append(self.interactor.offset(mid, (-100, 0)))
                    #print(self.interactor.offset(mid, (-100, 0)))

                for add_btn in add_button_positions[::-1]: #Backwards traversal to avoid tapping same user.
                    self.interactor.tap(add_btn)
                
        print("Finished adding friends.")
        self.close_snapchat()

    def boost_score_routine(self, cycles=2):
        self.open_snapchat()
        time.sleep(5)
        
        for cycle in range(cycles):
            ''' Take a snap and move to `after snap` page '''
            print(f"[Cycle {cycle} out of {cycles}.]")
            #NOTE: You may want to increase thread sleep times if your device is underpowered

            
            #self.interactor.tap_and_hold(self.positions["camera"][0], 15000)
            #Take a picture
            self.interactor.tap(self.positions['camera'][0])
            time.sleep(1)

            #Send video to `last snap` users  
            self.interactor.tap(self.positions["send_to"][0])
            time.sleep(1)
            self.interactor.tap(self.positions["last_snap"][0])
            self.interactor.tap(self.positions["commit"][0])

            '''Moving from chat page back to main cam page'''
            time.sleep(1)
            self.interactor.swipe(self.display.middle, self.interactor.offset(self.display.middle, (-300,0)), 600)
        
        print(f"Finished {cycles} cycles of snapscore boost. Bye bye!")
        self.close_snapchat()
    
    def delete_all_friends_routine(self):
        #Rough draft routine with hardcoded pointer location to delete all friends. Change them based on your device's screen size.
    #You should be in the `Chat` page of snapchat and then run it.
    #It will run indefinitely until you CTRL+C
    
        avatar_coords = (93, 504)
        more_button = (114, 2476)
        remove_friend_button = (372, 1531)
        confirm_removal = (757, 1587)
        while(True):
            self.interactor.tap_and_hold(avatar_coords, 500)
            time.sleep(2)
            self.interactor.tap(more_button)
            time.sleep(1.5)
            self.interactor.tap(remove_friend_button)
            time.sleep(2)
            self.interactor.tap(confirm_removal)
            time.sleep(2.5)


