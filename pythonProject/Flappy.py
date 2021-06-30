import pygame
import neat
import time
import os
import random

screen_width = 500
screen_height = 800
pygame.font.init()
bird_sprites = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
pipe_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
base_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
background_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

score_font = pygame.font.SysFont("comicsans", 50)
generation = 0


class Bird:
    sprites = bird_sprites
    max_rotation = 25
    rotation_velocity = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.sprite_count = 0
        self.current_sprite = self.sprites[0]

    def flap(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rotation_velocity

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def draw(self, window):
        self.sprite_count += 1
        if self.sprite_count < self.animation_time:
            self.current_sprite = self.sprites[0]
        elif self.sprite_count < self.animation_time * 2:
            self.current_sprite = self.sprites[1]
        elif self.sprite_count < self.animation_time * 3:
            self.current_sprite = self.sprites[2]
        elif self.sprite_count < self.animation_time * 4:
            self.current_sprite = self.sprites[1]
        elif self.sprite_count == self.animation_time * 4 + 1:
            self.current_sprite = self.sprites[0]
            self.sprite_count = 0

        if self.tilt <= -80:
            self.current_sprite = self.sprites[1]
            self.sprite_count = self.animation_time * 2

        rotated_image = pygame.transform.rotate(self.current_sprite, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.current_sprite.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.current_sprite)


class Pipe:
    gap = 200
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_sprite, False, True)
        self.pipe_bottom = pipe_sprite
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.velocity

    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_collision_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_collision_point = bird_mask.overlap(top_mask, top_offset)

        if bottom_collision_point or top_collision_point:
            return True

        return False


class Base:
    velocity = 5
    width = base_sprite.get_width()
    sprite = base_sprite

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.sprite, (self.x1, self.y))
        window.blit(self.sprite, (self.x2, self.y))


def draw_window(window, birds, pipes, base, score):
    global generation
    window.blit(background_sprite, (0, 0))
    for pipe in pipes:
        pipe.draw(window)

    text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    gen_text = score_font.render("Generation: " + str(generation), True, (255, 255, 255))
    window.blit(text, (screen_width - 10 - text.get_width(), 10))
    window.blit(gen_text, (10, 10))

    base.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def main(genomes, config):
    global generation
    generation += 1
    nets = []
    ge = []
    birds = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((screen_width, screen_height))
    run = True
    score = 0
    clock = pygame.time.Clock()
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_index = 1

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[birds.index(bird)].activate(
                (bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))
            if output[0] > 0.5:
                bird.jump()
                if bird.y <= 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        base.move()
        add_pipe = False
        removed = []

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.pipe_top.get_width() < 0:
                removed.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for pipe in removed:
            pipes.remove(pipe)

        for x, bird in enumerate(birds):
            if bird.y + bird.current_sprite.get_height() >= 730:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(window, birds, pipes, base, score)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 20)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
