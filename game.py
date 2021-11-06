import pygame, helper
from scene import Scene
from level import Level
from uiBase import Layer
from ui import *
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
    otherScenes = None
    ui = None

    def __init__(self, scr_size):
        super().__init__(scr_size)
        self.direction = [1, 0]
        self.gameOver = False
        self.moves = 0

    def setUi(self, gameUi):
        self.ui = gameUi

    def load(self, levelmap):
        self.sprites = {
            'P': {'up': pygame.image.load('sprites/up.png').convert_alpha(),
                  'down': pygame.image.load('sprites/down.png').convert_alpha(),
                  'left': pygame.image.load('sprites/left.png').convert_alpha(),
                  'right': pygame.image.load('sprites/right.png').convert_alpha()
                  },
            'B': pygame.image.load('sprites/box_0.png').convert_alpha(),
            'W': pygame.image.load('sprites/wall.png').convert_alpha(),
            'X': pygame.image.load('sprites/point.png').convert_alpha(),
            'activated_box': pygame.image.load('sprites/box_1.png').convert_alpha(),
            'H': pygame.image.load('sprites/hole.png').convert_alpha(),
            'E': pygame.image.load('sprites/space.png').convert_alpha()
        }

        #load game logic data
        self.levelmap = levelmap.split('*')
        self.gameStates.append(self.levelmap.copy())
        self.org_map = self.levelmap.copy()

        self.xpos = []
        for i in range(len(self.levelmap)):
            for j in range(len(self.levelmap[i])):
                if self.levelmap[i][j] == 'X':
                    self.xpos.append((i, j))
                elif self.levelmap[i][j] == 'P':
                    self.player_pos = [i, j]

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
            pass
        mapupdated = False
        updated = False
        for action in actions:
            if action == "undo" and not updated:
                now = datetime.now()
                dt = now - self.oldtime
                self.oldtime = now

                if dt >= timedelta(milliseconds=20) and len(self.gameStates) > 1:
                    self.gameStates.pop()
                    self.levelmap = self.gameStates[-1].copy()
                    self.find_player()

                    updated = True
                    self.moves -= 1
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
                            print('Winning!')

        if mapupdated:
            self.gameStates.append(self.levelmap.copy())
            #print(self.levelmap) #to debug
        return self.levelmap

    def blit(self, surf=None):
        surf = pygame.Surface(self.screensize)
        surf.fill((0, 0, 0))

        i = 0
        for row in self.levelmap:
            j = 0
            for o in row:
                pos = (64 * j + 100, 64 * i + 200)
                if o != 'B' and o != 'e':
                    if o == 'P':
                        surf.blit(self.sprites['E'], pos)
                        surf.blit(self.sprites[o][get_direction(self.direction)], pos)
                    else:
                        surf.blit(self.sprites[o], pos)
                elif o == 'B':
                    if helper.get_pos_data(self.org_map, [i, j]) == 'X':
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
        print(self.ui)

    def setGame(self, gameUi):
        self.game = gameUi

    def update(self, action):
        if isinstance(action, tuple):
            for o in self.ui:
                    o.onclick(action, sendAction, self.game, o.name)
        elif isinstance(action, dict):
            for o in self.ui:
                if o.name in action:
                    o.update(action[o.name])
                    break

    def blit(self, surf):
        for o in self.ui:
            mpos = pygame.mouse.get_pos()
            osurf, orect = o.blit(mpos)
            surf.blit(osurf, orect)
        return surf

class gameScene(Scene):
    def __init__(self, leveluri, levelid, screensize):
        super().__init__()
        level = Level()
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


