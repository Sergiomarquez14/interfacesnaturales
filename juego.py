import cv2
import mediapipe as mp
import pygame
import sys
import random
import time

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Control de Bola con Gestos")

# Configuración de la bola
ball_color = (255, 0, 0)
ball_radius = 20
ball_start_x, ball_start_y = 320, 50  # Posición inicial en la parte superior
ball_x, ball_y = ball_start_x, ball_start_y

# Configuración de las líneas
line_color = (0, 0, 0)
line_thickness = 10
num_lines = 5
line_spacing = 480 // (num_lines + 1)
line_gap_width = 100  # Ancho del hueco en cada línea

# Generar las posiciones iniciales de los huecos en cada línea
lines = []
for i in range(num_lines):
    gap_position = random.randint(50, 540 - line_gap_width)
    lines.append((line_spacing * (i + 1), gap_position))

# Configurar mediapipe para detección de manos
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Variables para suavizar el movimiento
smoothing_factor = 0.2

# Estados del juego
state = "start"  # Puede ser "start", "playing", "win", "enter_name", o "lose"
start_time = None  # Tiempo de inicio del cronómetro
final_time = 0     # Tiempo final cuando se gana

# Almacena el nombre del jugador
player_name = ""

# Archivo de ranking
ranking_file = "ranking.txt"

# Función para mostrar texto en la pantalla
def display_text(text, size, color, y_offset=0):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(320, 240 + y_offset))
    screen.blit(text_surface, text_rect)

# Función para guardar el puntaje en el archivo de ranking
def save_score(name, time_score):
    with open(ranking_file, "a") as file:
        file.write(f"{name},{time_score:.2f}\n")

# Función para mostrar el ranking
def display_ranking():
    screen.fill((255, 255, 255))
    display_text("Ranking", 36, (0, 0, 0), -180)
    with open(ranking_file, "r") as file:
        lines = file.readlines()
        scores = [line.strip().split(",") for line in lines]
        scores = sorted(scores, key=lambda x: float(x[1]))[:5]  # Top 5
    y_offset = -100
    for i, (name, score) in enumerate(scores):
        display_text(f"{i + 1}. {name} - {score} segundos", 24, (0, 0, 0), y_offset)
        y_offset += 40

# Bucle principal del juego
while True:
    # Procesar eventos de Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Iniciar el juego al presionar cualquier tecla en la pantalla de inicio o final
            if state in ["start", "win", "lose"]:
                state = "playing"
                ball_x, ball_y = ball_start_x, ball_start_y  # Reiniciar posición de la bola
                start_time = time.time()  # Reiniciar el cronómetro
                player_name = ""  # Reiniciar el nombre

            # Captura la entrada del nombre en el estado "enter_name"
            elif state == "enter_name":
                if event.key == pygame.K_RETURN:
                    # Guardar el puntaje y pasar a la pantalla de ranking
                    save_score(player_name, final_time)
                    state = "ranking"
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

            elif state == "ranking" and event.key == pygame.K_RETURN:
                state = "start"  # Reiniciar el juego al presionar ENTER en el ranking

    # Mostrar las pantallas según el estado
    if state == "start":
        screen.fill((255, 255, 255))
        display_text("Presiona cualquier tecla para comenzar", 36, (0, 0, 0))
        pygame.display.flip()
        continue
    elif state == "win":
        screen.fill((255, 255, 255))
        display_text("¡Ganaste!", 36, (0, 255, 0))
        display_text(f"Tiempo: {final_time:.2f} segundos", 24, (0, 0, 0), -40)
        display_text("Presiona cualquier tecla para continuar", 24, (0, 0, 0), 40)
        state = "enter_name"  # Cambiar estado a ingresar nombre
        pygame.display.flip()
        continue
    elif state == "enter_name":
        screen.fill((255, 255, 255))
        display_text("Introduce tu nombre:", 36, (0, 0, 0), -40)
        display_text(player_name, 36, (0, 0, 255), 40)
        pygame.display.flip()
        continue
    elif state == "ranking":
        display_ranking()
        display_text("Presiona ENTER para volver al inicio", 24, (0, 0, 0), 180)
        pygame.display.flip()
        continue
    elif state == "lose":
        screen.fill((255, 255, 255))
        display_text("Perdiste", 36, (255, 0, 0))
        display_text("Presiona cualquier tecla para reiniciar", 24, (0, 0, 0), 40)
        pygame.display.flip()
        continue

    # Leer frame de la cámara
    ret, frame = cap.read()
    if not ret:
        break

    # Invertir el frame para que actúe como un espejo
    frame = cv2.flip(frame, 1)

    # Convertir el frame a RGB para mediapipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar manos
    results = hands.process(image_rgb)

    # Si se detecta una mano, actualizar posición del objetivo
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
            screen_width, screen_height = pygame.display.get_surface().get_size()
            target_x = int(wrist_x * screen_width)
            target_y = int(wrist_y * screen_height)

            # Suavizar el movimiento de la bola
            ball_x += (target_x - ball_x) * smoothing_factor
            ball_y += (target_y - ball_y) * smoothing_factor

    # Dibujar el fondo y las líneas
    screen.fill((255, 255, 255))  # Fondo blanco
    for y, gap_x in lines:
        pygame.draw.line(screen, line_color, (0, y), (gap_x, y), line_thickness)
        pygame.draw.line(screen, line_color, (gap_x + line_gap_width, y), (640, y), line_thickness)

        # Comprobar si la bola toca la línea, excluyendo el hueco
        if (ball_y - ball_radius <= y <= ball_y + ball_radius) and not (gap_x < ball_x < gap_x + line_gap_width):
            state = "lose"  # Cambia a estado de pérdida
            break

    # Comprobar si la bola ha llegado a la parte inferior de la pantalla (victoria)
    if ball_y >= 480 - ball_radius:
        final_time = time.time() - start_time  # Guarda el tiempo final
        state = "win"  # Cambia a estado de victoria

    # Dibujar la bola en la pantalla
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Mostrar el tiempo en pantalla mientras el estado es "playing"
    if state == "playing":
        elapsed_time = time.time() - start_time  # Tiempo transcurrido
        display_text(f"Tiempo: {elapsed_time:.2f} segundos", 24, (0, 0, 0), -200)

    # Actualizar la pantalla de Pygame
    pygame.display.flip()

    # Mostrar el frame en una ventana de OpenCV (opcional)
    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar recursos
cap.release()
