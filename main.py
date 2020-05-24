#!/bin/env python3

import pygame
import functools

import actor
import config
import events
import game_assets
import geometry

import controller

""" This is the main file for the game.  """

def setup(screen):
    # Load assets
    asset_loader = game_assets.AssetLoader()
    fish_loader = game_assets.FishLoader()
    shark_loader = game_assets.SharkLoader()
    background_loader = game_assets.BackgroundLoader()

    # Create an actor controller
    actor_controller = controller.ActorController(asset_loader, geometry.Vector(0,0),
            geometry.Vector(config.ScreenInfo.width, config.ScreenInfo.height))

    game_controller = controller.GameController(actor_controller,
            background_loader)

    # Create a npc creator
    creator = controller.NpcCreator(fish_loader, shark_loader, pygame.time.set_timer)

    PROCESS_CUSTOM_EVENT = {
            config.EVENT_MAPPING["CREATE_NEW_FISH"]: creator.create_fish,
            config.EVENT_MAPPING["CREATE_NEW_SHARK"]: creator.create_shark,
    }

    # Fill in background
    screen.blit(background_loader.main_image,
            pygame.Rect(0,0,config.ScreenInfo.width,
                config.ScreenInfo.height))

    return (game_controller, PROCESS_CUSTOM_EVENT)

def main():
    """ This is the main function that runs everything else in the game. """
    pygame.init()
    config.ScreenInfo.font = pygame.font.Font("freesansbold.ttf", 24)
    screen = pygame.display.set_mode(config.ScreenInfo.size)

    game_controller, PROCESS_CUSTOM_EVENT = setup(screen)

    # Main loop, this runs continuously until the player decides to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue;
 
            # Process custom events
            if event.type in PROCESS_CUSTOM_EVENT and game_controller.active():
                PROCESS_CUSTOM_EVENT[event.type]()
        game_controller.tick(screen)
        pygame.display.flip()

        if game_controller.do_reset:
            game_controller, PROCESS_CUSTOM_EVENT = setup(screen)


if __name__=="__main__":
    main()
