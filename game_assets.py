#!/bin/env python3

import json
import os
import pygame

def load_img_with_alpha(path):
    img = pygame.image.load(path)
    img.convert_alpha()
    return img


class AssetLoader:
    ASSET_LIST = "assets/game_assets.json"
    def __init__(self):
        with open(self.ASSET_LIST) as json_file:
            self.asset_object = json.load(json_file)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, asset_object):
        super().__init__()
        self.actor = None
        self.size = None
        self.asset_object = asset_object
        self.asset_dir = self.asset_object["directory"]
        self.sprite_path = self.asset_object["sprite"]

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


class SealSprite(Sprite):
    ASSET_NAME = "seal"
    def __init__(self, asset_loader):
        super().__init__(asset_loader.asset_object[self.ASSET_NAME])
        self.main_image = self.load_images(self.sprite_path)
        self.rect = self.main_image.get_rect() 

        # Load all animations from chomp
        self.chomp_images = [self.load_images(x) for x in
                self.asset_object["animations"]["chomp"]]

        # Setting a different variable so that we can update the image with
        # animations later
        self.image = self.main_image

    def load_images(self, raw_path):
        img = Sprite.load_images(os.path.join(self.asset_dir, raw_path))

        # Resize to half the size
        img = pygame.transform.rotozoom(img, 0, 0.5)
        return img


class FishSprite(Sprite):
    ASSET_NAME = "fish"
    def __init__(self, asset_loader):
        super().__init__(asset_loader.asset_object[self.ASSET_NAME])
        self.main_image = self.load_images(self.sprite_path)
        self.rect = self.main_image.get_rect() 

        # Setting a different variable so that we can update the image with
        # animations later
        self.image = self.main_image

    def load_images(self, raw_path):
        img = Sprite.load_images(os.path.join(self.asset_dir, raw_path))

        # Resize fish
        img = pygame.transform.rotozoom(img, 0, 0.2)
        return img

