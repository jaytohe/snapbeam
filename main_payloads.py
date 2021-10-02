from automator_setup import Setup
import time
import sys
import socket
class PayloadRunner(Setup):

    def __init__(self, host="127.0.0.1", port=5037, minitouch_port=6723, serial=None):
        
        super().__init__(host, port, serial)

        if(super().setup_automation_env() == -1):
            sys.exit(1) #TODO: Better way to exit script more gracefully.

        self.minisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.minisocket.setblocking(True)
        try:
            self.minisocket.connect((host, minitouch_port))
        except OSError:
            print("Problem connecting to minitouch socket.")
            sys.exit(1)

        #print(repr(self.minisocket.recv(1024)))


    def add_friends_routine(self):
        self.open_snapchat()
        time.sleep(5)

        names=("Nigel",) #User names to search and add.
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
                
                for pointer_id, add_btn_coords in enumerate(add_button_positions):
                	self.minisocket.sendall(f"d {pointer_id} {int(add_btn_coords[0])} {int(add_btn_coords[1])} 1\n".encode())
                	print(pointer_id)
                	
                self.minisocket.sendall("c\n".encode())
                for pid in range(len(add_button_positions)):
                	self.minisocket.sendall(f"u {pid}\n".encode())
                	self.minisocket.sendall("c\n".encode())
                self.minisocket.sendall("c\n".encode())
                time.sleep(2)
                	
        print("Finished adding friends.")
        self.close_snapchat()

    def boost_score_routine(self, cycles=2):
        self.open_snapchat()
        time.sleep(5)
        
        for cycle in range(cycles):
            ''' Take a snap and move to `after snap` page '''
            #NOTE: You may want to increase thread sleep times if your device is underpowered

            #Record 15s video
            self.interactor.tap_and_hold(self.positions["camera"][0], 15000)
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


if __name__ == "__main__":
        p = PayloadRunner()
        p.add_friends_routine()
        #p.boost_score_routine()
