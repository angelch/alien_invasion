"""
Overall class to manage game assets and behaviour.
"""

import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        # make an instance of settings and use it to access them
        self.settings = Settings()
        #run the game in full screen mode: this tells to pygame to figure out
        #a window size that will fill the screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #a surface is a part of the screen where a game element is displayed
        #each element in the game, like an alien or ship, is its own surface
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        '''
        #set a specific window size for running the game
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        '''
        pygame.display.set_caption("Alien Invasion")
        # Set the background color
        self.bg_color = self.settings.bg_color
        #create a ship instance
        self.ship = Ship(self)
        #group to store all the live bullets, like a list with some extra funct
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #calling a method from within a class using dot notation
            self._check_events() #check for player input
            self.ship.update() #update the position of the ship
            self._update_bullets() #update the position of the bullets
            self._update_screen() #use the new positions to draw a new screen

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        #each keypress is registered as a KEYDOWN event
        #when the key is released it's a KEYUP event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #end the game when the player presses Q
        elif event.key == pygame.K_q:
            sys.exit()
        #a bullet is fired when the space bar is pressed
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) #add() method is similar to append()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        #when calling update on a group, the group calls update() for each
        #sprite (bullet) in the group
        self.bullets.update()
        # Deleting old bullets (the ones that have dissapeared)
        #we use a copy of the list because we cannot remove items in a loop
        for bullet in self.bullets.copy():
            #check if the bullet has reached the top of the screen
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images in the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)
        #we draw the ship on the screen by calling blitme() method
        self.ship.blitme()
        #bullets.sprites() returns a list of all sprites in the group bullets
        for bullet in self.bullets.sprites():
            #we draw all fired bullets to the screen
            bullet.draw_bullet()
        # Make the most recently drawn screen visible.
        #it updates the display constantly after moving game elements
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
