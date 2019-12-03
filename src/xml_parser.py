import xml.etree.ElementTree as ET

class XML:
    def __init__(self, relative_location):
        self.tree = None
        self.root = None

        try:
            self.tree = ET.parse(str(relative_location))
            self.root = self.tree.getroot()
        except Exception as e:
            print("Caught exception:",e)

    def FindByName(self, parent, name, value):
        # THIS IS CASE SENSITIVE
        # Find attribute by looping
        Found = ""
        for a in self.root.findall(str(parent)):
            found_name = a.get('name')
            if found_name.lower() == name.lower():
                # Matched, return value
                Found = a.find(str(value)).text
        return Found
