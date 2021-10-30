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
        if self.gameLayer is not None:
            screen.blit(self.gameLayer.blit(), (0, 0))
        if self.uiLayer is not None:
            screen.blit(self.uiLayer.blit(), (0, 0))
        """
        else:
            raise ValueError('UI LAYER CANNOT BE None!')
        """

    def update(self, key_input, mouse_input):
        return 'pls update this'

