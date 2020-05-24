#!/bin/env python3

import random
import pygame

import actor
import config
import events
import game_assets
import geometry

""" Controller classes """

class ActorController:
    def __init__(self, asset_loader, screen_min, screen_max):
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

    def update_actors(self):
        # Create new actors if we've received the signal
        self.listen_to_events()
        # Check for collisions
        pygame.sprite.spritecollide(self.player,
                self.fish_sprite_group, True, pygame.sprite.collide_mask) 

        result = pygame.sprite.spritecollide(self.player,
                self.shark_sprite_group, False) 
        if (result):
            events.GameEventsManager.notify_with_event(events.AteBySharkEvent())
        
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
        text = config.ScreenInfo.font.render("Fishes Eaten: " + str(self.score), True, config.Color["black"])
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
                True, config.Color["black"])
        text_rect = text.get_rect()
        # Center the text
        text_rect.center = (int(config.ScreenInfo.width / 2.0), int(config.ScreenInfo.height / 2.0))
        screen.blit(text, text_rect)


class GameController:
    MODE = [
        "STARTSCREEN",
        "PLAY",
        "ENDSCREEN"
    ]

    def __init__(self, actor_controller, background_loader):
        self.mode = self.MODE[0]

        self.handle_gamemode = {
                self.MODE[0] : self.start_screen_actions,
                self.MODE[1] : self.play_actions,
                self.MODE[2] : self.end_screen_actions,
        }

        self.transition_dict = {
                self.MODE[0]: lambda self: self.MODE[1],
                self.MODE[1]: lambda self: self.MODE[2],
                self.MODE[2]: lambda self: self.MODE[1],
        }

        self.actor_controller = actor_controller
        self.background_loader = background_loader

        self.do_reset = False

    def transition(self):
        if self.mode == self.MODE[2]:
            self.do_reset = True

        self.mode = self.transition_dict[self.mode](self)

    def active(self):
        return True if self.mode == self.MODE[1] else False

    def tick(self, screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.active():
                self.actor_controller.player.actor.add_velocity()
        if keys[pygame.K_s] and not self.active():
            # Transition modes
            self.transition()

        # Check for game ending condition
        if events.GameEventsManager.consume("got_eaten"):
            self.transition()

        # Handle game mode actions
        self.handle_gamemode[self.mode](screen)

    def press_to_continue(self, screen, text_string = "Press s to start"):
        text = config.ScreenInfo.font.render(text_string, True,
                config.Color["black"])
        text_rect = text.get_rect()
        text_rect.center = (int(config.ScreenInfo.width / 2.0),
                int(config.ScreenInfo.height * 3/4))
        screen.blit (text, text_rect)

    def start_screen_actions(self, screen):
        text = config.ScreenInfo.font.render("SMOL SEAL GOES CHOMP", True,
                config.Color["black"])
        text_rect = text.get_rect()
        text_rect.center = (int(config.ScreenInfo.width / 2.0),
                int(config.ScreenInfo.height / 2.0))
        screen.blit(text, text_rect)
        # Add the press space to continue message
        self.press_to_continue(screen)

    def play_actions(self, screen):
        screen.blit(self.background_loader.main_image,
                pygame.Rect(0,0,config.ScreenInfo.width,
                    config.ScreenInfo.height))
        self.actor_controller.update_actors()
        self.actor_controller.draw_actors(screen)

    def end_screen_actions(self, screen):
        text = config.ScreenInfo.font.render("You got eaten! You ate " +
                str(self.actor_controller.score) + " fishes. Happy Birthday!!",
                True, config.Color["black"])
        text_rect = text.get_rect()
        # Center the text
        text_rect.center = (int(config.ScreenInfo.width / 2.0), int(config.ScreenInfo.height / 2.0))
        screen.blit(text, text_rect)

        self.press_to_continue(screen, "Press s to play again")


class NpcCreator:
    def __init__(self, fish_loader, shark_loader, set_timer_fcn):
        """ Use the timer set function to initialize the relevant events """
        # Create a new fish every two seconds
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_FISH"], int(2 * 1e3))
        # Need the 0.1 offset, when the timers overlap bad things happen
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_SHARK"], int(5.1 * 1e3))

        self.fish_loader = fish_loader
        self.shark_loader = shark_loader


    def create_npc(self, npc_type, npc_size):
        npc_state = geometry.State()

        npc_state.position.x = config.ScreenInfo.width - npc_size.x
        npc_state.position.y = random.randrange(config.ScreenInfo.height - npc_size.y)

        npc_state.velocity.x = -0.4
        new_npc = npc_type(npc_state, npc_size)
        return new_npc


    def create_fish(self):
        fish_sprite = self.fish_loader.new_sprite()

        npc_size = geometry.Vector(*fish_sprite.rect.size)
        npc_fish = self.create_npc(actor.NpcFish, npc_size)

        fish_sprite.set_actor(npc_fish)
        events.GameEventsManager.notify_with_event(events.NewFishEvent(fish_sprite))


    def create_shark(self):
        shark_sprite = self.shark_loader.new_sprite()

        npc_size = geometry.Vector(*shark_sprite.rect.size)
        npc = self.create_npc(actor.NpcShark, npc_size)
        npc.state.velocity.x = -0.8

        shark_sprite.set_actor(npc)
        events.GameEventsManager.notify_with_event(events.NewSharkEvent(shark_sprite))
