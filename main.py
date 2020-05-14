#!/bin/env python3

import pygame

import config, geometry
from actor import PlayerSeal, AddSpeedCommand
from controller import GameController

""" 
This is the main file for the game.

This game has been purposefully designed such this (and config.py) are the only file that imports pygame. This way, the code can be easily reused for future projects.

"""

class ActorController:
    def __init__(self, screen_min, screen_max):
        self.add_velocity = geometry.Vector(0, 0.01)

        self.screen_bounds = (screen_min, screen_max)
        self.npc_bounds = (screen_min - geometry.Vector(200,0), )

        self.actor_dict = {
                "player": PlayerSeal(),
                "npcs": list(),
        }

    @property
    def player(self):
        return self.actor_dict["player"]

    @property
    def npcs(self):
        return self.actor_dict["npcs"]

    def handle_keypresses(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return AddSpeedCommand(self.player, self.add_velocity)
        return None

    def update_actors(self):
        self.player.update(self.screen_bounds[0], self.screen_bounds[1])

        # Mark npcs for deletion so we don't update the list while we're
        # iterating through it
        mark_for_deletion = list()
        for n in self.npcs:
            n.update(self.screen_bounds[0], self.screen_bounds[1])
            if n.delete:
                mark_for_deletion.append(n)
        # Delete marked npcs
        for d in mark_for_deletion:
            self.npcs.remove(d)

    def draw_actors(self, screen):
        pygame.draw.rect(screen, config.Color["blue"], config.rect_to_pygame(self.player.draw()))

        # Draw NPCs
        for n in self.npcs:
            pygame.draw.rect(screen, config.Color["red"],
                    config.rect_to_pygame(n.draw()))



def main():
    """ This is the main function that runs everything else in the game. """
    pygame.init()
    screen = pygame.display.set_mode(config.ScreenInfo.size)

    # Create an actor controller
    controller = ActorController(geometry.Vector(0,0),
            geometry.Vector(config.ScreenInfo.width, config.ScreenInfo.height))

    # Create a game manager
    mananger = GameController(pygame.time.set_timer)

    PROCESS_CUSTOM_EVENT = {
            config.EVENT_MAPPING["CREATE_NEW_FISH"]: mananger.create_fish,
    }

    # Main loop, this runs continuously until the player decides to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue;

            # Process custom events
            if event.type in PROCESS_CUSTOM_EVENT:
                PROCESS_CUSTOM_EVENT[event.type]()

        command = controller.handle_keypresses()
        if (command):
            command.execute()

        controller.update_actors()
        screen.fill(config.Color["black"])
        controller.draw_actors(screen)
        pygame.display.flip()


if __name__=="__main__":
    main()
