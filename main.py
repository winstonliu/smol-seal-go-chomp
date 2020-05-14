#!/bin/env python3

import pygame
import functools

import actor
import config
import geometry
from controller import GameController
from observer import GameEventsManager
from collision import CollisionMonitor

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
                "player": actor.PlayerSeal(),
                "npcs": list(),
        }

        self.collision_monitor = CollisionMonitor(self.actor_dict)
        self.game_over = False

    @property
    def player(self):
        return self.actor_dict["player"]

    @property
    def npcs(self):
        return self.actor_dict["npcs"]

    def listen_to_events(self):
        new_actor_list = GameEventsManager.consume("actors_created")
        if new_actor_list:
            self.npcs.extend([x.value for x in new_actor_list])

    def handle_keypresses(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return actor.AddSpeedCommand(self.player, self.add_velocity)
        return None

    def update_actors(self):
        # Create new actors if we've received the signal
        self.listen_to_events()
        # Check for collisions
        self.collision_monitor.check_player_collision()

        # Check if we've received a game over message
        result = GameEventsManager.consume("got_eaten")
        if (result):
            self.game_over = True
            return 

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
            pygame.draw.rect(screen, config.Color[n.color],
                    config.rect_to_pygame(n.draw()))

    def draw_game_over(self, screen):
        text = config.ScreenInfo.font.render("You got eaten! Happy Birthday!!", config.Color["black"], config.Color["white"])
        text_rect = text.get_rect()
        # Center the text
        text_rect.topleft = ((config.ScreenInfo.width - text_rect.width) / 2 , (config.ScreenInfo.height - text_rect.height) / 2)
        screen.blit(text, text_rect)


def main():
    """ This is the main function that runs everything else in the game. """
    pygame.init()
    config.ScreenInfo.font = pygame.font.Font("freesansbold.ttf", 24)
    screen = pygame.display.set_mode(config.ScreenInfo.size)

    # Create an actor controller
    controller = ActorController(geometry.Vector(0,0),
            geometry.Vector(config.ScreenInfo.width, config.ScreenInfo.height))

    # Create a game manager
    mananger = GameController(pygame.time.set_timer)

    # TODO switch these out with notify event triggers
    PROCESS_CUSTOM_EVENT = {
            config.EVENT_MAPPING["CREATE_NEW_FISH"]:
                    functools.partial(mananger.create_npc, actor.NpcFish),
            config.EVENT_MAPPING["CREATE_NEW_SHARK"]: 
                    functools.partial(mananger.create_npc, actor.NpcShark),
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

        screen.fill(config.Color["black"])

        if not controller.game_over:
            controller.update_actors()
            controller.draw_actors(screen)
        else:
            controller.draw_game_over(screen)

        pygame.display.flip()


if __name__=="__main__":
    main()
