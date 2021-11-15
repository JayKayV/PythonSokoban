from content.scene import Scene
from content.level import Level
from content.uiBase import Layer
from content.ui import *
from datetime import timedelta, datetime
pygame.init()

def get_direction(vec):
    if vec[0] == 0:
        if vec[1] == 1:
            return 'right'
        else:
            return 'left'
    else:
        if vec[0] == -1:
            return 'up'
        else:
            return 'down'
    return 'error'

class GameLayer(Layer):
    levelmap = None
    player_pos = None
    gameStates = []
    directionStates = []
    otherScenes = None
    ui = None

    def setUi(self, gameUi):
        self.ui = gameUi

    def load(self, levelmap):
        self.direction = [1, 0]
        self.gameOver = False
        self.moves = 0
        pfx = 'content/sprites/'
        self.sprites = {
            'P': {'up': pygame.image.load(pfx+'up.png').convert_alpha(),
                  'down': pygame.image.load(pfx+'down.png').convert_alpha(),
                  'left': pygame.image.load(pfx+'left.png').convert_alpha(),
                  'right': pygame.image.load(pfx+'right.png').convert_alpha()
                  },
            'B': pygame.image.load(pfx+'box_0.png').convert_alpha(),
            'W': pygame.image.load(pfx+'wall.png').convert_alpha(),
            'X': pygame.image.load(pfx+'point.png').convert_alpha(),
            'activated_box': pygame.image.load(pfx+'box_1.png').convert_alpha(),
            'H': pygame.image.load(pfx+'hole.png').convert_alpha(),
            'E': pygame.image.load(pfx+'space.png').convert_alpha()
        }

        pfx = 'content/audio/'
        self.sounds = {
            'footstep': pygame.mixer.Sound(pfx+'footstep.ogg'),
            'retrace': pygame.mixer.Sound(pfx+'footstep_retrace.ogg'),
            'game-over': pygame.mixer.Sound(pfx+'game_over.ogg')
        }
        self.channel = pygame.mixer.Channel(1)
        #load game logic data
        self.levelmap = levelmap.split('*')
        self.lvl_height, self.lvl_width = len(self.levelmap), len(self.levelmap[0])
        self.gameStates.append(self.levelmap.copy())
        self.directionStates.append(self.direction.copy())
        self.org_map = self.levelmap.copy()

        self.xpos = []
        for i in range(len(self.levelmap)):
            for j in range(len(self.levelmap[i])):
                if self.levelmap[i][j] in ['x', 'X']:
                    self.xpos.append((i, j))
                    if self.levelmap[i][j] == 'x':
                        helper.assign_lvlmap(self.levelmap, (i, j), 'B')
                        self.org_map = self.levelmap.copy()
                elif self.levelmap[i][j] == 'P':
                    self.player_pos = [i, j]
        self.gameStates[0] = self.levelmap.copy()

    def find_player(self):
        for i in range(len(self.levelmap)):
            ppos = self.levelmap[i].find('P')
            if ppos > 0:
                self.player_pos = [i, ppos]
                break

    def checkWinning(self):
        if self.levelmap is None or self.xpos is None:
            raise TypeError('None values...')

        for pos in self.xpos:
            if self.levelmap[pos[0]][pos[1]] != 'B':
                return False
        return True

    def update(self, actions):
        if self.gameOver:
            return 'None'
        mapupdated = False
        updated = False
        for action in actions:
            if action == 'reset' and not updated:
                now = datetime.now()
                dt = now - self.oldtime
                self.oldtime = now

                if dt >= timedelta(milliseconds=20) and len(self.gameStates) > 1:
                    self.gameStates = [self.gameStates[0]]
                    self.directionStates = [self.directionStates[0]]
                    self.direction = self.directionStates[0].copy()
                    self.levelmap = self.gameStates[-1].copy()
                    self.find_player()

                    updated = True
                    self.moves = 0
                    self.ui.update({'moves': 0, 'win': False})
            elif action == "undo" and not updated:

                now = datetime.now()
                dt = now - self.oldtime
                self.oldtime = now

                if dt >= timedelta(milliseconds=20) and len(self.gameStates) > 1:
                    self.directionStates.pop()
                    self.gameStates.pop()
                    self.direction = self.directionStates[-1].copy()
                    self.levelmap = self.gameStates[-1].copy()
                    self.find_player()

                    updated = True
                    self.moves -= 1
                    self.ui.update({'moves': self.moves})
                    self.channel.play(self.sounds['retrace'])
            else:
                now = datetime.now()
                dt = now - self.oldtime
                self.oldtime = now

                if dt >= timedelta(milliseconds=20):
                    if action == "right" and not updated:
                        self.direction = [0, 1]
                        updated = True
                    elif action == "down" and not updated:
                        self.direction = [1, 0]
                        updated = True
                    elif action == "left" and not updated:
                        self.direction = [0, -1]
                        updated = True
                    elif action == "up" and not updated:
                        self.direction = [-1, 0]
                        updated = True
                    else:
                        raise ValueError('action is not specified(action_name: {})'.format(action))

                    new_pos = helper.add(self.player_pos, self.direction)
                    new_pos_data = helper.get_pos_data(self.levelmap, new_pos)
                    #print(new_pos)
                    if new_pos_data in ['E', 'X']:
                        helper.swapin_lvlmap(self.levelmap, self.player_pos, new_pos)
                        if new_pos_data == 'X':
                            if helper.get_pos_data(self.org_map, self.player_pos) == 'X':
                                helper.assign_lvlmap(self.levelmap, self.player_pos, 'X')
                            else:
                                helper.assign_lvlmap(self.levelmap, self.player_pos, 'E')
                        self.player_pos = new_pos

                        mapupdated = True
                    elif new_pos_data == 'B':
                        new_bpos = helper.add(new_pos, self.direction)
                        new_bpos_data = helper.get_pos_data(self.levelmap, new_bpos)

                        if new_bpos_data in ['E', 'X', 'H']:
                            helper.swapin_lvlmap(self.levelmap, new_pos, new_bpos)
                            helper.swapin_lvlmap(self.levelmap, self.player_pos, new_pos)
                            helper.assign_lvlmap(self.levelmap, self.player_pos, 'E')

                            if new_bpos_data == 'H':
                                helper.assign_lvlmap(self.levelmap, new_bpos, 'E')

                            self.player_pos = new_pos

                            mapupdated = True

                    for pos in self.xpos:
                        if self.levelmap[pos[0]][pos[1]] == 'E':
                            helper.assign_lvlmap(self.levelmap, pos, 'X')
                    self.gameOver = self.checkWinning()
                    if mapupdated:
                        self.moves += 1
                        self.ui.update({'moves': self.moves})
                        if self.gameOver:
                            self.channel.play(self.sounds['game-over'])
                            self.ui.update({'win': True})
                    if not self.gameOver:
                        self.channel.play(self.sounds['footstep'])

        if mapupdated:
            self.gameStates.append(self.levelmap.copy())
            self.directionStates.append(self.direction.copy())
            #print(self.levelmap) #to debug
        return self.levelmap

    def blit(self, surf=None):
        surf = pygame.Surface(self.screensize)
        surf.fill((0, 0, 0))

        left, top = helper.centralize(self.lvl_width, self.lvl_height)

        i = 0
        for row in self.levelmap:
            j = 0
            for o in row:
                pos = (64 * j + 60 + left * 64, 64 * i + 60 + top * 32)
                if o != 'B' and o != 'e':
                    if o == 'P':
                        surf.blit(self.sprites['E'], pos)
                        surf.blit(self.sprites[o][get_direction(self.direction)], pos)
                    else:
                        surf.blit(self.sprites[o], pos)
                elif o == 'B':
                    if (i, j) in self.xpos:
                        surf.blit(self.sprites['activated_box'], pos)
                    else:
                        surf.blit(self.sprites[o], pos)
                j += 1
            i += 1
        return surf

class UiLayer(Layer):
    game = None

    def load(self):
        self.ui = parseScene('game')
        self.updateTable = {'moves': 0, 'win': False}
        #print(self.ui)
        self.ui['moves-text'].set('MOVES: {}', 0)

    def setGame(self, gameUi):
        self.game = gameUi

    def update(self, action):
        if isinstance(action, tuple):
            for o in self.ui.values():
                if o.collide(action):
                    return o.name
        elif isinstance(action, dict):
            for o in action:
                self.updateTable[o] = action[o]
                if o == 'moves':
                    self.ui['moves-text'].update(action[o])
                #must guarantee that action contain the same key as in updateTable

    def blit(self, surf):
        for name in self.ui.keys():
            mpos = pygame.mouse.get_pos()
            if name != 'win-text' or (name == 'win-text' and self.updateTable['win']):
                osurf, orect = self.ui[name].blit(mpos)
                surf.blit(osurf, orect)
        return surf

class gameScene(Scene):
    def __init__(self, leveluri, levelid, screensize):
        super().__init__()
        level = Level()
        self.leveluri, self.levelid = leveluri, int(levelid)
        self.leveldata, self.levelmap = level.autoload(leveluri, levelid)
        self.gameLayer = GameLayer(screensize)
        self.gameLayer.load(self.levelmap)

        self.uiLayer = UiLayer(screensize)
        self.uiLayer.load()

        self.gameLayer.setUi(self.uiLayer)

        keys = helper.readKeyData()
        self.game_keys = {pygame.key.key_code(keys[key]):key for key in keys}

    def update(self, key_input, mouse_input):
        if key_input is not None:
            update_keys = []
            for key in self.game_keys:
                if key_input[key]:
                    update_keys.append(self.game_keys[key])

            self.lvlmap = self.gameLayer.update(update_keys)
            if self.lvlmap is None:
                raise ValueError('lvlmap is null')
        if mouse_input != None:
            codename = self.uiLayer.update(mouse_input)
            if codename == 'prev-level':
                if self.levelid > 1:
                    self.levelid -= 1
                    self.leveldata, self.levelmap = Level.autoload(self.leveluri, str(self.levelid))
                    self.gameLayer.load(self.levelmap)

                    self.uiLayer.update({'moves': 0, 'win': False})
            if codename == 'next-level':
                if self.levelid < int(self.leveldata['size']):
                    self.levelid += 1
                    self.leveldata, self.levelmap = Level.autoload(self.leveluri, str(self.levelid))
                    self.gameLayer.load(self.levelmap)

                    self.uiLayer.update({'moves': 0, 'win': False})


        """
        if mouse_input == pygame.MOUSEBUTTONUP or pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.uiLayer.update(mouse_pos)
        """

def sendAction(*args):
    if len(args) != 2:
        raise KeyError('Need exacly two args')
    else:
        if not isinstance(args[0], GameLayer):
            raise TypeError('first argument have to be game layer type')

        if not isinstance(args[1], str):
            raise TypeError('second argument have to specify action')
        args[0].update(args[1])



