class Scene:
    gameLayer = None
    uiLayer = None

    def __init__(self):
        self.next = self

    def terminate(self):
        self.next == None

    def change(self, nextScene):
        self.next = nextScene

    def blit(self, screen):
        scene_res = None
        if self.gameLayer is not None:
            scene_res = self.gameLayer.blit()
            if self.uiLayer is not None:
                scene_res = self.uiLayer.blit(scene_res)

        if scene_res is None:
            raise ValueError('pls have gameLayer or uiLayer in scene')
        screen.blit(scene_res, (0, 0))
        """
        else:
            raise ValueError('UI LAYER CANNOT BE None!')
        """

    def update(self, key_input, mouse_input):
        return 'pls update this'

class Layer:
    def __init__(self, scr_size):
        if not isinstance(scr_size, tuple):
            raise ValueError('Must initiaze scr_size')
        elif not (isinstance(scr_size[0], int) and isinstance(scr_size[1], int)):
            raise TypeError('Tuple must contain int type')

        self.screensize = scr_size

    def load(self):
        return "pls update this!"

    def update(self, actions):
        return "pls update this!"

    def blit(self, surf=None):
        return "pls update this!"
