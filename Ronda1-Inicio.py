import pygame
import sys
import os
import time
import random

pygame.init()
pygame.mixer.init()

#Configuración de archivos de imágenes
RUTA_ARCHIVO_FONDO = "ciudad.jpg"
RUTA_ARCHIVO_UAIBOT = "UAIBOT.png"
RUTA_ARCHIVO_AUTO = "auto.png"
RUTA_ARCHIVO_INICIO = "inicio.jpg"  #Nueva imagen de pantalla de inicio

#Configuración de archivos de sonido
RUTA_SONIDO_SALTO = "salto.ganar"
RUTA_SONIDO_GANAR = "ganar.ganar"
RUTA_SONIDO_PERDER = "perder.ganar"
RUTA_SONIDO_POWERUP = "powerup.ganar"  #Nuevo sonido para power-up
RUTA_MUSICA_FONDO = "fondo.mp3"

#Colores
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (200, 0, 0)
COLOR_AZUL = (0, 0, 200)
COLOR_VERDE = (0, 200, 0)
COLOR_AMARILLO = (255, 255, 0)
COLOR_DORADO = (255, 215, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_INSTRUCCION_FONDO = (50, 50, 50)
COLOR_BARRA_ENERGIA_FONDO = (100, 100, 100)
COLOR_BARRA_ENERGIA = (0, 255, 0)
COLOR_PAUSA_FONDO = (0, 0, 0, 180)

#Configuración de pantalla
PANTALLA_ANCHO = 1280
PANTALLA_ALTO = 720
PISO_POS_Y = 650

#Estados del juego
ESTADO_INICIO = 0
ESTADO_INSTRUCCIONES = 1
ESTADO_JUGANDO = 2
ESTADO_PAUSA = 3
ESTADO_FIN = 4

#Configuración de juego
clock = pygame.time.Clock()
FPS = 60

#Inicializar pantalla
pantalla = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
pygame.display.set_caption("OFIRCA 2025 - Ronda 1 Inicio")

#Cargar imagen de inicio
img_inicio = None
if os.path.exists(RUTA_ARCHIVO_INICIO):
    try:
        img_inicio = pygame.image.load(RUTA_ARCHIVO_INICIO).convert()
        img_inicio = pygame.transform.scale(img_inicio, (PANTALLA_ANCHO, PANTALLA_ALTO))
        print("Imagen de inicio cargada correctamente")
    except pygame.error as e:
        print(f"Error cargando imagen de inicio: {e}")

#Cargar imagen de fondo
img_fondo = None
if os.path.exists(RUTA_ARCHIVO_FONDO):
    try:
        img_fondo = pygame.image.load(RUTA_ARCHIVO_FONDO).convert()
        img_fondo = pygame.transform.scale(img_fondo, (PANTALLA_ANCHO, PANTALLA_ALTO))
        print("Fondo cargado correctamente")
    except pygame.error as e:
        print(f"Error cargando fondo: {e}")

#Cargar imagen de UAIBOT
img_uaibot = None
if os.path.exists(RUTA_ARCHIVO_UAIBOT):
    try:
        img_uaibot = pygame.image.load(RUTA_ARCHIVO_UAIBOT).convert_alpha()
        img_uaibot = pygame.transform.scale(img_uaibot, (50, 50))
        print("UAIBOT cargado correctamente")
    except pygame.error as e:
        print(f"Error cargando UAIBOT: {e}")

#Cargar imagen de auto
img_auto = None
if os.path.exists(RUTA_ARCHIVO_AUTO):
    try:
        img_auto = pygame.image.load(RUTA_ARCHIVO_AUTO).convert_alpha()
        img_auto = pygame.transform.scale(img_auto, (100, 40))
        print("Auto cargado correctamente")
    except pygame.error as e:
        print(f"Error cargando auto: {e}")

#Cargar sonidos
sonido_salto = None
sonido_ganar = None
sonido_perder = None
sonido_powerup = None

print("Intentando cargar sonidos...")

if os.path.exists(RUTA_SONIDO_SALTO):
    try:
        sonido_salto = pygame.mixer.Sound(RUTA_SONIDO_SALTO)
        print("Sonido de salto cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de salto: {e}")

if os.path.exists(RUTA_SONIDO_GANAR):
    try:
        sonido_ganar = pygame.mixer.Sound(RUTA_SONIDO_GANAR)
        print("Sonido de ganar cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de ganar: {e}")

if os.path.exists(RUTA_SONIDO_PERDER):
    try:
        sonido_perder = pygame.mixer.Sound(RUTA_SONIDO_PERDER)
        print("Sonido de perder cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de perder: {e}")

if os.path.exists(RUTA_SONIDO_POWERUP):
    try:
        sonido_powerup = pygame.mixer.Sound(RUTA_SONIDO_POWERUP)
        print("Sonido de power-up cargado desde archivo")
    except pygame.error as e:
        print(f"Error cargando sonido de power-up: {e}")

#Cargar música de fondo
musica_cargada = False
if os.path.exists(RUTA_MUSICA_FONDO):
    try:
        pygame.mixer.music.load(RUTA_MUSICA_FONDO)
        pygame.mixer.music.set_volume(0.5)
        musica_cargada = True
        print("Música de fondo cargada desde archivo")
    except pygame.error as e:
        print(f"Error cargando música de fondo: {e}")

#Configuración de fuentes
font_titulo = pygame.font.SysFont(None, 120)
font_subtitulo = pygame.font.SysFont(None, 48)
font_TxtInstrucciones = pygame.font.SysFont(None, 36)
font_TxtGameOver = pygame.font.SysFont(None, 100)
font_TxtExito = pygame.font.SysFont(None, 80)
font_TxtContadores = pygame.font.SysFont(None, 32)
font_TxtPausa = pygame.font.SysFont(None, 120)
font_TxtReiniciar = pygame.font.SysFont(None, 48)
font_puntos = pygame.font.SysFont(None, 28)

#Textos de pantalla de inicio
txtTitulo = font_titulo.render("UAIBOT DELIVERY", True, COLOR_DORADO)
txtTitulo_rect = txtTitulo.get_rect(center=(PANTALLA_ANCHO // 2, 150))

txtOpcion1 = font_subtitulo.render("1 - JUGAR", True, COLOR_BLANCO)
txtOpcion1_rect = txtOpcion1.get_rect(center=(PANTALLA_ANCHO // 2, 400))

txtOpcion2 = font_subtitulo.render("2 - INSTRUCCIONES", True, COLOR_BLANCO)
txtOpcion2_rect = txtOpcion2.get_rect(center=(PANTALLA_ANCHO // 2, 460))

txtOpcion3 = font_subtitulo.render("3 - SALIR", True, COLOR_BLANCO)
txtOpcion3_rect = txtOpcion3.get_rect(center=(PANTALLA_ANCHO // 2, 520))

#Textos de pantalla de instrucciones
txtTituloInst = font_TxtGameOver.render("INSTRUCCIONES", True, COLOR_AMARILLO)
txtTituloInst_rect = txtTituloInst.get_rect(center=(PANTALLA_ANCHO // 2, 100))

instrucciones_texto = [
    "🤖 Eres UAIBOT, un robot de entregas que debe llevar un paquete",
    "",
    "🎯 OBJETIVO: Recorrer 1 kilómetro esquivando autos",
    "",
    "🕹️ CONTROLES:",
    "   • ESPACIO: Saltar (mantener presionado = salto alto)",
    "   • P: Pausar/Reanudar",
    "   • Q: Salir del juego",
    "",
    "⚡ MECÁNICAS:",
    "   • Tienes 60 segundos de energía",
    "   • Aparecen hasta 2 autos simultáneamente",
    "   • Recolecta esferas doradas para ganar puntos extra",
    "",
    "🏆 GANAR: Completa 1km sin chocar",
    "💥 PERDER: Chocar con un auto o quedarse sin energía",
    "",
    "Presiona cualquier tecla para volver al menú principal"
]

#Crear textos de instrucciones
textos_instrucciones = []
y_pos = 180
for linea in instrucciones_texto:
    if linea.strip():  #Si la línea no está vacía
        if linea.startswith("🎯") or linea.startswith("🕹️") or linea.startswith("⚡"):
            texto = font_TxtInstrucciones.render(linea, True, COLOR_CYAN)
        elif linea.startswith("🏆"):
            texto = font_TxtInstrucciones.render(linea, True, COLOR_VERDE)
        elif linea.startswith("💥"):
            texto = font_TxtInstrucciones.render(linea, True, COLOR_ROJO)
        else:
            texto = font_TxtContadores.render(linea, True, COLOR_BLANCO)
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO // 2, y_pos))
        textos_instrucciones.append((texto, texto_rect))
    y_pos += 25

#Texto de instrucciones del juego
txtInstrucciones = font_TxtInstrucciones.render("Usa la barra espaciadora para saltar", True, COLOR_BLANCO)
txtInstrucciones_desplazamiento = 10
txtInstrucciones_rect = txtInstrucciones.get_rect()
txtInstrucciones_rect.topleft = (10, 10)

fondo_rect = pygame.Rect(txtInstrucciones_rect.left - txtInstrucciones_desplazamiento,
                        txtInstrucciones_rect.top - txtInstrucciones_desplazamiento,
                        txtInstrucciones_rect.width + 2 * txtInstrucciones_desplazamiento,
                        txtInstrucciones_rect.height + 2 * txtInstrucciones_desplazamiento)

#Textos de fin de juego
txtGameOver = font_TxtGameOver.render("JUEGO TERMINADO", True, COLOR_ROJO)
txtGameOver_rect = txtGameOver.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))

txtExito = font_TxtExito.render("¡El paquete fue entregado con éxito!", True, COLOR_VERDE)
txtExito_rect = txtExito.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))

txtReiniciar = font_TxtReiniciar.render("Presiona 'R' para reiniciar", True, COLOR_BLANCO)
txtReiniciar_rect = txtReiniciar.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 + 50))

#Textos de pausa
txtPausa = font_TxtPausa.render("PAUSA", True, COLOR_AMARILLO)
txtPausa_rect = txtPausa.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))

txtReanudar = font_TxtReiniciar.render("Presiona 'P' para reanudar", True, COLOR_BLANCO)
txtReanudar_rect = txtReanudar.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2))

txtSalirPausa = font_TxtContadores.render("Presiona 'Q' para salir", True, COLOR_BLANCO)
txtSalirPausa_rect = txtSalirPausa.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 + 50))

#Texto para salir en pantalla de fin de juego
txtSalirFin = font_TxtContadores.render("Presiona 'Q' para salir", True, COLOR_BLANCO)
txtSalirFin_rect = txtSalirFin.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 + 100))

#Clase para power-ups
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 15
        self.puntos = 500
        self.activo = True
        self.tiempo_creacion = time.time()
        
    def mover(self, velocidad):
        self.x -= velocidad
        
    def dibujar(self, superficie):
        if self.activo:
            #Crear efecto de brillo
            for i in range(3):
                radio_actual = self.radio - (i * 3)
                alpha = 255 - (i * 80)
                s = pygame.Surface((radio_actual * 2, radio_actual * 2))
                s.set_alpha(alpha)
                s.fill(COLOR_DORADO)
                superficie.blit(s, (self.x - radio_actual, self.y - radio_actual))
            
            #Esfera principal
            pygame.draw.circle(superficie, COLOR_DORADO, (int(self.x), int(self.y)), self.radio)
            pygame.draw.circle(superficie, COLOR_AMARILLO, (int(self.x), int(self.y)), self.radio - 3)
            
    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

def reiniciar_juego():
    """Reinicia todas las variables del juego a sus valores iniciales"""
    global robot_x, robot_y, robot_vel_y, robot_en_piso
    global auto1_x, auto1_y, auto2_x, auto2_y, auto2_activo
    global fondo_x, energia_actual, kilometros_restantes, game_over, juego_ganado
    global tiempo_inicio, ultimo_tiempo, sonido_fin_reproducido, espacio_presionado
    global puntos, powerups, tiempo_ultimo_powerup, estado_juego
    
    #Configuración del robot/UAIBOT
    robot_x = 100
    robot_y = PISO_POS_Y - robot_tamaño
    robot_vel_y = 0
    robot_en_piso = True
    
    #Configuración de los autos
    auto1_x = PANTALLA_ANCHO
    auto1_y = PISO_POS_Y - auto_alto
    auto2_x = PANTALLA_ANCHO + PANTALLA_ANCHO // 2
    auto2_y = PISO_POS_Y - auto_alto
    auto2_activo = False
    
    #Configuración de animación de fondo
    fondo_x = 0
    
    #Configuración de energía y tiempo
    energia_actual = energia_maxima
    tiempo_inicio = time.time()
    
    #Configuración de kilómetros
    kilometros_restantes = kilometros_objetivo
    
    #Estados del juego
    game_over = False
    juego_ganado = False
    ultimo_tiempo = time.time()
    sonido_fin_reproducido = False
    espacio_presionado = False
    estado_juego = ESTADO_JUGANDO
    
    #Sistema de puntos
    puntos = 0
    powerups = []
    tiempo_ultimo_powerup = time.time()
    
    #Reiniciar música
    pygame.mixer.stop()  #Detener todos los sonidos
    if musica_cargada:
        pygame.mixer.music.play(-1)
        print("Música reiniciada")

#Configuración del robot/UAIBOT (salto más natural)
robot_tamaño = 50
robot_x = 100
robot_y = PISO_POS_Y - robot_tamaño
robot_vel_y = 0
robot_salto_normal = -12  #Reducido de -15 para salto más natural
robot_salto_alto = -18    #Reducido de -22 para salto más natural
robot_gravedad = 0.6      #Reducido de 0.8 para caída más suave
robot_en_piso = True

#Configuración de los autos
auto_ancho = 100
auto_alto = 40
auto1_x = PANTALLA_ANCHO
auto1_y = PISO_POS_Y - auto_alto
auto2_x = PANTALLA_ANCHO + PANTALLA_ANCHO // 2
auto2_y = PISO_POS_Y - auto_alto
auto2_activo = False
auto_vel_x = 7

#Configuración de animación de fondo
fondo_x = 0
fondo_vel_x = 2

#Configuración de energía y tiempo
energia_maxima = 60.0
energia_actual = energia_maxima
tiempo_inicio = time.time()

#Configuración de kilómetros
kilometros_objetivo = 1.0
kilometros_restantes = kilometros_objetivo
kilometros_por_segundo = 0.03

#Sistema de puntos y power-ups
puntos = 0
powerups = []
tiempo_ultimo_powerup = time.time()
intervalo_powerup = 8  #Segundos entre power-ups

#Estados del juego
estado_juego = ESTADO_INICIO
juegoEnEjecucion = True
game_over = False
juego_ganado = False
ultimo_tiempo = time.time()
sonido_fin_reproducido = False
espacio_presionado = False

#Bucle principal del juego
while juegoEnEjecucion:
    clock.tick(FPS)
    
    #Manejar eventos según el estado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juegoEnEjecucion = False
            
        if event.type == pygame.KEYDOWN:
            #Salir del juego con 'Q' en cualquier momento
            if event.key == pygame.K_q:
                juegoEnEjecucion = False
            
            #Estados de menú
            if estado_juego == ESTADO_INICIO:
                if event.key == pygame.K_1:
                    reiniciar_juego()
                elif event.key == pygame.K_2:
                    estado_juego = ESTADO_INSTRUCCIONES
                elif event.key == pygame.K_3:
                    juegoEnEjecucion = False
            
            elif estado_juego == ESTADO_INSTRUCCIONES:
                estado_juego = ESTADO_INICIO  #Volver al menú principal
            
            elif estado_juego == ESTADO_JUGANDO:
                #Pausa/Reanudar
                if event.key == pygame.K_p:
                    estado_juego = ESTADO_PAUSA
                    pygame.mixer.music.pause()
                    print("Juego pausado - música pausada")
                
                #Salto
                if (event.key == pygame.K_SPACE and robot_en_piso and not espacio_presionado):
                    robot_vel_y = robot_salto_normal
                    robot_en_piso = False
                    espacio_presionado = True
                    if sonido_salto:
                        sonido_salto.play()
            
            elif estado_juego == ESTADO_PAUSA:
                if event.key == pygame.K_p:
                    estado_juego = ESTADO_JUGANDO
                    pygame.mixer.music.unpause()
                    ultimo_tiempo = time.time()
                    print("Juego reanudado - música reanudada")
            
            elif estado_juego == ESTADO_FIN:
                if event.key == pygame.K_r:
                    reiniciar_juego()
                elif event.key == pygame.K_ESCAPE:
                    estado_juego = ESTADO_INICIO
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                espacio_presionado = False
    
    #Lógica según el estado del juego
    if estado_juego == ESTADO_INICIO:
        #Pantalla de inicio
        if img_inicio:
            pantalla.blit(img_inicio, (0, 0))
        else:
            pantalla.fill(COLOR_NEGRO)
            pantalla.blit(txtTitulo, txtTitulo_rect)
        
        #Overlay para las opciones
        overlay = pygame.Surface((400, 200))
        overlay.set_alpha(180)
        overlay.fill(COLOR_NEGRO)
        overlay_rect = overlay.get_rect(center=(PANTALLA_ANCHO // 2, 460))
        pantalla.blit(overlay, overlay_rect)
        
        pantalla.blit(txtOpcion1, txtOpcion1_rect)
        pantalla.blit(txtOpcion2, txtOpcion2_rect)
        pantalla.blit(txtOpcion3, txtOpcion3_rect)
    
    elif estado_juego == ESTADO_INSTRUCCIONES:
        #Pantalla de instrucciones
        pantalla.fill(COLOR_NEGRO)
        pantalla.blit(txtTituloInst, txtTituloInst_rect)
        
        for texto, rect in textos_instrucciones:
            pantalla.blit(texto, rect)
    
    elif estado_juego == ESTADO_JUGANDO:
        #Lógica principal del juego
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - ultimo_tiempo
        ultimo_tiempo = tiempo_actual
        
        #Verificar fin de juego
        if game_over or juego_ganado:
            estado_juego = ESTADO_FIN
            if not sonido_fin_reproducido:
                pygame.mixer.music.stop()
                if game_over and sonido_perder:
                    sonido_perder.play()
                elif juego_ganado and sonido_ganar:
                    sonido_ganar.play()
                sonido_fin_reproducido = True
            continue
        
        #Actualizar energía
        energia_actual -= tiempo_transcurrido
        if energia_actual <= 0:
            energia_actual = 0
            game_over = True
        
        #Actualizar kilómetros
        kilometros_restantes -= kilometros_por_segundo * tiempo_transcurrido
        if kilometros_restantes <= 0:
            kilometros_restantes = 0
            juego_ganado = True
        
        #Generar power-ups
        if tiempo_actual - tiempo_ultimo_powerup > intervalo_powerup:
            powerup_y = random.randint(PISO_POS_Y - 150, PISO_POS_Y - 50)
            powerups.append(PowerUp(PANTALLA_ANCHO, powerup_y))
            tiempo_ultimo_powerup = tiempo_actual
        
        #Actualizar power-ups
        for powerup in powerups[:]:
            powerup.mover(auto_vel_x)
            if powerup.x < -30:
                powerups.remove(powerup)
        
        #Mover autos
        auto1_x -= auto_vel_x
        auto2_x -= auto_vel_x
        
        #Auto 1: reaparición
        if auto1_x < -auto_ancho:
            auto1_x = PANTALLA_ANCHO
        
        #Auto 2: activación y reaparición
        if auto1_x <= PANTALLA_ANCHO // 2 and not auto2_activo:
            auto2_activo = True
        
        if auto2_activo and auto2_x < -auto_ancho:
            auto2_x = PANTALLA_ANCHO
        
        #Física del salto
        keys = pygame.key.get_pressed()
        if not robot_en_piso:
            if keys[pygame.K_SPACE] and robot_vel_y < 0:
                robot_vel_y += robot_gravedad * 0.4  #Gravedad reducida
            else:
                robot_vel_y += robot_gravedad
            
            robot_y += robot_vel_y
            
            if robot_y >= PISO_POS_Y - robot_tamaño:
                robot_y = PISO_POS_Y - robot_tamaño
                robot_vel_y = 0
                robot_en_piso = True
        
        #Colisiones con autos
        robot_rect = pygame.Rect(robot_x, robot_y, robot_tamaño, robot_tamaño)
        auto1_rect = pygame.Rect(auto1_x, auto1_y, auto_ancho, auto_alto)
        
        if robot_rect.colliderect(auto1_rect):
            game_over = True
        
        if auto2_activo:
            auto2_rect = pygame.Rect(auto2_x, auto2_y, auto_ancho, auto_alto)
            if robot_rect.colliderect(auto2_rect):
                game_over = True
        
        #Colisiones con power-ups
        for powerup in powerups[:]:
            if powerup.activo and robot_rect.colliderect(powerup.get_rect()):
                puntos += powerup.puntos
                powerups.remove(powerup)
                if sonido_powerup:
                    sonido_powerup.play()
        
        #Dibujar juego
        if img_fondo:
            fondo_x -= fondo_vel_x
            if fondo_x <= -PANTALLA_ANCHO:
                fondo_x = 0
            
            fondo_desplazamiento_y = -(PANTALLA_ALTO - PISO_POS_Y)
            pantalla.blit(img_fondo, (fondo_x, fondo_desplazamiento_y))
            pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, fondo_desplazamiento_y))
        else:
            pantalla.fill(COLOR_BLANCO)
        
        #Piso
        piso_altura = PANTALLA_ALTO - PISO_POS_Y
        piso_rect = pygame.Rect(0, PISO_POS_Y, PANTALLA_ANCHO, piso_altura)
        pygame.draw.rect(pantalla, COLOR_VERDE, piso_rect)
        pygame.draw.line(pantalla, COLOR_NEGRO, (0, PISO_POS_Y), (PANTALLA_ANCHO, PISO_POS_Y), 3)
        
        #Robot
        if img_uaibot:
            pantalla.blit(img_uaibot, (robot_x, robot_y))
        else:
            pygame.draw.rect(pantalla, COLOR_AZUL, robot_rect)
        
        #Autos
        if img_auto:
            pantalla.blit(img_auto, (auto1_x, auto1_y))
            if auto2_activo:
                pantalla.blit(img_auto, (auto2_x, auto2_y))
        else:
            pygame.draw.rect(pantalla, COLOR_ROJO, auto1_rect)
            if auto2_activo:
                pygame.draw.rect(pantalla, COLOR_ROJO, auto2_rect)
        
        #Power-ups
        for powerup in powerups:
            powerup.dibujar(pantalla)
        
        #Barra de energía
        barra_energia_ancho = 200
        barra_energia_alto = 30
        barra_energia_x = PANTALLA_ANCHO - barra_energia_ancho - 20
        barra_energia_y = 20
        
        pygame.draw.rect(pantalla, COLOR_BARRA_ENERGIA_FONDO, 
                        (barra_energia_x, barra_energia_y, barra_energia_ancho, barra_energia_alto))
        
        porcentaje_energia = energia_actual / energia_maxima
        ancho_energia_actual = int(barra_energia_ancho * porcentaje_energia)
        if ancho_energia_actual > 0:
            color_energia = COLOR_BARRA_ENERGIA if porcentaje_energia > 0.3 else COLOR_ROJO
            pygame.draw.rect(pantalla, color_energia, 
                            (barra_energia_x, barra_energia_y, ancho_energia_actual, barra_energia_alto))
        
        porcentaje_texto = f"{int(porcentaje_energia * 100)}%"
        txt_porcentaje = font_TxtContadores.render(porcentaje_texto, True, COLOR_BLANCO)
        txt_porcentaje_rect = txt_porcentaje.get_rect(center=(barra_energia_x + barra_energia_ancho // 2, 
                                                             barra_energia_y + barra_energia_alto // 2))
        pantalla.blit(txt_porcentaje, txt_porcentaje_rect)
        
        #Contador de kilómetros
        km_texto = f"Kilómetros restantes: {kilometros_restantes:.2f} km"
        txt_kilometros = font_TxtContadores.render(km_texto, True, COLOR_BLANCO)
        txt_km_rect = pygame.Rect(20, PANTALLA_ALTO - 100, txt_kilometros.get_width() + 20, 40)
        pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO, txt_km_rect)
        pantalla.blit(txt_kilometros, (30, PANTALLA_ALTO - 90))
        
        #Contador de puntos
        puntos_texto = f"Puntos: {puntos}"
        txt_puntos = font_puntos.render(puntos_texto, True, COLOR_DORADO)
        txt_puntos_rect = pygame.Rect(20, PANTALLA_ALTO - 140, txt_puntos.get_width() + 20, 30)
        pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO, txt_puntos_rect)
        pantalla.blit(txt_puntos, (30, PANTALLA_ALTO - 135))
        
        #Instrucciones
        pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO, fondo_rect)
        pantalla.blit(txtInstrucciones, txtInstrucciones_rect)
    
    elif estado_juego == ESTADO_PAUSA:
        #Mantener la última imagen del juego pero sin actualizaciones
        if img_fondo:
            fondo_desplazamiento_y = -(PANTALLA_ALTO - PISO_POS_Y)
            pantalla.blit(img_fondo, (fondo_x, fondo_desplazamiento_y))
            pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, fondo_desplazamiento_y))
        else:
            pantalla.fill(COLOR_BLANCO)
        
        #Elementos estáticos del juego
        piso_altura = PANTALLA_ALTO - PISO_POS_Y
        piso_rect = pygame.Rect(0, PISO_POS_Y, PANTALLA_ANCHO, piso_altura)
        pygame.draw.rect(pantalla, COLOR_VERDE, piso_rect)
        pygame.draw.line(pantalla, COLOR_NEGRO, (0, PISO_POS_Y), (PANTALLA_ANCHO, PISO_POS_Y), 3)
        
        #Personajes en posición actual
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
        
        #Power-ups en pausa
        for powerup in powerups:
            powerup.dibujar(pantalla)
        
        #Overlay de pausa
        overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        overlay.set_alpha(180)
        overlay.fill(COLOR_NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        pantalla.blit(txtPausa, txtPausa_rect)
        pantalla.blit(txtReanudar, txtReanudar_rect)
        pantalla.blit(txtSalirPausa, txtSalirPausa_rect)
    
    elif estado_juego == ESTADO_FIN:
        #Mantener la última imagen del juego
        if img_fondo:
            fondo_desplazamiento_y = -(PANTALLA_ALTO - PISO_POS_Y)
            pantalla.blit(img_fondo, (fondo_x, fondo_desplazamiento_y))
            pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, fondo_desplazamiento_y))
        else:
            pantalla.fill(COLOR_BLANCO)
        
        #Elementos del juego estáticos
        piso_altura = PANTALLA_ALTO - PISO_POS_Y
        piso_rect = pygame.Rect(0, PISO_POS_Y, PANTALLA_ANCHO, piso_altura)
        pygame.draw.rect(pantalla, COLOR_VERDE, piso_rect)
        pygame.draw.line(pantalla, COLOR_NEGRO, (0, PISO_POS_Y), (PANTALLA_ANCHO, PISO_POS_Y), 3)
        
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
        
        #Overlay de fin de juego
        overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        overlay.set_alpha(150)
        overlay.fill(COLOR_NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        #Mostrar puntuación final
        puntos_final_texto = f"Puntuación Final: {puntos}"
        txt_puntos_final = font_TxtReiniciar.render(puntos_final_texto, True, COLOR_DORADO)
        txt_puntos_final_rect = txt_puntos_final.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 20))
        
        if game_over:
            pantalla.blit(txtGameOver, txtGameOver_rect)
        elif juego_ganado:
            pantalla.blit(txtExito, txtExito_rect)
        
        pantalla.blit(txt_puntos_final, txt_puntos_final_rect)
        pantalla.blit(txtReiniciar, txtReiniciar_rect)
        pantalla.blit(txtSalirFin, txtSalirFin_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()