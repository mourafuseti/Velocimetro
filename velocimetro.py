# Velocímetro de Internet
# Criador: Leonardo de Moura Fuseti
# Email: mourafuseti@hotmail.com

import asyncio
import platform
import pygame
import math
import random
import socket
try:
    from ping3 import ping
    from speedtest import Speedtest
except ImportError:
    ping = None
    Speedtest = None

# Configurações
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
FONT_SIZE = 20
TITLE_FONT_SIZE = 30

# Inicialização
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Velocímetro de Internet")
font = pygame.font.SysFont('arial', FONT_SIZE)
title_font = pygame.font.SysFont('arial', TITLE_FONT_SIZE, bold=True)
clock = pygame.time.Clock()

# Estado do teste
testing = False
download_speed = 0
upload_speed = 0
test_progress = 0
test_duration = 5  # segundos
final_download_speed = 0
final_upload_speed = 0

# Sites para testar ping e IP
sites = [
    {"name": "Globo", "url": "globo.com"},
    {"name": "Google", "url": "google.com"},
    {"name": "YouTube", "url": "youtube.com"},
    {"name": "DNS Google", "url": "8.8.8.8"}
]
site_data = [{"ping": "N/A", "ip": "N/A"} for _ in sites]

# Botão
button_rect = pygame.Rect(0, 0, 100, 40)  # Posição ajustada dinamicamente
button_text = font.render("Iniciar", True, WHITE)
button_color = BLUE
button_hover_color = (100, 100, 255)

def get_ping_and_ip(url):
    try:
        ip = socket.gethostbyname(url)
        if ping:
            ping_time = ping(url, timeout=2)
            ping_time = int(round(ping_time * 1000)) if ping_time else "Falha"
        else:
            ping_time = int(round(random.uniform(10, 100)))  # Simulação
        return ping_time, ip
    except:
        return "Erro", "N/A"

def draw_gradient_arc(center, radius, start_angle, end_angle, segments=100):
    for i in range(segments):
        t = i / segments
        angle = start_angle + (end_angle - start_angle) * t
        next_angle = start_angle + (end_angle - start_angle) * ((i + 1) / segments)
        color = (
            int(GREEN[0] * (1 - t) + RED[0] * t),
            int(GREEN[1] * (1 - t) + RED[1] * t),
            int(GREEN[2] * (1 - t) + RED[2] * t)
        )
        points = [
            center,
            (center[0] + radius * math.cos(angle), center[1] - radius * math.sin(angle)),
            (center[0] + radius * math.cos(next_angle), center[1] - radius * math.sin(next_angle))
        ]
        pygame.draw.polygon(screen, color, points)

def draw_gauge(speed):
    center = (550, 250)  # À direita e acima
    radius = 150
    start_angle = math.radians(135)  # Esquerda (0 Mbps)
    end_angle = math.radians(405)    # Direita (100 Mbps)
    # Arco de fundo cinza
    pygame.draw.arc(screen, GRAY, (center[0] - radius, center[1] - radius, radius * 2, radius * 2), start_angle, end_angle, 10)
    # Arco gradiente
    draw_gradient_arc(center, radius, start_angle, end_angle)
    # Ponteiro
    max_speed = 100  # Mbps
    angle = start_angle + (end_angle - start_angle) * min(speed / max_speed, 1)
    pointer_end = (center[0] + radius * math.cos(angle), center[1] - radius * math.sin(angle))
    pygame.draw.line(screen, BLACK, center, pointer_end, 5)
    pygame.draw.circle(screen, BLACK, center, 10)  # Centro do ponteiro
    # Números
    for i, speed_label in enumerate([0, 25, 50, 75, 100]):
        label_angle = start_angle + (end_angle - start_angle) * (speed_label / max_speed)
        label_x = center[0] + (radius + 35) * math.cos(label_angle)
        label_y = center[1] - (radius + 35) * math.sin(label_angle)
        label_text = font.render(f"{speed_label}", True, BLACK)
        text_rect = label_text.get_rect(center=(label_x, label_y))
        screen.blit(label_text, text_rect)
    # Resultados de velocidade
    download_text = font.render(f"Download: {download_speed:.2f} Mbps", True, DARK_GRAY)
    upload_text = font.render(f"Upload: {upload_speed:.2f} Mbps", True, DARK_GRAY)
    screen.blit(download_text, (center[0] - download_text.get_width() // 2, center[1] + radius + 50))
    screen.blit(upload_text, (center[0] - upload_text.get_width() // 2, center[1] + radius + 75))

def draw_site_boxes():
    for i, (site, data) in enumerate(zip(sites, site_data)):
        box_rect = pygame.Rect(50, 100 + i * 90, 200, 80)
        pygame.draw.rect(screen, WHITE, box_rect)
        pygame.draw.rect(screen, DARK_GRAY, box_rect, 2)
        name_text = font.render(site["name"], True, BLACK)
        ping_text = font.render(f"Ping: {data['ping']} ms", True, DARK_GRAY)
        ip_text = font.render(f"IP: {data['ip']}", True, DARK_GRAY)
        screen.blit(name_text, (box_rect.x + 10, box_rect.y + 10))
        screen.blit(ping_text, (box_rect.x + 10, box_rect.y + 35))
        screen.blit(ip_text, (box_rect.x + 10, box_rect.y + 60))

def setup():
    global testing, test_progress
    testing = False
    test_progress = 0
    for i in range(len(sites)):
        site_data[i]["ping"], site_data[i]["ip"] = get_ping_and_ip(sites[i]["url"])

def update_loop():
    global testing, test_progress, download_speed, upload_speed, button_color, final_download_speed, final_upload_speed
    center = (550, 250)  # Centro do velocímetro
    radius = 150
    mouse_pos = pygame.mouse.get_pos()
    button_rect.center = (center[0], center[1] + radius + 140)  # Botão descido
    button_hovered = button_rect.collidepoint(mouse_pos)
    button_color = button_hover_color if button_hovered and not testing else BLUE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN and not testing:
            if button_rect.collidepoint(event.pos):
                testing = True
                test_progress = 0
                download_speed = 0
                upload_speed = 0
                # Definir velocidades finais para simulação
                final_download_speed = random.uniform(1, 50) if not Speedtest else 0
                final_upload_speed = random.uniform(1, 20) if not Speedtest else 0
    screen.fill(WHITE)
    # Título
    title_text = title_font.render("Teste de Velocidade", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    # Desenhar elementos
    draw_gauge(download_speed)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, button_rect.y + 10))
    draw_site_boxes()
    if testing:
        test_progress += 1 / (FPS * test_duration)
        if test_progress >= 1:
            testing = False
            if Speedtest:
                st = Speedtest()
                download_speed = st.download() / 1_000_000  # Mbps
                upload_speed = st.upload() / 1_000_000  # Mbps
            else:
                download_speed = final_download_speed
                upload_speed = final_upload_speed
        else:
            # Interpolação linear suave
            download_speed = final_download_speed * test_progress if not Speedtest else random.uniform(0, 50) * test_progress
            upload_speed = final_upload_speed * test_progress if not Speedtest else random.uniform(0, 20) * test_progress
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())