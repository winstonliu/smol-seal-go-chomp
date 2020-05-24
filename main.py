#!/bin/env python3

import pygame
import functools

import actor
import config
import events
import game_assets
import geometry

from controller import GameController

""" This is the main file for the game.  """

class ActorController:
    def __init__(self, asset_loader, screen_min, screen_max):
        self.add_velocity = geometry.Vector(0, 0.01)

        WAVE_HEIGHT = 150
        self.screen_bounds = (screen_min + geometry.Vector(0,150), screen_max)
        self.npc_bounds = (screen_min - geometry.Vector(200,-150), screen_max + geometry.Vector(100,0))
        
        # Set up actors and sprites
        player_sprite = game_assets.SealSprite(asset_loader)
        player = actor.PlayerSeal()
        # Set bounds
        player.bounds = (self.screen_bounds[0], self.screen_bounds[1])
        # Set size
        player.size = geometry.Vector(player_sprite.rect.width, player_sprite.rect.height)
        player_sprite.set_actor(player)

        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.player_sprite_group.add(player_sprite)

        # Create npc groups
        self.fish_sprite_group = pygame.sprite.Group()
        self.shark_sprite_group = pygame.sprite.Group()

        self.score = 0

        self.game_over = False

    @property
    def player(self):
        return self.player_sprite_group.sprites()[0]

    def listen_to_events(self):
        # Create actor bounds
        actor_bounds = self.npc_bounds

        sprite_list = events.GameEventsManager.consume("new_fish")
        if sprite_list:
            new_sprites = [x.value for x in sprite_list]
            # Set bounds on new actors
            for n in new_sprites:
                n.actor.bounds = actor_bounds
                self.fish_sprite_group.add(n)

        sprite_list = events.GameEventsManager.consume("new_shark")
        if sprite_list:
            new_sprites = [x.value for x in sprite_list]
            # Set bounds on new actors
            for n in new_sprites:
                n.actor.bounds = actor_bounds
                self.shark_sprite_group.add(n)

    def handle_keypresses(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return actor.AddSpeedCommand(self.player.actor, self.add_velocity)
        return None

    def update_actors(self):
        # Create new actors if we've received the signal
        self.listen_to_events()
        # Check for collisions
        pygame.sprite.spritecollide(self.player,
                self.fish_sprite_group, True, pygame.sprite.collide_mask) 

        result = pygame.sprite.spritecollide(self.player, self.shark_sprite_group, False) 
        if (result):
            self.game_over = True
            return 
        
        # Ordering is important here!
        # The sprite group update must be before the score update because the
        # sprites update uses the ate fish event
        self.player_sprite_group.update()
        self.fish_sprite_group.update()
        self.shark_sprite_group.update()

        # Update score counter
        result = events.GameEventsManager.consume("ate_fish")
        if (result):
            self.score += 1


    def draw_actors(self, screen):
        # Draw score counter
        text = config.ScreenInfo.font.render("Fishes Eaten: " + str(self.score), config.Color["black"], config.Color["black"])
        text_rect = text.get_rect()
        text_rect.bottomright = (config.ScreenInfo.width - 10, config.ScreenInfo.height - 10)
        screen.blit(text, text_rect)

        # Draw everything onto the screen
        self.player_sprite_group.draw(screen)
        self.fish_sprite_group.draw(screen)
        self.shark_sprite_group.draw(screen)

    def draw_game_over(self, screen):
        text = config.ScreenInfo.font.render("You got eaten! You ate " +
                str(self.score) + " fishes. Happy Birthday!!",
                config.Color["black"], config.Color["white"])
        text_rect = text.get_rect()
        # Center the text
        text_rect.center = (int(config.ScreenInfo.width / 2.0), int(config.ScreenInfo.height / 2.0))
        screen.blit(text, text_rect)


def main():
    """ This is the main function that runs everything else in the game. """
    pygame.init()
    config.ScreenInfo.font = pygame.font.Font("freesansbold.ttf", 24)
    screen = pygame.display.set_mode(config.ScreenInfo.size)

    # Load assets
    asset_loader = game_assets.AssetLoader()
    fish_loader = game_assets.FishLoader()
    shark_loader = game_assets.SharkLoader()
    background_loader = game_assets.BackgroundLoader()

    # Create an actor controller
    controller = ActorController(asset_loader, geometry.Vector(0,0),
            geometry.Vector(config.ScreenInfo.width, config.ScreenInfo.height))

    # Create a game manager
    manager = GameController(fish_loader, shark_loader, pygame.time.set_timer)

    # TODO switch these out with notify event triggers
    PROCESS_CUSTOM_EVENT = {
            config.EVENT_MAPPING["CREATE_NEW_FISH"]: manager.create_fish,
            config.EVENT_MAPPING["CREATE_NEW_SHARK"]: manager.create_shark,
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

        if not controller.game_over:
            screen.fill(config.Color["blue"])
            screen.blit(background_loader.main_image, pygame.Rect(0,0,config.ScreenInfo.width, config.ScreenInfo.height))

            controller.update_actors()
            controller.draw_actors(screen)
        else:
            controller.draw_game_over(screen)

        pygame.display.flip()


if __name__=="__main__":
    main()
