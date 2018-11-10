# CREDIT: https://qwewy.gitbooks.io/pygame-module-manual/chapter1/the-mainloop.html
import platforms
import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

running = True
while running:
    time = clock.tick(fps) #similar to timerDelay

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()