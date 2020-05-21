#!/bin/env python3

import json
import os
import pygame
import events

def load_img_with_alpha(path):
    img = pygame.image.load(path)
    img.convert_alpha()
    return img


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
        self.chomp_images = [self.load_images(x) for x in
                asset_object["animations"]["chomp"]]

        # Setting a different variable so that we can update the image with
        # animations later
        self.image = self.main_image

    def load_images(self, raw_path):
        img = Sprite.load_images(os.path.join(self.asset_dir, raw_path))

        # Resize to half the size
        img = pygame.transform.rotozoom(img, 0, 0.5)
        return img


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
