import pygame

from algorithms import algorithm

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#ffffff"

def main():
    pygame.init()   # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY)   # Создаем окошко
    pygame.display.set_caption("AlgoVis")   # Пишем в шапку
    bg = pygame.Surface(DISPLAY)    # Создание видимой поверхности
    bg.fill(pygame.Color(BACKGROUND_COLOR)) # Заливаем поверхность сплошным цветом
    maxA = 20
    minA = 1
    sort_elements = algorithm.Array(screen, bg, size=10, max_value=maxA, min_value=minA)
    sort_elements.bubble_sort()
    #sort_elements.swap(2,8)
    #sort_elements.swap(8,2)
    #sort_elements.update()
    #sort_elements.draw(bg)
    while(True):
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == pygame.QUIT:
                raise SystemExit
        timer = pygame.time.Clock()
        timer.tick(60)
        screen.blit(bg, (0,0))  # Каждую итерацию необходимо всё перерисовывать
        pygame.display.update() # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()