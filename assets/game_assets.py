#!/bin/env python3

import json
import os
import pygame

def load_img_with_alpha(path):
    img = pygame.image.load(path)
    img.convert_alpha()
    return img

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.actor = None
        self.size = None

    def set_actor(self, actor):
        self.actor = actor
        self.rect.topleft = self.actor.state.position.to_tuple()

class SealSprite(Sprite):
    ASSET_LIST = "assets/seal_assets.json"
    def __init__(self):
        super().__init__()
        with open(self.ASSET_LIST) as json_file:
            asset_object = json.load(json_file)

        asset_dir = asset_object["directory"]
        self.main_image = load_img_with_alpha(os.path.join(asset_dir,
                asset_object["sprite"]))
        self.rect = self.main_image.get_rect() 
        # Load all animations from chomp
        self.chomp_images = [load_img_with_alpha(os.path.join(asset_dir, x))
                for x in asset_object["animations"]["chomp"]]

        # Setting a different variable so that we can update the image with
        # animations later
        self.image = self.main_image

    def update(self):
        self.actor.update()

        # Update current position
        self.rect.topleft = self.actor.state.position.to_tuple()
