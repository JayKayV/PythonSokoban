import xml.etree.ElementTree as et

color = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'light_blue': (0, 255, 255),
    'yellow': (255, 255, 0),
    'black': (0, 0, 0),
    'magenta': (255, 0, 255),
    'gray': (80, 80, 80)
}

def StringAssign(s, i, c):
    return s[:i] + c + s[i+1:]

def readKeyData():
    filename = 'config/keys.xml'

    root = et.parse(filename).getroot()
    return {o.attrib['action']:o.text for o in root.findall('key')}

def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def minus(a, b):
    return [a[0] - b[0], a[1] - b[1]]

def get_pos_data(lmap, pos):
    return lmap[pos[0]][pos[1]]

def assign_lvlmap(lmap, pos, v):
    lmap[pos[0]] = StringAssign(lmap[pos[0]], pos[1], v)

def swapin_lvlmap(lmap, pos1, pos2):
    v1, v2 = get_pos_data(lmap, pos1), get_pos_data(lmap, pos2)
    assign_lvlmap(lmap, pos1, v2)
    assign_lvlmap(lmap, pos2, v1)

def aligncenter(size1, size2):
    return (size1[0] - size2[0]) // 2, (size1[1] - size2[1]) // 2

def updateKeyData(action, key):
    filename = 'config/keys.xml'

    root = et.parse(filename).getroot()
    o = root.find('/.[@action=\'{}\']'.format(action))
    o.text = key

def centralize(x, y):
    return (10 - x) // 2, (10 - y) // 2