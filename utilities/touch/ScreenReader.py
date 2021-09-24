from .TouchControlWrapper import TouchControlWrapper
import xml.etree.ElementTree as XML
class ScreenReader(TouchControlWrapper):

    def dump_ui_xml(self):
        raw_tty_out = self.dev.shell("uiautomator dump /dev/tty")
        last_tag = raw_tty_out.rfind(">")
        return XML.fromstring(raw_tty_out[:last_tag+1]) if last_tag != -1 else None

    #def search_xpath(self, *args, firstonly=True):
    def search_xpath(self, **kwargs):
        search_results = dict()
        print(kwargs)
        if (kwargs and (screen_xml := self.dump_ui_xml()) is not None):
            for dic_key, xpath_str in kwargs.items():
                if dic_key in {'firstonly', 'midpoint'}:
                    continue

                #print(screen_xml.find(xpath_str))
                search_results.update({ dic_key: [screen_xml.find(xpath_str),] if kwargs.get('firstonly') else screen_xml.findall(xpath_str)})
        
        return search_results


    def find_xpath_coords(self, **kwargs):
        dict_xpath_results = self.search_xpath(**kwargs)
        XPATH_COORDS = dict()
        #print(dict_xpath_results)
        if dict_xpath_results:
            for dic_key, xpath_string in dict_xpath_results.items():
                vector_positions = []
                #print(dict_xpath_results[xpath_string])
                for element in dict_xpath_results.get(dic_key):
                    if element is not None:
                        raw_str_bounds = element.get("bounds")
                        br_pos = raw_str_bounds.rfind("[")
                        str_list_bounds = raw_str_bounds[:br_pos]+','+raw_str_bounds[br_pos:]
                        x1y1, x2y2 = eval(str_list_bounds) # convert to list elements.
                        vector_positions.append(tuple(x1y1+x2y2))
                #print(vector_positions)
                
                if kwargs.get('midpoint'):
                    print(tuple(vector_positions))
                    XPATH_COORDS.update( {dic_key: self.midpoint(tuple(vector_positions))} )
                else:
                    XPATH_COORDS.update( {dic_key: tuple(vector_positions)} )
        
        #Returns dictionary of tuple of tuples where each inner tuple = (x1, y1, x2, y2), (k1, s1, k2, s2)... E.g. {xpath1: ((x1,y1,x2,y2),(k1,s1,k2,s2)), xpath2: ..., xpath3: ... }
        return XPATH_COORDS
    

    def midpoint(self, vectors):
        return tuple([tuple([(v[0]+v[2])/2,(v[1]+v[3])/2]) for v in vectors]) #returns tuple of tuples where each tuple= (k1, r1) | k1 = (x1+x2)/2 and r1=(y1+y2)/2

    def offset(self, vector, vector_offset):
        return tuple([vector[i]+vector_offset[i] for i in range(len(vector))]) if len(vector)==len(vector_offset) else None
'''
    def xpath_press_midpoint(self, xpath_str):
        positions = find_xpath_coords(xpath_str)
        if positions is not None:
            positions = midpoint(positions)

        for pos in positions:
            self.tap(pos)
    '''
