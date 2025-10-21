import cv2
import numpy as np
from sklearn.cluster import KMeans

# ----------------------------------------------------------------------
# 1. FUNÇÃO DE CLASSIFICAÇÃO DE CORES (A Sua Função Original)
# É IMPORTANTE que esta função esteja disponível para a análise
# ----------------------------------------------------------------------

def get_color_name(h, s, v):
    """Classifica um único pixel HSV em um nome de cor."""
    cor = "Indefinida"
    if v < 40:
        cor = "PRETO"
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
    return cor

# ----------------------------------------------------------------------
# 2. FUNÇÃO DE ANÁLISE DE COR PREDOMINANTE (Implementação Solicitada)
# ----------------------------------------------------------------------

def analyze_dominant_color(image_array, target_color_name):
    """
    Analisa a cor predominante em uma imagem usando K-Means Clustering 
    e verifica se ela corresponde à cor alvo.

    Args:
        image_array (np.array): A imagem BGR como um array NumPy.
        target_color_name (str): O nome da cor esperada (ex: 'VERMELHO').

    Returns:
        bool: True se a cor predominante corresponder à cor alvo, False caso contrário.
    """
    # 1. Pré-processamento e K-Means
    
    # Redimensiona para acelerar o K-Means (100x100 pixels é suficiente)
    resized_img = cv2.resize(image_array, (100, 100), interpolation=cv2.INTER_AREA)
    
    # Converte BGR para HSV e remodela o array de pixels para o K-Means
    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
    # Transforma a imagem 3D (H, L, A) em uma lista 2D de pixels (Pixel, Canal_HSV)
    pixels = hsv_img.reshape((-1, 3)) 
    
    # Aplica o K-Means para encontrar as N cores dominantes (clusters)
    # N_CLUSTERS = 5 é um bom ponto de partida para pegar as cores principais.
    N_CLUSTERS = 5
    kmeans = KMeans(n_clusters=N_CLUSTERS, n_init='auto', random_state=42)
    kmeans.fit(pixels)
    
    # 2. Encontrando a Cor Mais Dominante
    
    # Os 'labels' mostram a qual cluster cada pixel pertence.
    # Os 'cluster_centers' são os valores HSV médios de cada cor (cluster).
    
    # Encontra a porcentagem de pixels em cada cluster
    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    # Pega o índice do cluster que tem mais pixels (o mais dominante)
    dominant_cluster_index = unique[np.argmax(counts)]
    
    # Pega os valores HSV médios do cluster dominante
    hsv_dominant = kmeans.cluster_centers_[dominant_cluster_index]
    
    # Extrai os valores H, S, V e garante que sejam inteiros
    h = int(hsv_dominant[0])
    s = int(hsv_dominant[1])
    v = int(hsv_dominant[2])

    # 3. Classificação e Comparação
    
    # Classifica a cor dominante usando sua função original
    detected_color = get_color_name(h, s, v)
    
    # Compara a cor detectada com a cor alvo (convertendo para maiúsculas)
    return detected_color == target_color_name.upper()


# ----------------------------------------------------------------------
# EXEMPLO DE USO (MOCK - Simula a imagem vinda da API)
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Cria uma imagem de teste (500x500, metade azul, metade vermelha)
    test_img = np.zeros((500, 500, 3), dtype=np.uint8)
    
    # Define a metade superior (0-250) como VERMELHO (BGR: 0, 0, 255)
    test_img[0:250, :] = (0, 0, 255) 
    
    # Define a metade inferior (250-500) como AZUL (BGR: 255, 0, 0)
    test_img[250:500, :] = (255, 0, 0)
    
    # Se a cor alvo for VERMELHO, deve ser True (ou Azul, dependendo do K-Means)
    target = "VERMELHO"
    result = analyze_dominant_color(test_img, target)
    print(f"Cor alvo: {target}, Resultado: {result}")
    
    # Se a cor alvo for AZUL, deve ser True
    target = "AZUL"
    result = analyze_dominant_color(test_img, target)
    print(f"Cor alvo: {target}, Resultado: {result}")
    
    # Se a cor alvo for VERDE, deve ser False
    target = "VERDE"
    result = analyze_dominant_color(test_img, target)
    print(f"Cor alvo: {target}, Resultado: {result}")

    # # (Opcional: Descomente para visualizar a imagem de teste)
    # cv2.imshow("Test Image", test_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()