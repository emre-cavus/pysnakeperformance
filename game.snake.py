import time
import pygame
import random
import math
#   EMRE CAVUS PERFORMANS ÖDEVİ
#   pip install pygame
class Game():
  def __init__(self):
    pygame.init()

    # Colors
    self.white = (255, 255, 255)
    self.black = (0, 0, 0)
    self.gray = (128, 128, 128)
    self.blue = (0, 0, 255)
    self.red = (255, 0, 0)
    self.yellow = (255, 255, 102)
    self.green = (50, 153, 213)
    # Clock
    self.clock = pygame.time.Clock()
    # Snake
    self.snake_block_size = 20
    self.snake_speed = 20
    self.snake_list = []
    self.snake_length = 1
    # Food
    self.food_block_size = 20
    # Positions
    self.display_width = 800
    self.display_height = 600
    self.x1 = self.display_width / 2
    self.y1 = self.display_height / 2
    self.x1_change = 0
    self.y1_change = 0
    self.foodx = round(random.randrange(0, self.display_width - self.snake_block_size) / 10.00) * 10.00
    self.foody = round(random.randrange(0, self.display_height - self.snake_block_size) / 10.00) * 10.00
    # Font
    self.font_size = 30
    self.font_size_factor = 10 # Factor: 30 -> 10, 60 -> 20, 50 -> 16.5 [(Centralization) Divisible of 3 (Normalize Float with {}.5)]
    self.font_style = pygame.font.SysFont("Sans", self.font_size)
    # Game
    self.display = pygame.display.set_mode((self.display_width, self.display_height))
    self.game_quit_screen_wait = 1
    self.game_over = False
    self.game_close = False
    self.should_quit = False
    self.score = 0

  def quit(self):
    pygame.quit()

  def snake(self, snake_list):
    for index, body in enumerate(snake_list, 1):
      if index == len(snake_list):
        pygame.draw.rect(self.display, self.gray, [int(body[0]), int(body[1]), self.snake_block_size, self.snake_block_size])
      else:
        pygame.draw.rect(self.display, self.black, [int(body[0]), int(body[1]), self.snake_block_size, self.snake_block_size])

  def reset(self):
    print("Resetting all the data")
    self.score = 0
    self.game_over = False
    self.game_close = False
    self.x1 = self.display_width / 2
    self.y1 = self.display_height / 2
    self.snake_list = []
    self.snake_length = 1
    self.foodx = round(random.randrange(0, self.display_width - self.snake_block_size) / 10.00) * 10.00
    self.foody = round(random.randrange(0, self.display_height - self.snake_block_size) / 10.00) * 10.00

  def message(self, msg, color, top_placement = 50):
    halfLengthOfMsg = int(math.floor(len(msg) / 2))
    renderedMessage = self.font_style.render(msg, True, color)
    self.display.blit(renderedMessage, [int((self.display_width / 2) - (halfLengthOfMsg * self.font_size_factor)), top_placement])

  def loop(self):
    if self.game_over == True:
      return

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_over = True
        self.should_quit = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
          print("Snake moves: RIGHT")
          self.x1_change = self.snake_block_size
          self.y1_change = 0
        elif event.key == pygame.K_LEFT:
          print("Snake moves: LEFT")
          self.x1_change = -self.snake_block_size
          self.y1_change = 0
        elif event.key == pygame.K_UP:
          print("Snake moves: UP")
          self.x1_change = 0
          self.y1_change = -self.snake_block_size
        elif event.key == pygame.K_DOWN:
          print("Snake moves: DOWN")
          self.x1_change = 0
          self.y1_change = self.snake_block_size

    if self.x1 >= self.display_width or self.x1 < 0 or self.y1 >= self.display_height or self.y1 < 0:
      print("Snake collide with the wall")
      self.game_close = True

    # Update the position of the snake
    self.x1 += self.x1_change
    self.y1 += self.y1_change

    # display background rengi beyaz
    self.display.fill(self.white)

    pygame.draw.rect(self.display, self.green, [int(self.foodx), int(self.foody), self.food_block_size, self.food_block_size])

    snake_head = []
    snake_head.append(self.x1)
    snake_head.append(self.y1)
    self.snake_list.append(snake_head)
    if len(self.snake_list) > self.snake_length:
      del self.snake_list[0]

    for x in self.snake_list[:-1]:
      if x == snake_head:
        self.game_close = True

    # Create the snake yılan oluşturma
    self.snake(self.snake_list)

    # ekran yenileme
    pygame.display.update()

    # yemekler
    if (abs(self.x1 - self.foodx) >= (0) and abs(self.x1 - self.foodx) <= (self.food_block_size)) and \
    (abs(self.y1 - self.foody) >= (0) and abs(self.y1 - self.foody) <= (self.food_block_size)):
      print("Collide with food!!!")
      self.foodx = round(random.randrange(0, self.display_width - self.snake_block_size) / 10.0) * 10.0
      self.foody = round(random.randrange(0, self.display_height - self.snake_block_size) / 10.0) * 10.0
      self.snake_length += 1
      self.score += 1

    self.clock.tick(self.snake_speed)

    # Printing
    print("Snake X: {:.2f} | Y: {:.2f}, Food X: {:.2f} | Y: {:.2f}".format(self.x1, self.y1, self.foodx, self.foody))
    print("Score: " + str(self.score))

  def close(self):
    self.display.fill(self.white)
    self.message("Score: " + str(self.score), self.red)
    self.message("Game Over! (Q) - Quit or (P) - Play Again", self.red, top_placement=100)

    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_over = True
        self.should_quit = True
        self.game_close = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          self.game_over = True
          self.game_close = False
        if event.key == pygame.K_p:
          self.reset()
          self.main()

  # Public
  def get_snake_position(self):
    return { "X": self.x1, "Y": self.y1 }

  def setup_display(self):
    pygame.display.update()
    pygame.display.set_caption('Snake')

  def main(self):
    # Main game loop döngü
    while not self.game_over:
      # Close loop kapatma döngüsü
      while self.game_close == True:
        self.close()
      self.loop()

    # çıkış
    if self.should_quit == True:
      print("Quit!!!")
      self.quit()

    self.display.fill(self.white)

    # 'Game Over' screen
    self.message("Finish", self.red)

    # Update  screen
    pygame.display.update()

    time.sleep(self.game_quit_screen_wait)

    # Quit game
    self.quit()

if __name__ == '__main__':
  game = Game()
  game.setup_display()
  game.main()

  for i in range(10000000):
    print(game.get_snake_position())
# emre cavus : )