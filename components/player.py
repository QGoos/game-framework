from tkinter import END
import pygame
from numpy.linalg import norm
from math import floor, sqrt
from components import entity

class Player(entity.Entity):
    
    def __init__(self, x, y, width, height, speed, group) -> None:
        super().__init__(x, y, width, height, group)
        self.speed = speed
        self.pre_move = (x,y)
        self.image.fill((97, 239, 236))
        self.last_move = [0,0]
        self.setHitbox(width, height//2)

    def move(self, inputs, dt) -> None:
        '''move player'''
        mod_vect = [0, 0]
        # make sure moving on an angle is about same speed
        mod_vect[0] = sum(inputs[0:2])
        mod_vect[1] = sum(inputs[2:4])
        nm = max(norm(mod_vect),1)
        mod_vect[0] = mod_vect[0]/nm
        mod_vect[1] = mod_vect[1]/nm

        # update value
        self.last_move = [round(mod_vect[0]*self.speed*dt), round(mod_vect[1]*self.speed*dt)]
        self.rect = self.rect.move(self.last_move)
        self.hitbox = self.hitbox.move(self.last_move)


    def update(self,dt) -> None:
        '''move the Player on provided screen'''
        self.pre_move = (self.rect.x, self.rect.y)
        keys = pygame.key.get_pressed()
        input_vect = [0,0,0,0]

        # get input for movement only
        if keys[pygame.K_a]:
            input_vect[0] = -1
        if keys[pygame.K_d]:
            input_vect[1] = 1
        if keys[pygame.K_w]:
            input_vect[2] = -1
        if keys[pygame.K_s]:
            input_vect[3] = 1
        if keys[pygame.K_e]:
            self.speed = 50
        if keys[pygame.K_q]:
            self.speed = 5

        self.move(input_vect,dt)

    def collide(self, entity) -> None:
        '''check if player is colliding and fix it'''
        is_self = self.collisionRect()
        is_entity = entity.collisionRect()

        if self.getZ() == entity.getZ():
            if (is_self.colliderect(is_entity)):
                # check move direction
                if(abs(self.last_move[1]) > abs(self.last_move[0])):
                    self.hitbox.y += self.last_move[1]*-1
                    self.rect.y += self.last_move[1]*-1
                elif(abs(self.last_move[1]) < abs(self.last_move[0])):
                    self.hitbox.x += self.last_move[0]*-1
                    self.rect.x += self.last_move[0]*-1
                # account for multi directional movement
                else:
                    self.hitbox = self.hitbox.move([self.last_move[0]*-1,0])
                    self.rect = self.rect.move([self.last_move[0]*-1,0])
                    if(self.hitbox.colliderect(is_entity)):
                        self.hitbox = self.hitbox.move([self.last_move[0]*1,self.last_move[1]*-1])
                        self.rect = self.rect.move([self.last_move[0]*1,self.last_move[1]*-1])
                    if(self.hitbox.colliderect(is_entity)):
                        self.hitbox = self.hitbox.move([self.last_move[0]*-1,0])
                        self.rect = self.rect.move([self.last_move[0]*-1,0])

            
