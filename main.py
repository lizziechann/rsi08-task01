import pygame
import sys
import time

#initialise pygame
pygame.init()
#display surface
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Panda Search Game")

#load images
image1 = pygame.image.load("/Users/elizabeth/Documents/rsi08/image1.png") #grayscale
image2_panda = pygame.image.load("/Users/elizabeth/Documents/rsi08/image2.png") #panda only
image3 = pygame.image.load("/Users/elizabeth/Documents/rsi08/image3.png") #grayscale again
image4 = pygame.image.load("/Users/elizabeth/Documents/rsi08/image4.png") #search image

screen_rect = screen.get_rect()

#center image 1
image1_rect = image1.get_rect()
image1_rect.center = screen_rect.center

#image2 by placing panda centered on grayscale
image2 = image1.copy() #copying grayscale to avoid modifying og pic
grayrect = image2.get_rect() #get rect of grayscale image
panda_rect = image2_panda.get_rect() #get rect of panda image
#center panda on grayscale image
panda_rect.center = grayrect.center #aligning centers
image2.blit(image2_panda, panda_rect)
image2_rect = image2.get_rect()
image2_rect.center = screen_rect.center

# center image3
image3_rect = image3.get_rect()
image3_rect.center = screen_rect.center

# center image4
image4_rect = image4.get_rect()
image4_rect.center = screen_rect.center

#function to display an image for a set duration
def show_image_for_ms(image, rect, ms):
    screen.fill((0,0,0)) #clear screen
    screen.blit(image, rect.topleft)
    pygame.display.flip()
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))  # clear screen
        screen.blit(image, rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # limit to ~60 FPS

#main game loop (repeat 4 times)
reaction_times = []
NUM_REPETITIONS = 4

running = True
game_over = False

for trial in range(NUM_REPETITIONS):
    print(f"\nStarting trial {trial + 1}")

    #show image 1 (grayscale) for 500 ms
    show_image_for_ms(image1, image1_rect, 500)

    #show image 2 (grayscale + panda) for 1500 ms
    show_image_for_ms(image2, image2_rect, 1500)

    #show image 3 (grayscale) for 500 ms
    show_image_for_ms(image3, image3_rect, 500)

    #clear screen before displaying image 4
    screen.fill((0,0,0))
    screen.blit(image4,image4_rect.topleft)
    pygame.display.flip()

    start_time = time.time()
    clicked = False
    timeout = False

    while not clicked and not timeout:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                print(f"Trial {trial+1}: Mouse clicked at {click_pos}")

                target_x = image4_rect.left + 12
                target_y = image4_rect.top + 9
                target_width = 75
                target_height = 50
                target_rect = pygame.Rect(target_x, target_y, target_width, target_height)

                if target_rect.collidepoint(click_pos):
                    print("Correct! You clicked on the panda.")
                    reaction_times.append(time.time() - start_time)
                    clicked = True
                    game_over = True
                else:
                    print("Incorrect. Try again.")

        #timeout after 2000 ms (2 seconds)
        if (time.time() - start_time) > 2.0: #pygame uses ms, python uses s
            print (f"Trial {trial + 1}: Timeout! No click registered within 2s.")
            reaction_times.append(2.0) #record max time for timeout
            timeout = True #break loop on timeout

    if game_over:
        break

#after all trials, calculate avg rxn time
avg_rt = sum(reaction_times)/ len(reaction_times)
print (f"\nAll trials completed. Average reaction time: {avg_rt: .2f} seconds")

pygame.quit()
sys.exit()












