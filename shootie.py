import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width, window_height = 1280, 720

# Create the window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Image Overlay Window")

# Load images
background_image = pygame.image.load('background.png').convert_alpha()
fade_image = pygame.image.load('fade.png').convert_alpha()
arms_image = pygame.image.load('arms.png').convert_alpha()
cursor_image = pygame.image.load('cursor.png').convert_alpha()

# Set initial scale factors for images
background_scale = 1.0
fade_scale = 0.5
arms_scale = 0.3
cursor_scale = 0.1

# Get image rects
background_rect = background_image.get_rect(center=(window_width // 2, window_height // 2))
fade_rect = fade_image.get_rect(center=(window_width // 2, window_height // 2))

# Set the size of the hitbox
hitbox_width = 100
hitbox_height = 50
fade_rect.inflate_ip(hitbox_width - fade_rect.width, hitbox_height - fade_rect.height)

# Manually adjust hitbox position to center it
fade_rect.center = (window_width // 2, window_height // 2)

arms_fixed_y = window_height - int(arms_image.get_height() * arms_scale)
arms_rect = arms_image.get_rect(bottom=arms_fixed_y, left=0)
cursor_rect = cursor_image.get_rect(center=(0, 0))

# Set up clock to control frame rate
clock = pygame.time.Clock()

# Set up variables for fading
fade_time = None
fade_duration = 2000  # 2 seconds in milliseconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fade_rect.collidepoint(pygame.mouse.get_pos()):
                fade_time = time.time() * 1000  # Record the current time in milliseconds

    # Calculate alpha value for fade image
    current_time = time.time() * 1000
    if fade_time is not None:
        elapsed_time = current_time - fade_time
        alpha_value = max(255 - (elapsed_time / fade_duration * 255), 0)
        fade_image.set_alpha(alpha_value)

        # If 2 seconds have passed, reset the fade
        if elapsed_time >= fade_duration:
            fade_time = None
            fade_image.set_alpha(255)  # Reset alpha to fully visible

    # Update the position of the arms image based on the mouse x-coordinate
    arms_rect.left = max(0, min(window_width - int(arms_image.get_width() * arms_scale), pygame.mouse.get_pos()[0]))
    arms_rect.top = window_height - int(arms_image.get_height() * arms_scale)

    # Update the position of the cursor image to follow the mouse
    cursor_rect.center = pygame.mouse.get_pos()

    # Draw everything to the screen
    screen.fill((255, 255, 255))  # Fill the background with white
    screen.blit(
        pygame.transform.scale(background_image, (int(background_image.get_width() * background_scale),
                                                  int(background_image.get_height() * background_scale))),
        (background_rect.centerx - background_rect.width * background_scale / 2,
         background_rect.centery - background_rect.height * background_scale / 2)
    )
    screen.blit(
        pygame.transform.scale(fade_image, (int(fade_image.get_width() * fade_scale),
                                            int(fade_image.get_height() * fade_scale))),
        (fade_rect.centerx - fade_rect.width * fade_scale / 2,
         fade_rect.centery - fade_rect.height * fade_scale / 2)
    )
    screen.blit(
        pygame.transform.scale(arms_image, (int(arms_image.get_width() * arms_scale),
                                            int(arms_image.get_height() * arms_scale))),
        (arms_rect.left, arms_rect.top)
    )
    screen.blit(
        pygame.transform.scale(cursor_image, (int(cursor_image.get_width() * cursor_scale),
                                              int(cursor_image.get_height() * cursor_scale))),
        (cursor_rect.centerx - cursor_rect.width * cursor_scale / 2,
         cursor_rect.centery - cursor_rect.height * cursor_scale / 2)
    )

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
