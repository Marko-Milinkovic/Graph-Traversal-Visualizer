import pygame
from settings import *


class Dropdown:
    def __init__(self, x, y, w, h, options, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected_index = 0
        self.expanded = False
        self.callback = callback  # Function to call when selection changes

    def draw(self, surface):
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw selected item
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.options[self.selected_index], True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(surface, LIGHT_GRAY, option_rect)
                pygame.draw.rect(surface, BLACK, option_rect, 1)
                text = font.render(option, True, BLACK)
                surface.blit(text, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(mouse_pos):
                        self.selected_index = i
                        self.expanded = False
                        self.callback(self.options[i])
                        break
                else:
                    self.expanded = False
