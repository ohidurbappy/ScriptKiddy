import pygame
import pygame.camera
import pygame.image
import sys
from pygame import _camera_vidcapture

from pygame.locals import *
pygame.camera.init()
pygame.camera.list_cameras()

pygame.camera.Camera(0,(300,200),"RGB")
