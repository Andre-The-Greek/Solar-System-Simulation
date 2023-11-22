import pygame as pg
from pygame.locals import *
import sys
import math     

pg.init()
    
WIDTH = 800
HEIGHT = 800
display = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Solar System")
pg.mouse.set_visible(False)
font = pg.font.get_default_font()
FONT = pg.font.Font(font, 14)
clock = pg.time.Clock()

G = 6.6743e-11
AU = 1.496e11
TIMESTEP = 3600*24
SCALE = 50 / AU
        
class Planet():        
    def __init__(self, x, y, name, mass, radius, color, sun, initial_v_x):
        self.x = x
        self.y = y
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color
        
        self.sun = sun
        self.dis_to_sun = 0
        
        self.v = pg.Vector2()
        self.v.x = initial_v_x
        self.line_points = []
    
    def calc_distance(self, p2):
        d = math.sqrt((p2.x - self.x)**2 + (p2.y - self.y)**2)
        if p2.sun:
            self.dis_to_sun = d
        return d

    def calc_angle(self, p2):
        dx = p2.x - self.x
        dy = p2.y - self.y
        angle = math.atan2(dy, dx)
        return angle
    
    def update_pos(self, planets):
        total_fx, total_fy = 0,0
        for planet in planets:
            if planet == self:
                continue
            else:
                d = self.calc_distance(planet)
                angle = self.calc_angle(planet)
                force = G * self.mass * planet.mass / d**2  # F = ma
                fx = force * math.cos(angle)
                fy = force * math.sin(angle)
                total_fx += fx
                total_fy += fy
                
        self.v.x += total_fx / self.mass * TIMESTEP
        self.v.y += total_fy / self.mass * TIMESTEP
        
        self.x += self.v.x * TIMESTEP
        self.y += self.v.y * TIMESTEP
        self.line_points.append((self.x,self.y))
        
                
    def draw(self):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        
        if len(self.line_points) > 2:
            if len(self.line_points) > 15000:
                self.line_points = self.line_points[1:]
            scaled_points = []
            for point in self.line_points:
                px, py = point
                px = px * SCALE + WIDTH / 2
                py = py * SCALE + HEIGHT / 2
                scaled_points.append((px,py))
            
            pg.draw.lines(display, self.color, False, scaled_points, 2)
        
        pg.draw.circle(display, self.color, (x, y), self.radius)
        if not self.sun: 
            name_text = FONT.render(f"{self.name}", 1, (255,255,255))
            distance_text = FONT.render(f"{round(self.dis_to_sun/1000, 1)}km", 1, (255,255,255))
            display.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_height()/2 - self.radius * 3))
            display.blit(distance_text, (x - distance_text.get_width()/2, y + distance_text.get_height()/2 + self.radius))

def main(): 
    running = True
               
    planets = [Planet(0, 0, "Sun", 1.989e30, 15, (253, 184, 19), True, 0),
               Planet(0, 1 * AU, "Earth", 5.972e24, 5, (107,147,214), False, 29.78e3),
               Planet(0, 1.5 * AU, "Mars", 6.39e23, 3, (193,68,14), False, 24.08e3),
               Planet(0, -0.7 * AU, "Venus", 4.867e24, 4, (165,124,27), False, -35.02e3),
               Planet(0, -5.2 * AU, "Jupiter", 1.89813e27, 13, (227,220,203), False, -13.06e3)]        
    
    while running:
        clock.tick(60)
        
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
        if keys[K_ESCAPE]:
            running = False
            pg.quit()
            sys.exit()
            
        display.fill((0,0,0))
        
        for planet in planets:
            planet.update_pos(planets)
            planet.draw()
            
        pg.display.flip()
        
if __name__ == "__main__": main()