class DisplayText:
    def __init__(self,screen, message,font_type,color,posX,posY,marginX,marginY):
        self.msg = font_type.render(message, True, color)
        self.msgRect = self.msg.get_rect()
        self.msgRect.centerx = posX + marginX
        self.msgRect.centery = posY + marginY
        self.screen = screen

    def render(self):
        self.screen.blit(self.msg, self.msgRect)