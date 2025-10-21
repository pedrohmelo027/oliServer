import cv2 #Importa e biblioteca OpenCV (cores) 
import numpy as np #Importa a biblioteca NumPy (matemática)

cap = cv2.VideoCapture(0) #Inicia a captura de vídeo padrão
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #Define a largura do frame para 1280 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #Define a altura do frame para 720 pixels

def desenhar_estrela(frame, cx, cy, raio=20, cor=(156, 204, 102), espessura=2): #Função que desenha uma estrela verde claro
    pontos = []
    for i in range(10):
        angulo = i * (2 * np.pi / 10)
        r = raio if i % 2 == 0 else raio // 2
        x = int(cx + r * np.cos(angulo - np.pi/2))
        y = int(cy + r * np.sin(angulo - np.pi/2))
        pontos.append((x, y))
    pontos = np.array(pontos, np.int32)
    cv2.polylines(frame, [pontos], isClosed=True, color=cor, thickness=espessura)

while True:
    _, frame = cap.read() #Lê um frame da câmera
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Converte o frame do espaço de cores BGR para HSV (Hue, Saturation, Value)
    altura, largura, _ = frame.shape #Obtém a altura e a largura do frame.
    cx = int(largura / 2) #Calcula a coordenada x do centro do frame
    cy = int(altura / 2) #Calcula a coordenada y do centro do frame
    centro_pixel = hsv_frame[cy, cx] #Obtém as componentes HSV do pixel central
    h, s, v = int(centro_pixel[0]), int(centro_pixel[1]), int(centro_pixel[2]) #Extrai os valores HSV do pixel central

    cor = "Indefinida" #Inicializa a variável cor com o valor padrão "Indefinida"
    if v < 40: #Verifica se os valores HSV estão dentro do intervalo para as cores disponíveis
        cor = "PRETO" #Definição das cores
        
    elif s < 30 and v > 180:
        cor = "BRANCO"
    elif s < 60 and 40 < v < 180:
        cor = "CINZA"
    elif 5 < h < 22 and s > 100 and v < 150:
        cor = "MARROM"
        
    elif h < 5 or h >= 170:
        cor = "VERMELHO"
    elif h < 22:
        cor = "LARANJA"
    elif h < 33:
        cor = "AMARELO"
    elif h < 78 and v < 100:
        cor = "VERDE ESCURO"
    elif h < 78:
        cor = "VERDE"
    elif h < 102:
        cor = "AZUL"
    elif h < 131:
        cor = "AZUL ESCURO"
    elif h < 145:
        cor = "ROXO"
    elif h < 168 and v < 160:
        cor = "ROSA ESCURO"
    elif h < 168:
        cor = "ROSA"
    else:
        cor = "VERMELHO"

    centro_pixel_bgr = frame[cy, cx] #Obtém as componentes BGR do pixel central no frame original
    b, g, r = int(centro_pixel_bgr[0]), int(centro_pixel_bgr[1]), int(centro_pixel_bgr[2]) #Extrai os valores BGR do pixel central

    cv2.putText(frame, cor, (10, 70), 0, 1.5, (b, g, r), 2) #Desenha o texto da cor no frame usando a cor detectada
    desenhar_estrela(frame, cx, cy)  #Desenha a estrela no centro
    cv2.imshow("Frame", frame) #Exibe o frame em uma janela denominada "Frame"
    chave = cv2.waitKey(1) #Espera por 1 milissegundo por uma tecla ser pressionada
    if chave == 27: #Verifica se a tecla pressionada foi Esc (código ASCII 27)
        break #Sai do loop se a tecla Esc foi pressionada

cap.release() #Libera os recursos da câmera 
cv2.destroyAllWindows() #Fecha todas as janelas abertas pelo OpenCV
