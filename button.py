import pygame
from settings import *


algos = ["BFS", "DFS", "A*", "IDDFS", "FRINGE", "GREEDY BFS", "BIDIRECT BFS"]


class Button:
    def __init__(self, text, x, y, width, height, callback, font_size=24):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.font = pygame.font.SysFont(None, font_size)
        self.base_color = LIGHT_GRAY
        self.hover_color = DARK_GRAY
        self.text_color = BLACK
        self.active_color = ACTIVE_BTN
        self.is_active = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.is_active:
            color = self.active_color
        elif self.text in algos:
            color = (100, 230, 210) if self.rect.collidepoint(mouse_pos) else ALGO_BTN
        elif self.text == "Run (Enter)":
            color = (80, 230, 150) if self.rect.collidepoint(mouse_pos) else RUN_BTN
        elif self.text == "Save Grid" or self.text == "Load Grid" or self.text == "Clear Grid":
            color = (255, 140, 140) if self.rect.collidepoint(mouse_pos) else UTILITY_BTN
        elif self.text == "Visualizer Description":
            color = (100, 170, 255) if self.rect.collidepoint(mouse_pos) else DESCRIPTION_BTN
        else:
            color = (130, 145, 170) if self.rect.collidepoint(mouse_pos) else DEFAULT_BTN

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WARM_GRAY, self.rect, 2)  # border

        # Draw text centered
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                if self.text in algos:
                    self.is_active = True
                else:
                    self.is_active = False
