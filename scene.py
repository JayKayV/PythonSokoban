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

