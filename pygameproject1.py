import pygame
import sys
from random import randint
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface_num = test_font.render(f'{current_time//100}', False, (255,255,255))
    score_rectangle_num = score_surface_num.get_rect(center = (450,76))
    display.blit(score_surface_num, score_rectangle_num)
    
def enemy_movement(enemy_list):
    enemy_rate = 5
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= enemy_rate
            if enemy_rect.bottom == 360:
                display.blit(alien_surface1, enemy_rect) 
            elif enemy_rect.bottom == 361:
                display.blit(spaceman_surface1, enemy_rect)
            elif enemy_rect.bottom == 280:
                display.blit(ghost_surface1, enemy_rect)
            enemy_rate += 1.5
        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]

        return enemy_list
    else: 
        return []

def enemy_collision(player, enemies):
    if enemies:
        for enemy_rect in enemies:
            if player.collidepoint(enemy_rect.center): return False
    return True

def player_animation():
    global player_index, player_surface
    player_index += 0.1
    if player_index >= len(player_walk): player_index = 0
    player_surface = player_walk[int(player_index)]
    


#Initialization
pygame.init()
pygame.font.init()

#sounds
jump_sound = pygame.mixer.Sound('jumpsound.mp3')
jump_sound.set_volume(0.5)
dragonsoul = pygame.mixer.Sound('dragonsoul.mp3')
dragonsoul.set_volume(0.2)
dragonsoul.play(loops = -1)

#Screen display and clock
display = pygame.display.set_mode((576,600))
clock = pygame.time.Clock()
gameActive = False
test_font = pygame.font.Font('slkscr.ttf', 50)
start_time = 0



#Title and Screen
pygame.display.set_caption("SPACE RUSH")
icon = pygame.image.load('spacebackground.jpg')
pygame.display.set_icon(icon)
surface = pygame.image.load('space.png')
ground = pygame.image.load('ground.jpg')
alien_stand = pygame.transform.scale(pygame.image.load('tile002.png'), (250,250)).convert_alpha()
alien_stand_rect = alien_stand.get_rect(center = (288,300))
end_text1 = test_font.render('SPACE RUSH', False, (0,0,139))
end_text1_rect = end_text1.get_rect(center = (288, 75))
end_text2 = test_font.render('press space', False, (0,0,139))

end_text2_rect = end_text2.get_rect(center = (288, 500))
#Score
score_surface = test_font.render('Score: ', False, (255,255,255))
score_rectangle = score_surface.get_rect(center = (175,76))

#Timer for enemies
rate = 1350
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,rate)

#characters
player_surface1 = pygame.image.load('tile006.png').convert_alpha()
player_surface1 = pygame.transform.scale(player_surface1, (50,50))
player_surface2 = pygame.image.load('tile007.png').convert_alpha()
player_surface2 = pygame.transform.scale(player_surface2, (50,50))
player_surface3 = pygame.image.load('tile008.png').convert_alpha()
player_surface3 = pygame.transform.scale(player_surface3, (50,50))
player_walk = [player_surface1, player_surface2, player_surface3]
player_index = 0
alien_surface1 = pygame.transform.scale(pygame.image.load('tile003.png'), (50,50)).convert_alpha()
alien_surface2 = pygame.transform.scale(pygame.image.load('tile004.png'), (50,50)).convert_alpha()
alien_surface3 = pygame.transform.scale(pygame.image.load('tile005.png'), (50,50)).convert_alpha()
alien_walk = [alien_surface1, alien_surface2, alien_surface3]
alien_index = 0
ghost_surface1 = pygame.transform.scale(pygame.image.load('ghost01.png'), (50,50)).convert_alpha()
ghost_surface2 = pygame.transform.scale(pygame.image.load('ghost02.png'), (50,50)).convert_alpha()
ghost_surface3 = pygame.transform.scale(pygame.image.load('ghost03.png'), (50,50)).convert_alpha()
ghost_walk = [ghost_surface1, ghost_surface2, ghost_surface3]
spaceman_surface1 = pygame.transform.scale(pygame.image.load('spaceman1.png'), (50,50)).convert_alpha()
spaceman_surface2 = pygame.transform.scale(pygame.image.load('spaceman2.png'), (50,50)).convert_alpha()
spaceman_surface3 = pygame.transform.scale(pygame.image.load('spaceman2.png'), (50,50)).convert_alpha()
spaceman_walk = [spaceman_surface1, spaceman_surface2, spaceman_surface3]

#Enemy lists
enemy_rect_list = []

#player dimensions and position
player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (100,360))
gravity = 0
alien_surface = alien_walk[alien_index]

#Display loop
gameOver = False
while not gameOver: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if gameActive == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rectangle.bottom == 360:
                        gravity = -10
                        jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    gameActive = True
                    start_time = pygame.time.get_ticks()     
        if event.type == enemy_timer and gameActive:
            enemy_type = randint(0,2)
            if enemy_type == 2:
                enemy_rect_list.append(alien_surface.get_rect(midbottom = (randint(600,900), 360)))
            elif enemy_type == 1:
                enemy_rect_list.append(ghost_surface1.get_rect(midbottom = (randint(600,900), 280)))
            elif enemy_type == 0:
                enemy_rect_list.append(spaceman_surface1.get_rect(midbottom = (randint(600,900), 361)))
    
    if gameActive == True:
        display.blit(surface, (0,0))
        display.blit(ground, (-150,360))
        display.blit(score_surface, score_rectangle)
        display_score()
        
       

        #Jumping and gravity
        gravity += 0.5
        player_rectangle.y += gravity
        if player_rectangle.bottom >= 360 :
            player_rectangle.bottom = 360
        player_animation()
        display.blit(player_surface, player_rectangle)
        

        #Enemy 
        
        enemy_rect_list = enemy_movement(enemy_rect_list)
        gameActive = enemy_collision(player_rectangle, enemy_rect_list)
        

    else :
        display.fill((191,64, 191))
        display.blit(end_text1, end_text1_rect)
        display.blit(end_text2, end_text2_rect)
        display.blit(alien_stand, alien_stand_rect)
        enemy_rect_list.clear()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
