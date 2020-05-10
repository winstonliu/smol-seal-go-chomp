#!/bin/env python3

import pygame

import config, geometry
from seal import PlayerSeal, AddSpeedCommand

class ActorController:
    def __init__(self, screen_min, screen_max):
        self.player = PlayerSeal()
        self.add_velocity = geometry.Vector(0, 0.01)

        self.player_bounds = (screen_min, screen_max)

    def handle_keypresses(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return AddSpeedCommand(self.player, self.add_velocity)
        return None

    def update_actors(self):
        self.player.update(self.player_bounds[0], self.player_bounds[1])

    def draw_actors(self, screen):
        pygame.draw.rect(screen, config.Color["blue"], config.rect_to_pygame(self.player.draw()))


def main():
    """ 
    This is the main function that runs everything else in the game.
    """
    pygame.init()
    screen = pygame.display.set_mode(config.ScreenInfo.size)
    controller = ActorController(geometry.Vector(0,0),
            geometry.Vector(config.ScreenInfo.width, config.ScreenInfo.height))

    # Main loop, this runs continuously until the player decides to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue;

        command = controller.handle_keypresses()
        if (command):
            command.execute()

        controller.update_actors()
        screen.fill(config.Color["black"])
        controller.draw_actors(screen)
        pygame.display.flip()


if __name__=="__main__":
    main()
