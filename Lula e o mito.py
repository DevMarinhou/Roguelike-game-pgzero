import math
import random
from pgzero.rect import Rect
from pgzero.actor import Actor
from pgzero.constants import keys

# ========================= CONFIGURAÇÕES =========================
BACKGROUND_IMAGE = "bg_sala.png"
WIDTH = 960
HEIGHT = 640
TITLE = "Vote 13"

# Estados do Jogo
MENU = "MENU"
PLAYING = "PLAYING"
UPGRADE = "UPGRADE"
GAME_OVER = "GAME_OVER"

# Dimensões e Margens
ROOM_MARGIN = 40
EXIT_DOOR_RECT = Rect(WIDTH - ROOM_MARGIN - 24, HEIGHT // 2 - 50, 26, 100)

# Cores do Sistema (Procedurais e Definidas)
# Paleta Zap/Meme
ZAP_BG = (15, 25, 20)      # Fundo escuro
ZAP_GREEN = (37, 211, 102) # Verde WhatsApp
ZAP_YELLOW = (255, 214, 51)# Amarelo Br/Zap
ZAP_BLUE = (30, 136, 229)  # Azul Br/Zap

# Cores Padrão
WHITE = (245, 245, 235)
RED = (220, 60, 50)
DARK_RED = (100, 30, 30)
GOLD = (234, 190, 82)
BLUE = (80, 160, 224)
CANE = (139, 89, 48)
CANE_TIP = (255, 230, 100)

# nomes dos arquivos

SOUND_PLAYER_HIT = "player_hit"
SOUND_PLAYER_ATTACK = "player_attack"
SOUND_ENEMY_HIT = "enemy_hit"

try:
    fundo_img = pygame.image.load("bg_sala.png")
    fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))
    print("Fundo carregado com sucesso!")
except:
    fundo_img = None
      
PLAYER_SPRITE = "lula"
PLAYER_SPRITE_SIZE = (82, 84)  # Tamanho base
ENEMY_SPRITE = "bolsonaro"
ENEMY_SPRITE_SIZE = (72, 74)

# ---------- NOVOS ASSETS ----------
BACKGROUND_IMAGE = "bg_sala"   # imagem de fundo (sem extensão)
WEAPON_IMAGE = "cane"          # imagem da arma

# ========================= UTILITÁRIOS =========================
def clamp(value, low, high):
    return max(low, min(high, value))

def vector_length(x, y):
    return math.hypot(x, y)

def normalized(x, y):
    length = vector_length(x, y)
    if length == 0:
        return 0, 0
    return x / length, y / length

def angle_difference(a, b):
    return abs((a - b + math.pi) % (math.tau) - math.pi)

def circle_rect_collision(cx, cy, radius, rect):
    rx, ry, rw, rh = rect
    closest_x = clamp(cx, rx, rx + rw)
    closest_y = clamp(cy, ry, ry + rh)
    return vector_length(cx - closest_x, cy - closest_y) <= radius

def input_vector():
    x = 0
    y = 0
    if keyboard.a: x -= 1
    if keyboard.d: x += 1
    if keyboard.w: y -= 1
    if keyboard.s: y += 1
    return normalized(x, y)

def mix_color(a, b, t):
    return (int(a[0] + (b[0]-a[0])*t),
            int(a[1] + (b[1]-a[1])*t),
            int(a[2] + (b[2]-a[2])*t))

def draw_rounded_rect(rect, color, radius):
    x, y, w, h = rect
    if w < 2*radius: radius = w//2
    if h < 2*radius: radius = h//2
    screen.draw.filled_rect(Rect(x+radius, y, w-2*radius, h), color)
    screen.draw.filled_rect(Rect(x, y+radius, w, h-2*radius), color)
    screen.draw.filled_circle((x+radius, y+radius), radius, color)
    screen.draw.filled_circle((x+w-radius, y+radius), radius, color)
    screen.draw.filled_circle((x+radius, y+h-radius), radius, color)
    screen.draw.filled_circle((x+w-radius, y+h-radius), radius, color)

def draw_rounded_bar(x, y, w, h, pct, color1, color2, bg_color=(40,40,40)):
    pct = clamp(pct, 0, 1)
    draw_rounded_rect(Rect(x, y, w, h), bg_color, h//2)
    if pct > 0:
        bar_w = int(w * pct)
        if bar_w < h: bar_w = h # 
        draw_rounded_rect(Rect(x, y, bar_w, h), color1, h//2)
        draw_rounded_rect(Rect(x+2, y+2, bar_w-4, h//2-2), color2, h//4)

def draw_star(x, y, outer_r, inner_r, color):
    step = math.tau / 10
    pts = []
    for i in range(10):
        r = outer_r if i % 2 == 0 else inner_r
        angle = i * step - math.pi/2
        pts.append((int(x + r*math.cos(angle)), int(y + r*math.sin(angle))))
    
    for i in range(len(pts)):
        screen.draw.line(pts[i], pts[(i+1)%len(pts)], color)

#juice
class JuiceSystem:
    def __init__(self):
        self.screen_shake = 0
        self.screen_shake_max = 12
        self.pa_texts = [] 

    def trigger_shake(self, intensity=8):
        self.screen_shake = intensity

    def trigger_pa(self, x, y, angle):
        self.pa_texts.append([0.6, x, y, angle, 1.0]) 

    def update(self, dt):
        self.screen_shake = max(0, self.screen_shake - dt * 30)
        for pa in self.pa_texts[:]:
            pa[0] -= dt 
            pa[4] = 0.5 + 0.5 * (pa[0] / 0.6) 
            if pa[0] <= 0:
                self.pa_texts.remove(pa)

    def get_shake_offset(self):
        if self.screen_shake > 0:
            return (random.uniform(-self.screen_shake, self.screen_shake),
                    random.uniform(-self.screen_shake, self.screen_shake))
        return (0, 0)

juice = JuiceSystem()

# particuas
class Particle:
    def __init__(self, x, y, vx, vy, radius, color, life, gravity=0, fade=True, dynamic_size=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.life = life
        self.max_life = life
        self.gravity = gravity
        self.fade = fade
        self.dynamic_size = dynamic_size
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.life -= dt
        if self.life <= 0:
            self.alive = False

    def draw(self, offset_x=0, offset_y=0):
        if not self.alive:
            return
        t = self.life / self.max_life
        
        if self.dynamic_size:
            size = self.radius * (0.2 + 0.8 * t)
        else:
            size = self.radius

        if size < 1:
            return
            
        if self.fade:
            color = (int(self.color[0]*t), int(self.color[1]*t), int(self.color[2]*t))
        else:
            color = self.color
            
        screen.draw.filled_circle((int(self.x + offset_x), int(self.y + offset_y)), int(size), color)

# Global
particles = []
flash_white = 0.0
transition = False

def spawn_particles_enemy_damage(enemy, count=15):
    for _ in range(count):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(80, 220)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed - 60
        radius = random.randint(3, 7)
        color = RED if random.random() > 0.4 else WHITE
        life = random.uniform(0.5, 1.2)
        particles.append(Particle(enemy.x, enemy.y, vx, vy, radius, color, life, gravity=200))

def spawn_particles_enemy_death(enemy, count=40):
    colors = [ZAP_GREEN, ZAP_YELLOW, ZAP_BLUE]
    for _ in range(count):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(150, 350)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed - 100
        radius = random.randint(4, 9)
        color = random.choice(colors)
        life = random.uniform(0.8, 1.6)
        particles.append(Particle(enemy.x, enemy.y, vx, vy, radius, color, life, gravity=180, dynamic_size=True))

def spawn_attack_sparks(angle, x, y, range_len):
    juice.trigger_shake(6) 
    juice.trigger_pa(x + math.cos(angle) * 40, y + math.sin(angle) * 40, angle)

    for _ in range(18):
        a = angle + random.uniform(-math.pi/3, math.pi/3)
        dist = random.uniform(range_len*0.3, range_len*0.9)
        px = x + math.cos(a)*dist
        py = y + math.sin(a)*dist
        vx = math.cos(a) * random.uniform(100, 280)
        vy = math.sin(a) * random.uniform(100, 280)
        color = mix_color(GOLD, WHITE, random.random())
        radius = random.randint(3, 6)
        life = random.uniform(0.2, 0.5)
        particles.append(Particle(px, py, vx, vy, radius, color, life, gravity=50, fade=True))

# Lula (Jogador)
class Player:
    def __init__(self):
        self.actor = None
        self.weapon = None          # <-- NOVO: Actor da arma
        self.radius = 18
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.max_hp = 100
        self.hp = self.max_hp

        self.speed = 230
        self.damage = 24
        self.attack_range = 82
        self.attack_arc = math.radians(82)
        self.attack_cooldown = 0.28
        self.attack_timer = 0
        self.attack_visual_timer = 0
        self.attack_angle = 0

        self.dash_speed = 720
        self.dash_duration = 0.14
        self.dash_cooldown = 0.72
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dash_dx = 1
        self.dash_dy = 0

        self.invincible_timer = 0
        self.facing_angle = 0

        self.breathe_offset = 0
        self.star_angle = 0
        self.trail_positions = []
        self.damage_flash = 0

    def ensure_actor(self):
        if self.actor is None:
            self.actor = Actor(PLAYER_SPRITE)
            self.actor.width, self.actor.height = PLAYER_SPRITE_SIZE
            self.actor.x = self.x
            self.actor.y = self.y
        if self.weapon is None:
            self.weapon = Actor(WEAPON_IMAGE)
            self.weapon.anchor = (0, 0)  # ponto de ancoragem na empunhadura

    def reset_for_room(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dash_timer = 0
        self.attack_timer = 0
        self.attack_visual_timer = 0
        self.trail_positions.clear()
        self.ensure_actor()

    def is_dashing(self):
        return self.dash_timer > 0

    def can_take_damage(self):
        return self.invincible_timer <= 0 and not self.is_dashing()

    def take_damage(self, amount):
        if not self.can_take_damage():
            return
        self.hp = max(0, self.hp - amount)
        self.invincible_timer = 1.0
        self.damage_flash = 0.18
        juice.trigger_shake(12)
        sounds.player_hit.play()

    def start_dash(self, move_dx, move_dy):
        if self.dash_cooldown_timer > 0:
            return
        if move_dx == 0 and move_dy == 0:
            move_dx = math.cos(self.facing_angle)
            move_dy = math.sin(self.facing_angle)
        self.dash_dx, self.dash_dy = normalized(move_dx, move_dy)
        self.dash_timer = self.dash_duration
        self.dash_cooldown_timer = self.dash_cooldown
        self.invincible_timer = max(self.invincible_timer, self.dash_duration + 0.1)

    def start_attack(self, target_pos):
        if self.attack_timer > 0:
            return False
        mx, my = target_pos
        self.attack_angle = math.atan2(my - self.y, mx - self.x)
        self.facing_angle = self.attack_angle
        self.attack_timer = self.attack_cooldown
        self.attack_visual_timer = 0.13
        return True

    def update(self, dt):
        global last_mouse_pos, time
        self.attack_timer = max(0, self.attack_timer - dt)
        self.attack_visual_timer = max(0, self.attack_visual_timer - dt)
        self.dash_timer = max(0, self.dash_timer - dt)
        self.dash_cooldown_timer = max(0, self.dash_cooldown_timer - dt)
        self.invincible_timer = max(0, self.invincible_timer - dt)
        self.damage_flash = max(0, self.damage_flash - dt)

        self.breathe_offset = math.sin(time * 3) * 2
        self.star_angle += dt * 0.8

        move_dx, move_dy = input_vector()
        if self.is_dashing():
            vx = self.dash_dx * self.dash_speed
            vy = self.dash_dy * self.dash_speed
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > 6:
                self.trail_positions.pop(0)
            if random.random() < 0.4:
                particles.append(Particle(self.x, self.y, random.uniform(-20,20), random.uniform(-20,20), random.randint(3,6), BLUE, random.uniform(0.2, 0.4)))
        else:
            vx = move_dx * self.speed
            vy = move_dy * self.speed
            mx, my = last_mouse_pos
            self.facing_angle = math.atan2(my - self.y, mx - self.x)
            if len(self.trail_positions) > 0:
                self.trail_positions.pop(0)

        self.x += vx * dt
        self.y += vy * dt
        self.x = clamp(self.x, ROOM_MARGIN + self.radius, WIDTH - ROOM_MARGIN - self.radius)
        self.y = clamp(self.y, ROOM_MARGIN + self.radius, HEIGHT - ROOM_MARGIN - self.radius)

        if self.actor:
            self.actor.x = self.x
            self.actor.y = self.y + self.breathe_offset

    def draw(self, offset_x=0, offset_y=0):
        self.ensure_actor()
        px, py = self.x + offset_x, self.y + offset_y
        pa_y = py + self.breathe_offset

        
        draw_rounded_rect(Rect(int(px - 24), int(py + 14), 48, 12), (15, 20, 15), 6)

        # Aura do lula
        for i in range(5):
            angle = self.star_angle + i * math.tau/5
            dist = 52 + math.sin(time*1.5 + i)*5
            sx = px + math.cos(angle)*dist
            sy = pa_y + math.sin(angle)*dist
            draw_star(sx, sy, 8, 4, GOLD)

        # Efeitos
        if self.damage_flash > 0 and int(self.damage_flash * 20) % 2 == 0:
            self.actor.tint = (255, 100, 100)
        else:
            self.actor.tint = WHITE
            
        if self.invincible_timer > 0 and int(self.invincible_timer * 20) % 2 == 0:
            self.actor.alpha = 100
        else:
            self.actor.alpha = 255
            
        # Rastro
        for i, (tx, ty) in enumerate(self.trail_positions):
            self.actor.x, self.actor.y = tx + offset_x, ty + offset_y + self.breathe_offset
            self.actor.alpha = int(255 * (i+1)/len(self.trail_positions))
            self.actor.draw()

        # Draw do jogardor
        self.actor.x, self.actor.y = px, pa_y
        self.actor.alpha = 255 if self.can_take_damage() or self.damage_flash <= 0 else 100
        self.actor.draw()

        # draw da arma
        self.draw_cane(offset_x, offset_y)

        # area de atack
        if self.attack_visual_timer > 0:
            self.draw_attack_arc(offset_x, offset_y)

    
    def draw_cane(self, offset_x, offset_y):
        self.ensure_actor()
        px, py = self.x + offset_x, self.y + offset_y + self.breathe_offset
        # Posição da mão (lado direito do corpo)
        side_angle = self.facing_angle + math.pi/2
        hand_x = px + math.cos(side_angle) * 8
        hand_y = py + math.sin(side_angle) * 8

        # Posição arma
        self.weapon.x = hand_x
        self.weapon.y = hand_y
        self.weapon.angle = math.degrees(self.facing_angle) -90   
        self.weapon.draw()

    def draw_attack_arc(self, offset_x, offset_y):
        start = self.attack_angle - self.attack_arc/2
        steps = 14
        previous = None
        current_range = self.attack_range * (0.4 + 0.6 * (1 - self.attack_visual_timer/0.13))
        
        for i in range(steps+1):
            angle = start + self.attack_arc * i / steps
            end_x = self.x + offset_x + math.cos(angle)*current_range
            end_y = self.y + offset_y + self.breathe_offset + math.sin(angle)*current_range
            
            if previous is not None:
                screen.draw.line(previous, (end_x, end_y), mix_color(GOLD, WHITE, random.random()))
                screen.draw.filled_circle((int(end_x), int(end_y)), 2, WHITE)
                
            previous = (end_x, end_y)


# Mito (inimigo)
class Enemy:
    def __init__(self, x, y, room_number):
        self.actor = Actor(ENEMY_SPRITE)
        self.actor.x = x
        self.actor.y = y
        self.actor.width, self.actor.height = ENEMY_SPRITE_SIZE
        self.x = x
        self.y = y
        self.radius = 16
        self.max_hp = 34 + room_number * 8
        self.hp = self.max_hp
        self.speed = random.uniform(80 + room_number * 7, 120 + room_number * 10)
        self.damage = 10
        self.flash_timer = 0
        self.knockback_x = 0
        self.knockback_y = 0
        self.death_timer = 0
        self.is_dying = False
        self.scale = 1.0

    def take_damage(self, amount, attack_angle):
        self.hp -= amount
        self.flash_timer = 0.16
        k_force = 180
        self.knockback_x = math.cos(attack_angle) * k_force
        self.knockback_y = math.sin(attack_angle) * k_force
        spawn_particles_enemy_damage(self)
        sounds.enemy_hit.play()

    def is_dead(self):
        return self.hp <= 0 and not self.is_dying

    def update(self, dt, target):
        if self.is_dying:
            self.death_timer -= dt
            self.scale = max(0.01, self.death_timer / 0.7)
            self.actor.scale = self.scale
            self.actor.angle += dt * 360
            return

        self.flash_timer = max(0, self.flash_timer - dt)

        angle = math.atan2(target.y - self.y, target.x - self.x)
        
        chase_x = math.cos(angle) * self.speed
        chase_y = math.sin(angle) * self.speed

        self.x += (chase_x + self.knockback_x) * dt
        self.y += (chase_y + self.knockback_y) * dt

        self.knockback_x *= max(0, 1 - 7 * dt)
        self.knockback_y *= max(0, 1 - 7 * dt)

        self.x = clamp(self.x, ROOM_MARGIN + self.radius, WIDTH - ROOM_MARGIN - self.radius)
        self.y = clamp(self.y, ROOM_MARGIN + self.radius, HEIGHT - ROOM_MARGIN - self.radius)

        self.actor.x = self.x
        self.actor.y = self.y
        self.actor.angle = math.degrees(angle) + 90

        if self.flash_timer > 0:
            self.actor.tint = mix_color(RED, WHITE, 0.5)
        else:
            self.actor.tint = WHITE
        self.actor.scale = 1.0

    def touches(self, target):
        return vector_length(self.x - target.x, self.y - target.y) < self.radius + target.radius

    def draw(self, offset_x=0, offset_y=0):
        self.ensure_actor()
        if self.is_dying and self.death_timer <= 0:
            return
            
        ex, ey = self.actor.x + offset_x, self.actor.y + offset_y
        
        # Sombra do Inimigo
        sw = int(self.radius * 2.8 * self.scale)
        sh = int(self.radius * 1.0 * self.scale)
        if sw > 4 and sh > 4:
            draw_rounded_rect(Rect(int(ex - sw/2), int(ey+18 - sh/2), sw, sh), (15, 15, 15), sh//2)
        
        self.actor.draw()
        if not self.is_dying:
            self.draw_hp_bar(offset_x, offset_y)

    def draw_hp_bar(self, offset_x, offset_y):
        hp_width = 44
        hp_height = 5
        pct = clamp(self.hp / self.max_hp, 0, 1)
        bar_x = self.x + offset_x - hp_width/2
        bar_y = self.y + offset_y - self.radius - 14
        
        draw_rounded_rect(Rect(bar_x, bar_y, hp_width, hp_height), (40, 20, 20), 2)
        color = mix_color(RED, ZAP_GREEN, pct)
        draw_rounded_rect(Rect(bar_x, bar_y, int(hp_width*pct), hp_height), color, 2)

    def ensure_actor(self):
         self.actor.width, self.actor.height = ENEMY_SPRITE_SIZE

    def start_death(self):
        self.is_dying = True
        self.death_timer = 0.7 
        juice.trigger_shake(9) 
        spawn_particles_enemy_death(self)

# Boosters
BOON_POOL = [
    {"name": "Picanha Mística", "text": "+8 dano da bengala", "kind": "damage", "amount": 8},
    {"name": "Bengala Turbo 5G", "text": "+100 velocidade dash", "kind": "dash", "amount": 100},
    {"name": "SUS Premium", "text": "+25 HP Max e cura 25", "kind": "max_hp", "amount": 25},
    {"name": "Bênção da Véia", "text": "+16 alcance", "kind": "range", "amount": 16},
    {"name": "Cafezinho Forte", "text": "+20 velocidade", "kind": "speed", "amount": 20},
]

# Stat gb
state = MENU
player = None
enemies = []
room_number = 1
room_cleared = False
boon_options = []
last_mouse_pos = (WIDTH//2+1, HEIGHT//2)
time = 0.0

def start_new_run():
    global state, room_number, player, enemies, particles
    room_number = 1
    player = Player()
    particles.clear()
    juice.screen_shake = 0
    start_room()
    state = PLAYING

def start_room():
    global enemies, room_cleared, boon_options
    room_cleared = False
    boon_options = []
    if player:
        player.reset_for_room()
    enemies = []
    enemy_count = 3 + room_number * 2
    for _ in range(enemy_count):
        enemies.append(spawn_enemy())

def spawn_enemy():
    margin = ROOM_MARGIN + 30
    side = random.choice(("top","bottom","left","right"))
    if side == "top":
        x = random.randint(margin, WIDTH-margin)
        y = margin
    elif side == "bottom":
        x = random.randint(margin, WIDTH-margin)
        y = HEIGHT-margin
    elif side == "left":
        x = margin
        y = random.randint(margin, HEIGHT-margin)
    else:
        x = WIDTH-margin
        y = random.randint(margin, HEIGHT-margin)
    return Enemy(x, y, room_number)

def clear_room():
    global state, room_cleared, boon_options
    room_cleared = True
    boon_options = random.sample(BOON_POOL, 2)
    juice.trigger_shake(7) 
    state = UPGRADE

def apply_boon(index):
    global state
    if index < 0 or index >= len(boon_options):
        return
    boon = boon_options[index]
    amount = boon["amount"]
    if boon["kind"] == "damage":
        player.damage += amount
    elif boon["kind"] == "dash":
        player.dash_speed += amount
        player.dash_cooldown = max(0.32, player.dash_cooldown - 0.05)
    elif boon["kind"] == "max_hp":
        player.max_hp += amount
        player.hp = min(player.max_hp, player.hp + amount)
    elif boon["kind"] == "range":
        player.attack_range += amount
    elif boon["kind"] == "speed":
        player.speed += amount
    state = PLAYING

def go_to_next_room():
    global room_number, transition, flash_white
    room_number += 1
    start_room()
    transition = True
    flash_white = 0.5 

def perform_player_attack():
    hit_anything = False
    for enemy in enemies:
        if enemy.is_dying: continue
        dx = enemy.x - player.x
        dy = enemy.y - player.y
        distance = vector_length(dx, dy)
        if distance > player.attack_range + enemy.radius:
            continue
        angle_to_enemy = math.atan2(dy, dx)
        if angle_difference(angle_to_enemy, player.attack_angle) <= player.attack_arc/2:
            enemy.take_damage(player.damage, player.attack_angle)
            spawn_attack_sparks(player.attack_angle, enemy.x, enemy.y, 25)
            hit_anything = True
            sounds.player_attack.play()
            
    if hit_anything:
        juice.trigger_shake(8)

# Updat
def update(dt):
    global state, enemies, time, transition, flash_white
    time += dt
    juice.update(dt)

    for p in particles[:]:
        p.update(dt)
        if not p.alive:
            particles.remove(p)

    if transition:
        flash_white -= dt
        if flash_white <= 0:
            transition = False

    if state != PLAYING:
        return

    if player is None:
        return

    player.update(dt)

    for enemy in enemies[:]:
        if enemy.hp <= 0 and not enemy.is_dying:
            enemy.start_death()
        
        enemy.update(dt, player)
        
        if enemy.is_dying and enemy.death_timer <= 0:
            enemies.remove(enemy)

    for enemy in enemies:
        if not enemy.is_dying and enemy.touches(player):
            player.take_damage(enemy.damage)

    if player.hp <= 0:
        state = GAME_OVER
        juice.trigger_shake(15) 
        return

    if not any(e.hp > 0 for e in enemies) and not room_cleared:
        clear_room()
        return

    if room_cleared and circle_rect_collision(player.x, player.y, player.radius, EXIT_DOOR_RECT):
        go_to_next_room()

# evenbtos
def on_mouse_down(pos, button):
    global last_mouse_pos
    last_mouse_pos = pos
    if state == PLAYING and button == mouse.LEFT and player:
        if player.start_attack(pos):
            perform_player_attack()

def on_mouse_move(pos):
    global last_mouse_pos
    last_mouse_pos = pos

def on_key_down(key):
    global state
    if state == MENU:
        if key == keys.RETURN or key == keys.SPACE:
            start_new_run()
        return
    if state == PLAYING:
        if key == keys.SPACE and player:
            player.start_dash(*input_vector())
        return
    if state == UPGRADE:
        if key == keys.K_1:
            apply_boon(0)
        elif key == keys.K_2:
            apply_boon(1)
        return
    if state == GAME_OVER:
        if key == keys.R:
            start_new_run()
        elif key == keys.M:
            state = MENU

# desenhar
def draw():
    screen.clear()
    shake_x, shake_y = juice.get_shake_offset()
    
    draw_room(shake_x, shake_y)
    
    if state == MENU:
        draw_menu(shake_x, shake_y)
        return

    draw_door_and_exit(shake_x, shake_y)
    
    for enemy in enemies:
        enemy.draw(shake_x, shake_y)
        
    if player:
        player.draw(shake_x, shake_y)
        
    for p in particles:
        p.draw(shake_x, shake_y)
        
    draw_pa_texts(shake_x, shake_y)
    draw_hud()
    
    if state == UPGRADE:
        draw_upgrade_menu()
    elif state == GAME_OVER:
        draw_game_over()
        
    if (transition or flash_white > 0) and state != MENU:
        intensity = clamp(int(flash_white * 255 * 1.5), 0, 255)
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT), (intensity, intensity, intensity))

# dundo
def draw_room(offset_x, offset_y):
    if fundo_img is not None:
        screen.blit(fundo_img, (0, 0))
    else:
        # fundo preto
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (20, 20, 20))

# ---- PORTA E SAÍDA (sem alterações) ----
def draw_door_and_exit(offset_x, offset_y):
    x, y, w, h = EXIT_DOOR_RECT.x, EXIT_DOOR_RECT.y, EXIT_DOOR_RECT.width, EXIT_DOOR_RECT.height
    dx, dy = x + offset_x, y + offset_y
    
    shadow_door = Rect(dx-8, dy+10, w+16, h+20)
    draw_rounded_rect(shadow_door, (10, 15, 10), 8)
    
    door_rect = Rect(dx, dy, w, h)
    
    if not room_cleared:
        screen.draw.filled_rect(door_rect, mix_color((30,30,40), RED, 0.2))
        screen.draw.rect(door_rect, DARK_RED)
        for offset in (15, 38, 62, 85):
            screen.draw.line((dx+5, dy+offset), (dx+w-5, dy+offset), (20,20,30))
    else:
        pulse = 0.5 + 0.5 * math.sin(time * 4)
        color = mix_color(ZAP_GREEN, WHITE, 0.1 + pulse*0.2)
        screen.draw.filled_rect(door_rect, color)
        screen.draw.rect(door_rect, WHITE)
        
        for i in range(3):
            screen.draw.circle((int(dx+w//2), int(dy+h//2)), 12 + i*8, ZAP_YELLOW)

        screen.draw.text("SAIDA", center=(dx+w//2, dy+h//2), fontsize=18, color=WHITE, bold=True)

def draw_hud():
    if player is None: return
    panel_rect = Rect(16, 16, 260, 110)
    draw_rounded_rect(panel_rect, (20, 22, 20), 10)
    screen.draw.rect(panel_rect, WHITE)

    
    hp_pct = player.hp / player.max_hp
    draw_rounded_bar(62, 26, 180, 18, hp_pct, RED, WHITE)
    screen.draw.text(f"{player.hp}/{player.max_hp}", (62+190, 26), fontsize=16, color=WHITE)


    dash_pct = 1 if player.dash_cooldown_timer <= 0 else 1 - player.dash_cooldown_timer/player.dash_cooldown
    dash_color = mix_color(BLUE, WHITE, 0.3)
    draw_rounded_bar(62, 60, 180, 16, dash_pct, BLUE, dash_color, bg_color=(30, 30, 45))
    dash_text = f"Dash {player.dash_cooldown_timer:.1f}s" if player.dash_cooldown_timer > 0 else "Pronto"
    screen.draw.text(dash_text, (62+190, 60), fontsize=14, color=WHITE)

    screen.draw.text(f"Dano: {player.damage}   |   Alcance: {player.attack_range}", (62, 88), fontsize=15, color=mix_color(WHITE, GOLD, 0.5))
    
    room_text = f"STF | Sala {room_number}"
    screen.draw.text(room_text, (WIDTH-280, 20), fontsize=26, color=ZAP_YELLOW)

# Dialogo
def draw_pa_texts(offset_x, offset_y):
    for time_left, pa_x, pa_y, angle, scale in juice.pa_texts:
        px, py = pa_x + offset_x, pa_y + offset_y
        
        glow_c = ZAP_YELLOW
        screen.draw.filled_circle((int(px), int(py)), int(22*scale), (glow_c[0]//3, glow_c[1]//3, glow_c[2]//3))
        
        fontsize = int(48 * scale)
        if fontsize < 8: continue
        
        t_pa = f"13!"
        color_pa = mix_color(WHITE, ZAP_YELLOW, random.random())
        final_color = mix_color(color_pa, ZAP_BG, 1 - time_left/0.6)
        
        screen.draw.text(t_pa, center=(px, py), fontsize=fontsize, color=final_color)

# menu
def draw_menu(offset_x, offset_y):
    for y in range(HEIGHT):
        t_grad = y / HEIGHT
        bg_col = mix_color(ZAP_BG, ZAP_GREEN, t_grad * 0.4)
        screen.draw.line((0, y), (WIDTH, y), bg_col)
        
    for i in range(40):
        x = (i * 149 + math.sin(time*0.4 + i*2.1) * 40) % WIDTH
        y = (i * 89 + math.cos(time*0.6 + i*1.3) * 30) % HEIGHT
        sc_col = mix_color(GOLD, ZAP_YELLOW, random.random())
        draw_star(x, y, 9, 5, sc_col)

    shadow_o = 5
    screen.draw.text("Lula E Mito", center=(WIDTH//2 + shadow_o, 100 + shadow_o), fontsize=76, color=(10,10,10))
    screen.draw.text("Lula E Mito", center=(WIDTH//2, 100), fontsize=76, color=GOLD)
  
    panel_rect = Rect(WIDTH//2 - 250, 360, 500, 200)
    draw_rounded_rect(panel_rect, (20, 25, 20), 12)
    screen.draw.rect(panel_rect, WHITE)
    
    screen.draw.text("W-A-S-D anda  |  Espaço dar dash  |  Bt esquerdo bate", center=(WIDTH//2, 390), fontsize=24, color=WHITE)

    pulse = 0.5 + 0.5*math.sin(time*3.5)
    btn_w, btn_h = 240 + pulse*20, 60 + pulse*8
    btn_x, btn_y = WIDTH//2 - btn_w//2, 460 - btn_h//2
    
    btn_color = mix_color(RED, ZAP_GREEN, 0.4 + pulse*0.2)
    draw_rounded_rect(Rect(btn_x, btn_y, btn_w, btn_h), ZAP_YELLOW, btn_h//2) 
    draw_rounded_rect(Rect(btn_x+4, btn_y+4, btn_w-8, btn_h-8), btn_color, (btn_h-8)//2) 

    screen.draw.text("INICIAR", center=(WIDTH//2, 460), fontsize=38, color=WHITE, bold=True)
    screen.draw.text("Enter ou Espaço", center=(WIDTH//2, 530), fontsize=18, color=mix_color(WHITE, (10,10,10), 0.3))

    mx, my = WIDTH//2, 260 + math.sin(time*2)*8
    draw_rounded_rect(Rect(int(mx - 28), int(my + 10), 56, 10), (15, 15, 15), 5) # Sombra menu
    
    p_temp = Player()
    p_temp.x, p_temp.y, p_temp.ensure_actor()
    p_temp.actor.x, p_temp.actor.y = mx, my
    p_temp.actor.tint = WHITE
    p_temp.actor.draw()
    p_temp.attack_visual_timer = 0.1 
    p_temp.attack_angle = math.tau/4 
    tip_x, tip_y = mx, my + 45
    screen.draw.filled_circle((int(tip_x), int(tip_y)), 7, CANE_TIP)
    screen.draw.line((mx, my), (tip_x, tip_y), CANE)
    screen.draw.text("13!", center=(mx+45, my+60), fontsize=34, color=ZAP_YELLOW)

# pud
def draw_upgrade_menu():
    screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT), (10,10,15))
    juice.trigger_shake(0) 
    
    for i in range(3):
        screen.draw.circle((WIDTH//2, 100), 70 + i*15, ZAP_YELLOW)
    screen.draw.text("Escolha seu Boon BR", center=(WIDTH//2, 100), fontsize=52, color=GOLD, bold=True)
    
    for i, boon in enumerate(boon_options):
        bx = 160 + i*340
        by = 220
        bw, bh = 280, 220
        
        card_rect = Rect(bx, by, bw, bh)
        
        for j in range(2):
            draw_rounded_rect(Rect(bx-4+j*2, by-4+j*2, bw+8-j*4, bh+8-j*4), mix_color(GOLD, ZAP_YELLOW, random.random()), 12)
            
        card_color = (35, 30, 40)
        draw_rounded_rect(card_rect, card_color, 12)
        
        screen.draw.text(boon["name"], (bx+80, by+25), fontsize=32, color=WHITE, bold=True)
        
        t_color = mix_color(WHITE, GOLD, 0.4)
        screen.draw.text(boon["text"], (bx+20, by+100), fontsize=22, color=t_color)
        
        screen.draw.filled_circle((bx+bw//2, by+bh-35), 25, ZAP_BG)
        draw_rounded_rect(Rect(bx+bw//2-25, by+bh-60, 50, 50), mix_color(ZAP_BG, RED, 0.3), 10)
        screen.draw.text(str(i+1), center=(bx+bw//2, by+bh-35), fontsize=28, color=WHITE, bold=True)

# -Fim de hogo
def draw_game_over():
    for y in range(HEIGHT):
        t_grad = y / HEIGHT
        bg_col = mix_color((30,10,10), RED, t_grad * 0.7)
        screen.draw.line((0, y), (WIDTH, y), bg_col)
    
    offset_x = math.sin(time*30)*6
    offset_y = math.cos(time*35)*5
    
    t_over = "ACABOU O CAFEZINHO"
    screen.draw.text(t_over, center=(WIDTH//2 + offset_x, 200 + offset_y + 4), fontsize=68, color=(10,10,10))
    screen.draw.text(t_over, center=(WIDTH//2 + offset_x, 200 + offset_y), fontsize=68, color=WHITE, bold=True)
    
    room_f = max(0, room_number-1)
    screen.draw.text(f"Salas Vencidas: {room_f}", center=(WIDTH//2, 310), fontsize=34, color=mix_color(WHITE, RED, 0.5))
    
    p_rect = Rect(WIDTH//2 - 200, 380, 400, 100)
    draw_rounded_rect(p_rect, ZAP_BG, 10)
    screen.draw.rect(p_rect, WHITE)
    screen.draw.text("R para recomeçar  |  M para menu", center=(WIDTH//2, 430), fontsize=28, color=BLUE)

# ========================= MAIN =========================
if __name__ == "__main__":
    import pgzrun
    pgzrun.go()