#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from .living_object import LivingObject
from ..base.game_constants import SpriteType
from .. import res
from ..base.game_constants import Facing
from ..util.path_finder import get_border_with_obstacles, find_path, ActionType
import pygame


class Enemy(LivingObject):
    __BASE_UP_SURFACE: pygame.Surface = None
    __BASE_DOWN_SURFACE: pygame.Surface = None
    __BASE_LEFT_SURFACE: pygame.Surface = None
    __BASE_RIGHT_SURFACE: pygame.Surface = None

    __SURFACE_UP: pygame.Surface = None
    __SURFACE_DOWN: pygame.Surface = None
    __SURFACE_LEFT: pygame.Surface = None
    __SURFACE_RIGHT: pygame.Surface = None

    _WIDTH = 1
    _HEIGHT = 1.5
    _ANIMATION_LENGTH = 4
    _MILISECONDS_PER_FRAME = 200
    _MOVE_COOLDOWN = 400

    IGNORED_TYPES = [SpriteType.GHOST, SpriteType.PLAYER, SpriteType.ITEM]

    def __init__(self, size):
        super().__init__(size)
        if not Enemy.__BASE_UP_SURFACE:
            Enemy.__BASE_UP_SURFACE = pygame.image.load(res.IMG_DIR + "player/sword/walk/up.png").convert_alpha()
            Enemy.__BASE_DOWN_SURFACE = pygame.image.load(res.IMG_DIR + "player/sword/walk/down.png").convert_alpha()
            Enemy.__BASE_LEFT_SURFACE = pygame.image.load(res.IMG_DIR + "player/sword/walk/left.png").convert_alpha()
            Enemy.__BASE_RIGHT_SURFACE = pygame.image.load(res.IMG_DIR + "player/sword/walk/right.png").convert_alpha()

        self.target_distance = 0

    def update(self, context):
        super().update(context)

        if self.move_cooldown_current > 0:
            return

        if self.can_attack(context, SpriteType.PLAYER):
            self.attack(context, SpriteType.PLAYER)
            return

        player = context.sprites.find_by_type(SpriteType.PLAYER)[0]

        source = self.position.x, self.position.y, self.facing.value
        target = player.position.x, player.position.y
        obstacles = [(sprite.position.x, sprite.position.y)
                     for sprite in context.sprites
                     if (sprite != self and
                         sprite.sprite_type not in Enemy.IGNORED_TYPES)
                     ]
        doors = [tuple(door.center) for door in context.sprites.find_by_type(SpriteType.DOOR)]

        path = find_path(
            source,
            target,
            get_border_with_obstacles(obstacles, doors),
            self.target_distance
        )

        if path is not None:
            facing = self.facing
            while len(path) > 0:
                step = path.pop(0)
                if step.type == ActionType.TURN:
                    self.moving = False
                    facing = Facing(step.direction)

                elif step.type == ActionType.MOVE:
                    self.move(facing, context)
                    return
            if self.facing != facing:
                self.moving = False
                self.facing = facing
                self.move_cooldown_current = self._MOVE_COOLDOWN
        else:
            self.moving = False
            rand = random.random()
            if rand < 0.1:
                self.move(self.facing, context)
            elif rand < 0.3:
                self.facing = random.choice(list(Facing))
                self.move_cooldown_current = self._MOVE_COOLDOWN
            else:
                self.move_cooldown_current = self._MOVE_COOLDOWN

    @property
    def sprite_type(self) -> SpriteType:
        return SpriteType.ENEMY

    @classmethod
    def update_render_context(cls, render_context):
        Enemy.__SURFACE_UP = pygame.transform.smoothscale(
            Enemy.__BASE_UP_SURFACE,
            (
                int(Enemy._WIDTH * cls.tile_size * Enemy._ANIMATION_LENGTH),
                int(Enemy._HEIGHT * cls.tile_size)
            )
        )
        Enemy.__SURFACE_DOWN = pygame.transform.smoothscale(
            Enemy.__BASE_DOWN_SURFACE,
            (
                int(Enemy._WIDTH * cls.tile_size * Enemy._ANIMATION_LENGTH),
                int(Enemy._HEIGHT * cls.tile_size)
            )
        )
        Enemy.__SURFACE_LEFT = pygame.transform.smoothscale(
            Enemy.__BASE_LEFT_SURFACE,
            (
                int(Enemy._WIDTH * cls.tile_size * Enemy._ANIMATION_LENGTH),
                int(Enemy._HEIGHT * cls.tile_size)
            )
        )
        Enemy.__SURFACE_RIGHT = pygame.transform.smoothscale(
            Enemy.__BASE_RIGHT_SURFACE,
            (
                int(Enemy._WIDTH * cls.tile_size * Enemy._ANIMATION_LENGTH),
                int(Enemy._HEIGHT * cls.tile_size)
            )
        )
