import pygame
import random
import math

class Algorithm():
    pass


class Sort(Algorithm):
    def __init__(self):
        super().__init__()


class Array(pygame.sprite.Group):
    STEP_SLEEP = 2000
    BACKGROUND_COLOR = pygame.Color(255, 255, 255)

    def __init__(self, screen, background, size, max_value=10, min_value=0):
        super().__init__()
        self.background = background
        self.full_screen = screen
        values = [random.randint(min_value, max_value) for i in range(0, size)]
        self.element_width = background.get_width() / size
        self.sprites = [];
        self.max_value = max_value
        self.values_range = max(abs(max_value - min_value), abs(max_value), abs(min_value))

        if(min_value >= 0 and max_value >= 0):
            ground_level = background.get_height()
        elif(min_value < 0 and max_value > 0):
            ground_level = (1 - abs(min_value) / self.values_range) * background.get_height()
        else:
            ground_level = 0

        for index, value in enumerate(values):
            element_height = abs(value) / self.values_range * background.get_height()
            if(value > 0):
                y = math.ceil(ground_level - element_height)
            else:
                y = ground_level
            x = self.element_width * index
            self.sprites.append(Element(value, x, y, self.element_width, element_height))
    
    def swap(self, i, j):
        #self.sprites[i].rect.x, self.sprites[j].rect.x = self.sprites[j].rect.x, self.sprites[i].rect.x
        self.sprites[i].image.fill(Element.CHANGE_COLOR)
        self.sprites[j].image.fill(Element.CHANGE_COLOR)
        self.sprites[i], self.sprites[j] = self.sprites[j], self.sprites[i]
        self.update()
        self.draw()
        self.full_screen.blit(self.background, (0, 0))
        pygame.display.update()
        self.sprites[i].image.fill(Element.VALUE_COLOR)
        self.sprites[j].image.fill(Element.VALUE_COLOR)
        pygame.time.wait(Array.STEP_SLEEP)

    def update(self, *args):
        for index, sprite in enumerate(self.sprites):
            sprite.update(index);

    def draw(self):
        self.background.fill(Array.BACKGROUND_COLOR)
        for sprite in self.sprites:
            self.background.blit(sprite.image, sprite.rect)
    
    def bubble_sort(self):        
        for j in range(1, len(self.sprites)):
            for i in range(len(self.sprites) - j):
                print(i, i+1)
                if(self.sprites[i] > self.sprites[i + 1]):
                    self.swap(i, i + 1)

    def sort(self):
        self.sprites.sort()


class Element(pygame.sprite.Sprite):
    VALUE_COLOR = pygame.Color(0, 149, 183)
    CHANGE_COLOR = pygame.Color(0, 183, 149)

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, value, x , y, width, height):
       # Call the parent class (Sprite) constructor
       super().__init__()

       # Set sorting value
       self.value = value

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(Element.VALUE_COLOR)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = pygame.Rect(x, y, width, height)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __ge__(self, other):
        return self.value >= other.value

    def __hash__(self):
        return self.rect.x

    def update(self, index):
        #color = pygame.Color(0, 0, int(255 * abs(self.value) / abs(values_range)), 255)
        #self.image.fill(color)
        self.rect.x = index * self.rect.width