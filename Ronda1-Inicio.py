import pygame
import sys
import os
import time

pygame.init()
pygame.mixer.init()

# Configuración de archivos de imágenes
RUTA_ARCHIVO_FONDO = "ciudad.jpg"
RUTA_ARCHIVO_UAIBOT = "UAIBOT.png"  # Cambiada para estar en la carpeta actual
RUTA_ARCHIVO_AUTO = "auto.png"

# Configuración de archivos de sonido
RUTA_SONIDO_SALTO = "jump.mp3"
RUTA_SONIDO_GANAR = "win.mp3"
RUTA_SONIDO_PERDER = "lose.mp3"
RUTA_MUSICA_FONDO = "background.mp3"

# Colores
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (200, 0, 0)
COLOR_AZUL = (0, 0, 200)
COLOR_VERDE = (0, 200, 0)
COLOR_AMARILLO = (255, 255, 0)
COLOR_INSTRUCCION_FONDO = (50, 50, 50)
COLOR_BARRA_ENERGIA_FONDO = (100, 100, 100)
COLOR_BARRA_ENERGIA = (0, 255, 0)
COLOR_PAUSA_FONDO = (0, 0, 0, 180)  # Negro semitransparente

# Configuración de pantalla
PANTALLA_ANCHO = 1280
PANTALLA_ALTO = 720
PISO_POS_Y = 650

# Configuración de juego
clock = pygame.time.Clock()
FPS = 60

# Inicializar pantalla
pantalla = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
pygame.display.set_caption("OFIRCA 2025 - Ronda 1 Inicio")

# Cargar imagen de fondo
img_fondo = None
if os.path.exists(RUTA_ARCHIVO_FONDO):
    try:
        img_fondo = pygame.image.load(RUTA_ARCHIVO_FONDO).convert()
        img_fondo = pygame.transform.scale(img_fondo, (PANTALLA_ANCHO, PANTALLA_ALTO))
        print("Fondo cargado correctamente")
    except pygame.error as e:
        print(f"Error cargando fondo: {e}")
        img_fondo = None

# Cargar imagen de UAIBOT
img_uaibot = None
if os.path.exists(RUTA_ARCHIVO_UAIBOT):
    try:
        img_uaibot = pygame.image.load(RUTA_ARCHIVO_UAIBOT).convert_alpha()
        img_uaibot = pygame.transform.scale(img_uaibot, (50, 50))
        print("UAIBOT cargado correctamente")
    except pygame.error as e:
        print(f"Error cargando UAIBOT: {e}")
        img_uaibot = None

# Cargar imagen de auto
img_auto = None
if os.path.exists(RUTA_ARCHIVO_AUTO):
    try:
        img_auto = pygame.image.load(RUTA_ARCHIVO_AUTO).convert_alpha()
        img_auto = pygame.transform.scale(img_auto, (100, 40))
        print("Auto cargado correctamente")
    except pygame.error as e:
        print(f"Error cargando auto: {e}")
        img_auto = None

# Cargar sonidos
sonido_salto = None
sonido_ganar = None
sonido_perder = None

# Crear sonidos básicos si no existen los archivos
print("Intentando cargar sonidos...")

if os.path.exists(RUTA_SONIDO_SALTO):
    try:
        sonido_salto = pygame.mixer.Sound(RUTA_SONIDO_SALTO)
        print("Sonido de salto cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de salto: {e}")
else:
    print(f"Archivo {RUTA_SONIDO_SALTO} no encontrado")

if os.path.exists(RUTA_SONIDO_GANAR):
    try:
        sonido_ganar = pygame.mixer.Sound(RUTA_SONIDO_GANAR)
        print("Sonido de ganar cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de ganar: {e}")
else:
    print(f"Archivo {RUTA_SONIDO_GANAR} no encontrado")

if os.path.exists(RUTA_SONIDO_PERDER):
    try:
        sonido_perder = pygame.mixer.Sound(RUTA_SONIDO_PERDER)
        print("Sonido de perder cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de perder: {e}")
else:
    print(f"Archivo {RUTA_SONIDO_PERDER} no encontrado")

# Cargar música de fondo
musica_cargada = False
if os.path.exists(RUTA_MUSICA_FONDO):
    try:
        pygame.mixer.music.load(RUTA_MUSICA_FONDO)
        pygame.mixer.music.set_volume(0.5)
        musica_cargada = True
        print("Música de fondo cargada desde archivo")
    except pygame.error as e:
        print(f"Error cargando música de fondo: {e}")
else:
    print(f"Archivo {RUTA_MUSICA_FONDO} no encontrado")

# Configuración de fuentes
font_TxtInstrucciones = pygame.font.SysFont(None, 36)
font_TxtGameOver = pygame.font.SysFont(None, 100)
font_TxtExito = pygame.font.SysFont(None, 80)
font_TxtContadores = pygame.font.SysFont(None, 32)
font_TxtPausa = pygame.font.SysFont(None, 120)
font_TxtReiniciar = pygame.font.SysFont(None, 48)

# Texto de instrucciones
txtInstrucciones = font_TxtInstrucciones.render("Usa la barra espaciadora para saltar", True, COLOR_BLANCO)
txtInstrucciones_desplazamiento = 10
txtInstrucciones_rect = txtInstrucciones.get_rect()
txtInstrucciones_rect.topleft = (10, 10)

fondo_rect = pygame.Rect(txtInstrucciones_rect.left - txtInstrucciones_desplazamiento,
                        txtInstrucciones_rect.top - txtInstrucciones_desplazamiento,
                        txtInstrucciones_rect.width + 2 * txtInstrucciones_desplazamiento,
                        txtInstrucciones_rect.height + 2 * txtInstrucciones_desplazamiento)

# Textos de fin de juego
txtGameOver = font_TxtGameOver.render("JUEGO TERMINADO", True, COLOR_ROJO)
txtGameOver_rect = txtGameOver.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))

txtExito = font_TxtExito.render("¡El paquete fue entregado con éxito!", True, COLOR_VERDE)
txtExito_rect = txtExito.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))

txtReiniciar = font_TxtReiniciar.render("Presiona 'R' para reiniciar", True, COLOR_BLANCO)
txtReiniciar_rect = txtReiniciar.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 + 50))

# Textos de pausa
txtPausa = font_TxtPausa.render("PAUSA", True, COLOR_AMARILLO)
txtPausa_rect = txtPausa.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))

txtReanudar = font_TxtReiniciar.render("Presiona 'P' para reanudar", True, COLOR_BLANCO)
txtReanudar_rect = txtReanudar.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2))

txtSalirPausa = font_TxtContadores.render("Presiona 'Q' para salir", True, COLOR_BLANCO)
txtSalirPausa_rect = txtSalirPausa.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 + 50))

# Texto para salir en pantalla de fin de juego
txtSalirFin = font_TxtContadores.render("Presiona 'Q' para salir", True, COLOR_BLANCO)
txtSalirFin_rect = txtSalirFin.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 + 100))

def reiniciar_juego():
    """Reinicia todas las variables del juego a sus valores iniciales"""
    global robot_x, robot_y, robot_vel_y, robot_en_piso
    global auto1_x, auto1_y, auto2_x, auto2_y, auto2_activo
    global fondo_x, energia_actual, kilometros_restantes, game_over, juego_ganado
    global tiempo_inicio, ultimo_tiempo, sonido_fin_reproducido, espacio_presionado
    
    # Configuración del robot/UAIBOT
    robot_x = 100
    robot_y = PISO_POS_Y - robot_tamaño
    robot_vel_y = 0
    robot_en_piso = True
    
    # Configuración de los autos
    auto1_x = PANTALLA_ANCHO
    auto1_y = PISO_POS_Y - auto_alto
    auto2_x = PANTALLA_ANCHO + PANTALLA_ANCHO // 2  # Empieza más lejos
    auto2_y = PISO_POS_Y - auto_alto
    auto2_activo = False
    
    # Configuración de animación de fondo
    fondo_x = 0
    
    # Configuración de energía y tiempo
    energia_actual = energia_maxima
    tiempo_inicio = time.time()
    
    # Configuración de kilómetros
    kilometros_restantes = kilometros_objetivo
    
    # Estados del juego
    game_over = False
    juego_ganado = False
    ultimo_tiempo = time.time()
    sonido_fin_reproducido = False
    espacio_presionado = False
    
    # Reiniciar música
    if musica_cargada:
        pygame.mixer.music.play(-1)
        print("Música reiniciada")

# Configuración del robot/UAIBOT
robot_tamaño = 50
robot_x = 100
robot_y = PISO_POS_Y - robot_tamaño
robot_vel_y = 0
robot_salto_normal = -15
robot_salto_alto = -22
robot_gravedad = 0.8
robot_en_piso = True

# Configuración de los autos (ahora 2 autos)
auto_ancho = 100
auto_alto = 40
auto1_x = PANTALLA_ANCHO
auto1_y = PISO_POS_Y - auto_alto
auto2_x = PANTALLA_ANCHO + PANTALLA_ANCHO // 2  # Auto 2 empieza más lejos
auto2_y = PISO_POS_Y - auto_alto
auto2_activo = False  # El auto 2 no está activo al inicio
auto_vel_x = 7

# Configuración de animación de fondo
fondo_x = 0
fondo_vel_x = 2

# Configuración de energía y tiempo
energia_maxima = 60.0  # 60 segundos
energia_actual = energia_maxima
tiempo_inicio = time.time()

# Configuración de kilómetros
kilometros_objetivo = 1.0
kilometros_restantes = kilometros_objetivo
kilometros_por_segundo = 0.03

# Estados del juego
juegoEnEjecucion = True
game_over = False
juego_ganado = False
juego_pausado = False
ultimo_tiempo = time.time()
sonido_fin_reproducido = False
espacio_presionado = False  # Para controlar el salto

# Iniciar música de fondo
if musica_cargada:
    pygame.mixer.music.play(-1)
    print("Música de fondo iniciada")

# Bucle principal del juego
while juegoEnEjecucion:
    clock.tick(FPS)
    
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juegoEnEjecucion = False
            
        if event.type == pygame.KEYDOWN:
            # Salir del juego con 'Q'
            if event.key == pygame.K_q:
                juegoEnEjecucion = False
            
            # Pausa/Reanudar
            if event.key == pygame.K_p and not game_over and not juego_ganado:
                juego_pausado = not juego_pausado
                if juego_pausado:
                    pygame.mixer.music.pause()
                    print("Juego pausado - música pausada")
                else:
                    pygame.mixer.music.unpause()
                    ultimo_tiempo = time.time()  # Resetear tiempo para evitar saltos
                    print("Juego reanudado - música reanudada")
            
            # Reiniciar juego
            if event.key == pygame.K_r and (game_over or juego_ganado):
                pygame.mixer.music.stop()  # Detener música antes de reiniciar
                reiniciar_juego()
            
            # Salto (solo si el juego está activo y no pausado)
            if (event.key == pygame.K_SPACE and robot_en_piso and 
                not game_over and not juego_ganado and not juego_pausado and not espacio_presionado):
                robot_vel_y = robot_salto_normal
                robot_en_piso = False
                espacio_presionado = True
                if sonido_salto:
                    sonido_salto.play()
                    print("Sonido de salto reproducido")
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                espacio_presionado = False
    
    # Solo actualizar el juego si no está pausado
    if not juego_pausado:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - ultimo_tiempo
        ultimo_tiempo = tiempo_actual
        
        # Dibujar fondo animado
        if img_fondo:
            # Animar el fondo para crear sensación de velocidad
            if not game_over and not juego_ganado:
                fondo_x -= fondo_vel_x
                if fondo_x <= -PANTALLA_ANCHO:
                    fondo_x = 0
            
            # Dibujar dos copias del fondo para el efecto de scroll infinito
            fondo_desplazamiento_y = -(PANTALLA_ALTO - PISO_POS_Y)
            pantalla.blit(img_fondo, (fondo_x, fondo_desplazamiento_y))
            pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, fondo_desplazamiento_y))
        else:
            pantalla.fill(COLOR_BLANCO)
        
        # Dibujar el piso
        piso_altura = PANTALLA_ALTO - PISO_POS_Y
        piso_rect = pygame.Rect(0, PISO_POS_Y, PANTALLA_ANCHO, piso_altura)
        pygame.draw.rect(pantalla, COLOR_VERDE, piso_rect)
        pygame.draw.line(pantalla, COLOR_NEGRO, (0, PISO_POS_Y), (PANTALLA_ANCHO, PISO_POS_Y), 3)
        
        # Lógica del juego solo si no está terminado
        if not game_over and not juego_ganado:
            # Actualizar energía
            energia_actual -= tiempo_transcurrido
            if energia_actual <= 0:
                energia_actual = 0
                game_over = True
            
            # Actualizar kilómetros
            kilometros_restantes -= kilometros_por_segundo * tiempo_transcurrido
            if kilometros_restantes <= 0:
                kilometros_restantes = 0
                juego_ganado = True
            
            # Mover autos
            auto1_x -= auto_vel_x
            auto2_x -= auto_vel_x
            
            # Auto 1: Si sale de los límites, reaparece
            if auto1_x < -auto_ancho:
                auto1_x = PANTALLA_ANCHO
            
            # Auto 2: Activar cuando el auto 1 llega a la mitad del mapa
            if auto1_x <= PANTALLA_ANCHO // 2 and not auto2_activo:
                auto2_activo = True
                print("Auto 2 activado")
            
            # Auto 2: Si sale de los límites, reaparece (solo si está activo)
            if auto2_activo and auto2_x < -auto_ancho:
                auto2_x = PANTALLA_ANCHO
            
            # Manejar salto con mecánica mejorada (una sola pulsación)
            keys = pygame.key.get_pressed()
            
            # Física del salto del robot
            if not robot_en_piso:
                # Si mantiene presionada la barra espaciadora, salto más alto
                if keys[pygame.K_SPACE] and robot_vel_y < 0:
                    robot_vel_y += robot_gravedad * 0.3  # Gravedad reducida mientras mantiene presionado
                else:
                    robot_vel_y += robot_gravedad
                
                robot_y += robot_vel_y
                
                # Verificar si toca el piso
                if robot_y >= PISO_POS_Y - robot_tamaño:
                    robot_y = PISO_POS_Y - robot_tamaño
                    robot_vel_y = 0
                    robot_en_piso = True
            
            # Detectar colisión con auto 1
            robot_rect = pygame.Rect(robot_x, robot_y, robot_tamaño, robot_tamaño)
            auto1_rect = pygame.Rect(auto1_x, auto1_y, auto_ancho, auto_alto)
            
            if robot_rect.colliderect(auto1_rect):
                game_over = True
                print("Colisión con auto 1")
            
            # Detectar colisión con auto 2 (solo si está activo)
            if auto2_activo:
                auto2_rect = pygame.Rect(auto2_x, auto2_y, auto_ancho, auto_alto)
                if robot_rect.colliderect(auto2_rect):
                    game_over = True
                    print("Colisión con auto 2")
        
        # Reproducir sonidos de fin de juego (solo una vez)
        if not sonido_fin_reproducido:
            if game_over:
                pygame.mixer.music.stop()  # Detener música inmediatamente
                if sonido_perder:
                    sonido_perder.play()
                    print("Sonido de perder reproducido")
                sonido_fin_reproducido = True
            elif juego_ganado:
                pygame.mixer.music.stop()  # Detener música inmediatamente
                if sonido_ganar:
                    sonido_ganar.play()
                    print("Sonido de ganar reproducido")
                sonido_fin_reproducido = True
        
        # Dibujar UAIBOT (robot)
        if img_uaibot:
            pantalla.blit(img_uaibot, (robot_x, robot_y))
        else:
            robot_rect = pygame.Rect(robot_x, robot_y, robot_tamaño, robot_tamaño)
            pygame.draw.rect(pantalla, COLOR_AZUL, robot_rect)
        
        # Dibujar auto 1
        if img_auto:
            pantalla.blit(img_auto, (auto1_x, auto1_y))
        else:
            auto1_rect = pygame.Rect(auto1_x, auto1_y, auto_ancho, auto_alto)
            pygame.draw.rect(pantalla, COLOR_ROJO, auto1_rect)
        
        # Dibujar auto 2 (solo si está activo)
        if auto2_activo:
            if img_auto:
                pantalla.blit(img_auto, (auto2_x, auto2_y))
            else:
                auto2_rect = pygame.Rect(auto2_x, auto2_y, auto_ancho, auto_alto)
                pygame.draw.rect(pantalla, COLOR_ROJO, auto2_rect)
        
        # Dibujar barra de energía
        barra_energia_ancho = 200
        barra_energia_alto = 30
        barra_energia_x = PANTALLA_ANCHO - barra_energia_ancho - 20
        barra_energia_y = 20
        
        # Fondo de la barra
        pygame.draw.rect(pantalla, COLOR_BARRA_ENERGIA_FONDO, 
                        (barra_energia_x, barra_energia_y, barra_energia_ancho, barra_energia_alto))
        
        # Barra de energía actual
        porcentaje_energia = energia_actual / energia_maxima
        ancho_energia_actual = int(barra_energia_ancho * porcentaje_energia)
        if ancho_energia_actual > 0:
            color_energia = COLOR_BARRA_ENERGIA if porcentaje_energia > 0.3 else COLOR_ROJO
            pygame.draw.rect(pantalla, color_energia, 
                            (barra_energia_x, barra_energia_y, ancho_energia_actual, barra_energia_alto))
        
        # Texto del porcentaje de energía
        porcentaje_texto = f"{int(porcentaje_energia * 100)}%"
        txt_porcentaje = font_TxtContadores.render(porcentaje_texto, True, COLOR_BLANCO)
        txt_porcentaje_rect = txt_porcentaje.get_rect(center=(barra_energia_x + barra_energia_ancho // 2, 
                                                             barra_energia_y + barra_energia_alto // 2))
        pantalla.blit(txt_porcentaje, txt_porcentaje_rect)
        
        # Dibujar contador de kilómetros
        km_texto = f"Kilómetros restantes: {kilometros_restantes:.2f} km"
        txt_kilometros = font_TxtContadores.render(km_texto, True, COLOR_BLANCO)
        txt_km_rect = pygame.Rect(20, PANTALLA_ALTO - 60, txt_kilometros.get_width() + 20, 40)
        pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO, txt_km_rect)
        pantalla.blit(txt_kilometros, (30, PANTALLA_ALTO - 50))
        
        # Dibujar instrucciones solo si el juego está en curso
        if not game_over and not juego_ganado:
            pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO, fondo_rect)
            pantalla.blit(txtInstrucciones, txtInstrucciones_rect)
        
        # Pantalla de Game Over
        if game_over:
            # Fondo semitransparente
            overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
            overlay.set_alpha(150)
            overlay.fill(COLOR_NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            pantalla.blit(txtGameOver, txtGameOver_rect)
            pantalla.blit(txtReiniciar, txtReiniciar_rect)
            pantalla.blit(txtSalirFin, txtSalirFin_rect)
        
        # Pantalla de éxito
        if juego_ganado:
            # Fondo semitransparente
            overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
            overlay.set_alpha(150)
            overlay.fill(COLOR_NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            pantalla.blit(txtExito, txtExito_rect)
            pantalla.blit(txtReiniciar, txtReiniciar_rect)
            pantalla.blit(txtSalirFin, txtSalirFin_rect)
    
    else:  # Juego pausado
        # Redibujar la última pantalla pero sin actualizaciones
        if img_fondo:
            fondo_desplazamiento_y = -(PANTALLA_ALTO - PISO_POS_Y)
            pantalla.blit(img_fondo, (fondo_x, fondo_desplazamiento_y))
            pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, fondo_desplazamiento_y))
        else:
            pantalla.fill(COLOR_BLANCO)
        
        # Dibujar elementos estáticos
        piso_altura = PANTALLA_ALTO - PISO_POS_Y
        piso_rect = pygame.Rect(0, PISO_POS_Y, PANTALLA_ANCHO, piso_altura)
        pygame.draw.rect(pantalla, COLOR_VERDE, piso_rect)
        pygame.draw.line(pantalla, COLOR_NEGRO, (0, PISO_POS_Y), (PANTALLA_ANCHO, PISO_POS_Y), 3)
        
        # Dibujar personajes
        if img_uaibot:
            pantalla.blit(img_uaibot, (robot_x, robot_y))
        else:
            robot_rect = pygame.Rect(robot_x, robot_y, robot_tamaño, robot_tamaño)
            pygame.draw.rect(pantalla, COLOR_AZUL, robot_rect)
        
        if img_auto:
            pantalla.blit(img_auto, (auto1_x, auto1_y))
            if auto2_activo:
                pantalla.blit(img_auto, (auto2_x, auto2_y))
        else:
            auto1_rect = pygame.Rect(auto1_x, auto1_y, auto_ancho, auto_alto)
            pygame.draw.rect(pantalla, COLOR_ROJO, auto1_rect)
            if auto2_activo:
                auto2_rect = pygame.Rect(auto2_x, auto2_y, auto_ancho, auto_alto)
                pygame.draw.rect(pantalla, COLOR_ROJO, auto2_rect)
        
        # Overlay de pausa
        overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        overlay.set_alpha(180)
        overlay.fill(COLOR_NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        pantalla.blit(txtPausa, txtPausa_rect)
        pantalla.blit(txtReanudar, txtReanudar_rect)
        pantalla.blit(txtSalirPausa, txtSalirPausa_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()