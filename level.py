import xml.etree.ElementTree as et

def testParse(name="levels/example_level.xml"):
    a = Level.makeFromString('Manga*Comic', 1000)
    print(a.root.find('row').text)

class Level:
    def __init__(self, root = None):
        self.root = root

    def parse(self, lvl_uri, lvl_id):
        tree = et.parse(lvl_uri)
        root = tree.getroot()
        self.leveldata = root.attrib
        self.root = root.find('./level[@id=\'{}\']'.format(lvl_id))
        for att in self.root.attrib:
            self.leveldata[att] = self.root.attrib[att]

    def load(self):
        levelmap = '*'.join([o.text for o in self.root.findall('row')])
        return self.leveldata, levelmap

    @staticmethod
    def autoload(lvl_uri, lvl_id):
        lvl = Level()
        lvl.parse(lvl_uri, lvl_id)
        return lvl.load()

    def fromXmlString(self, arg):
        if not isinstance(arg, str):
            raise TypeError

        self.root = et.fromstring(arg)

    @staticmethod
    def to_etree(arg):
        if not isinstance(arg, str):
            raise TypeError(arg)

        rows = arg.split('*')
        root = et.Element('level')
        for row in rows:
            o = et.SubElement(root, 'row')
            o.text = row
        return root

    @staticmethod
    def fromstring(arg):
        lvl = Level(Level.to_etree(arg))
        return lvl