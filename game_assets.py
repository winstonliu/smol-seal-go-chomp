#!/bin/env python3

import json
import os
import pygame
import events

def load_img_with_alpha(path):
    img = pygame.image.load(path)
    img.convert_alpha()
    return img


class Animation:
    def __init__(self, image_list, num_frames):
        self.image_list = image_list
        self.num_frames = num_frames
        self.active = False
        self.index = 0

    def tick(self):
        if self.active:
            if self.index >= len(self.image_list) * self.num_frames:
                # Set animation to false if this is the last image
                self.active = False
                self.index = 0
                return None

            current_image = self.image_list[self.index // self.num_frames]
            self.index += 1

            return current_image
        return None


class AssetLoader:
    ASSET_LIST = "assets/game_assets.json"
    def __init__(self):
        with open(self.ASSET_LIST) as json_file:
            self.asset_object = json.load(json_file)

class FishLoader(AssetLoader):
    """ Factory class that produces fishes """
    ASSET_NAME = "fish"
    def __init__(self):
        super().__init__()
        fish_object = self.asset_object[self.ASSET_NAME]
        raw_path = fish_object["sprite"]
        sprite_path = os.path.join(fish_object["directory"], raw_path)

        self.main_image = self.load_images(sprite_path)

    def load_images(self, full_path):
        img = Sprite.load_images(full_path)
        # Resize fish
        img = pygame.transform.rotozoom(img, 0, 0.2)
        return img

    def new_sprite(self):
        new_sprite = FishSprite(self.main_image)
        return new_sprite

class SharkLoader(FishLoader):
    ASSET_NAME = "shark"
    def __init__(self):
        super().__init__()

    def load_images(self, full_path):
        img = Sprite.load_images(full_path)
        img = pygame.transform.rotozoom(img, 0, 0.5)
        return img

    def new_sprite(self):
        new_sprite = SharkSprite(self.main_image)
        return new_sprite

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.actor = None

    def set_actor(self, actor):
        self.actor = actor
        self.rect.topleft = self.actor.state.position.to_tuple()

    @staticmethod
    def load_images(path):
        img = pygame.image.load(path)
        img.convert_alpha()
        return img

    def update(self):
        self.actor.update()
        # Update current position
        self.rect.topleft = self.actor.state.position.to_tuple()

        # Check if actor has marked itself as delete
        if self.actor.delete:
            self.kill()


class SealSprite(Sprite):
    ASSET_NAME = "seal"
    def __init__(self, asset_loader):
        super().__init__()
        asset_object = asset_loader.asset_object[self.ASSET_NAME]
        self.asset_dir = asset_object["directory"]
        self.sprite_path = asset_object["sprite"]
        self.main_image = self.load_images(self.sprite_path)
        self.rect = self.main_image.get_rect() 

        # Load all animations from chomp
        chomp_images = [self.load_images(x) for x in
                asset_object["animations"]["chomp"]]
        self.chomp = Animation(chomp_images, 30)

        # Setting a different variable so that we can update the image with
        # animations later
        self.image = self.main_image
        # Set collision box to front quarter of the seal
        new_rect = self.image.get_rect().copy()
        new_rect.width /= 3
        new_rect.topright = self.image.get_rect().topright
        cropped_surface = self.image.subsurface(new_rect)
        full_size_surface = pygame.Surface([self.image.get_rect().width,
            self.image.get_rect().height], pygame.SRCALPHA)
        full_size_surface = full_size_surface.convert_alpha()
        full_size_surface.blit(cropped_surface, new_rect)
        self.mask = pygame.mask.from_surface(full_size_surface)

        self.current_animation = None

    def load_images(self, raw_path):
        img = Sprite.load_images(os.path.join(self.asset_dir, raw_path))

        # Resize to half the size
        img = pygame.transform.rotozoom(img, 0, 0.5)
        return img

    def update(self):
        """ Custom update function to take care of seal animations."""
        super().update()

        if events.GameEventsManager.peek("ate_fish"):
            self.chomp.active = True

        result = self.chomp.tick()
        if result:
            self.image = result
        else:
            self.image = self.main_image


class FishSprite(Sprite):
    def __init__(self, main_image):
        super().__init__()
        self.rect = main_image.get_rect() 

        # Setting a different variable so that we can update the image with
        # animations later
        self.image = main_image

    def kill(self):
        if not self.actor.delete:
            # We got eaten
            events.GameEventsManager.notify_with_event(events.AteFishEvent())
        super().kill()

class SharkSprite(FishSprite):
    def __init__(self, main_image):
        super().__init__(main_image)

    def kill(self):
        if not self.actor.delete:
            # We ate the seal
            events.GameEventsManager.notify_with_event(events.AteBySharkEvent())
        super().kill()
