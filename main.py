import pygame
import math
import numpy as np
import pyaudio

pygame.font.init()

PA = pyaudio.PyAudio()
FONT = pygame.font.SysFont("Mono", 14)

WIDTH, HEIGHT = 800, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH//2, HEIGHT//2
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY = 127, 127, 127

BLUE = (100, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 0)

FPS = 200

R = 0.0821

RPM = 3000

class Cyl:
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

        self.compression_ratio = 8
        self.cylindical_vol = (math.pi * radius**2 * height)

        self.total_vol = self.cylindical_vol / 1000             # Full volume of the Cyl in L. ex. 0.5L
        self.const_vol = self.total_vol/self.compression_ratio  # Fully compressed volume that remains in the Cyl regardless of the piston position. ex. 0.0625L
        self.amplitude = (self.total_vol - self.const_vol) / 2  # Amplitude of the changing volume due to piston position ex. 0.2187
        self.mid_point = (self.total_vol + self.const_vol) / 2  # Middle point of the oscilating volume, ensures the calc does not go negative. ex. 0.2812
        
        self.stage = -1
        self.prev_stage = -1
        self.stage_text = 'Intake'
        self.base_freq = 200
        self.base_amp = 4

        if RPM == 0:
            self.omega = 0
        else:
            self.omega = (2 * math.pi) / (60 / RPM)

        self.v = self.const_vol # The vol in L
        self.t = 273.15 # Atmos Temp in Kelvin
        self.p = 1 # 1 atm
        self.n = (self.p * self.v) / (self.t * R) # No of molecules in moles.
        self.E_k = self.n * R * self.t * 1.5 # The total kinetic energy added from all the particles.


    def check_stage_transition(self):
        if self.stage != self.prev_stage:
            # print(self.starting_E_k - self.E_k)
            # match self.prev_stage:
            #     case 0:
            #         print("Intake Complete")
            #     case 1:
            #         print("Compression Complete")
            #     case 2:
            #         print("Combustion Complete")
            #     case 3:
            #         print("Exhaust Complete")
            pass

    def get_stage(self, deg):
        adjusted = (deg - 270) % 720
       
        self.prev_stage = self.stage
        if 0 <= adjusted < 180:
            self.stage = 0
            self.stage_text = "Intake"
        elif 180 <= adjusted < 360:
            self.stage = 1
            self.stage_text = "Compression"
        elif 360 <= adjusted < 540:
            self.stage = 2
            self.stage_text = "Combustion"
        elif 540 <= adjusted < 720:
            self.stage = 3
            self.stage_text = "Exhaust"
       
    

    def update(self, deg):
        t = math.radians(deg)
        nv = (self.amplitude * (math.sin(t)) + self.mid_point)

        self.t = self.E_k / (1.5 * self.n * R)
        # self.p = (self.n * R * self.t) / nv
        self.p = self.E_k / (1.5 * nv)
        self.v = nv

        self.get_stage(deg)
        self.check_stage_transition()
        

    def get_pressure(self):
        return self.n * self.t * R
    
    def get_sound_parameters(self):
        freq = self.base_freq + (self.p / self.base_amp) ** self.p
        amp = min(self.p / self.base_amp, 0.3)
        return freq, amp
   
class Piston:
    def __init__(self, crank, cyl, phase, color):
        self.cyl = cyl
        self.phase = phase
        self.color = color
        self.crank = crank
        self.state = 0
        self.ox, self.oy = 0, 0
        self.arm_len = 100
        self.half_arm_len = self.arm_len/2
        
    def draw(self):
        tdeg = self.crank.deg
        r = math.radians(tdeg)
        self.ox, self.oy = math.cos(r) * self.crank.radius, math.sin(r) * self.crank.radius
        cx, cy = HALF_WIDTH + self.ox, HALF_HEIGHT + self.oy
        
        # self.cyl.set_vol((math.sin(r) * 0.5)+0.5999999998)
        pygame.draw.rect(WINDOW, BLACK, (HALF_WIDTH-35, HALF_HEIGHT-self.arm_len*2, 70, 100))

        pygame.draw.circle(WINDOW, self.color, (cx, cy), 5)
        pygame.draw.line(WINDOW, self.color, (cx, cy), (HALF_WIDTH, cy-self.arm_len))
        pygame.draw.rect(WINDOW, self.color, (HALF_WIDTH - 25, cy - self.arm_len - self.half_arm_len, 50, self.half_arm_len))
    
    def get_vol(self):
        print(60+self.oy)
    def push(dy):
        
        pass

class Crank:
    def __init__(self, radius) -> None:
        self.radius = radius
        self.deg = 270
        self.adjusted_deg = 0
        self.speed = 2
    
    def set_speed(self, pol):
        if 0.1 <= self.speed + pol <= 10:
            self.speed += pol

    def update(self, dt):
        self.deg = (self.deg + self.speed * dt) % 720
        self.adjusted_deg = (self.deg - 270) % 720
        
    def draw(self):
        pygame.draw.circle(WINDOW, BLACK, (HALF_WIDTH, HALF_HEIGHT), self.radius)

class Slider:
    def __init__(self, x, y, min, max, value, label, round=None):
        self.x, self.y = x, y
        self.w, self.h = 100, 20
        self.half_w, self.half_h = 50, 10
        self.min, self.max = min, max
        self.value = value
        self.rendered_label = FONT.render(label, False, BLACK, WHITE)
        self.round = round

    def is_clicked(self, mx, my):
        return mx >= self.x and mx <= self.x + self.w and my >= self.y and my <= self.y + self.h
    
    def set_value(self, val):
        val -= self.x
        val = max(min(val, 100), 0)
        self.value = val

    def get_value(self):
        temp = self.value * (self.max - self.min) / 100 + self.min
        if self.round:
            temp = round(temp, self.round)
        return temp

    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(WINDOW, BLACK, (self.x, self.y + self.half_h - 1.5, self.w, 3))
        pygame.draw.circle(WINDOW, BLUE, (self.x + self.value, self.y + self.half_h), 6)
        rendered_text = FONT.render(str(self.get_value()), False, BLACK, WHITE)
        WINDOW.blit(self.rendered_label, (self.x, self.y - self.h))
        WINDOW.blit(rendered_text, (self.x + self.w + 10, self.y))
        


def render(c, crank, pistons, sliders):
    WINDOW.fill(GREY)
    rendered_c = FONT.render(str(c.stage_text), False, BLACK)
    WINDOW.blit(rendered_c, (10, 10))
    crank.draw()
    for p in pistons:
        p.draw()

    for slider in sliders:
        slider.draw()

def main():
    running = True
    clock = pygame.time.Clock()
    c = Cyl(4.5, 7.86)
    crank = Crank(50)
    pistons = [Piston(crank, c, 270, RED)]
    sliders = [
        Slider(10, 100, 50, 400, 43, " Base Frequency", 1),
        Slider(10, 140, 1, 10, 11, " Base Amplitude", 2)
        ]
    
    clicked_slider = None
    def audio_callback(in_data, frame_count, time_info, status):
        freq, amp = c.get_sound_parameters()
        samples = amp * np.sin(2 * np.pi * np.arange(frame_count) * freq / 44100)
        return (samples.astype(np.float32), pyaudio.paContinue)
    
    def get_clicked_slider(mx, my):
        for slider in sliders:
            if slider.is_clicked(mx, my):
                return slider
        return None


    stream = None
    stream = PA.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True, stream_callback=audio_callback)
    stream.start_stream()

    while running:
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        dt = clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_slider = get_clicked_slider(mx, my)

        if keys_pressed[pygame.K_w]:
            crank.set_speed(0.01)
            pass
        elif keys_pressed[pygame.K_s]:
            crank.set_speed(-0.01)
        

        if clicked_slider and mouse_pressed[0]:
            clicked_slider.set_value(pygame.mouse.get_pos()[0])

        c.base_freq = sliders[0].get_value()
        c.base_amp = sliders[1].get_value()
        render(c, crank, pistons, sliders)
        pygame.display.update()
        c.update(crank.deg)
        crank.update(dt)
       
if __name__ == "__main__":
    main()

        