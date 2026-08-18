import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Converte para escala de cinza, pq para Threshold ou Canny precisa vir em escala de cinza
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. Desfoque leve para espalhar os pixels de luz da tela
    desfoque = cv2.GaussianBlur(cinza, (11, 11), 0)
    
    # 3. MÁGICA PARA O ESCURO: Tudo que for muito brilhante (acima de 200) vira BRANCO Puro.
    # O resto do quarto escuro vira PRETO absoluto.
    _, thresh = cv2.threshold(desfoque, 200, 255, cv2.THRESH_BINARY) #( src-imagem, thrseh - o 'corte' que separa pixels escuros do claros (sensibilidade), maxVal - Valor aos pixels que passam no teste do thresh, type - tipo de limiarização a ser aplicada (BINÁRIA, BINÁRIA INV))

    bordas = cv2.Canny(desfoque, threshold1=50, threshold2=150)

    # 4. Encontra o contorno desse borrão de luz branco da tela
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #thrseh
    
    for c in contornos:
        # Ignora pequenos reflexos ou luzes de LED ao fundo
        if cv2.contourArea(c) < 2000:
            continue
            
        # Cria a caixa ao redor da luz da tela
        x, y, largura, altura = cv2.boundingRect(c)
        
        # Desenha o retângulo verde ao redor da tela acesa no frame colorido
        cv2.rectangle(frame, (x, y), (x + largura, y + altura), (0, 255, 0), 3)

    # Exibe a câmera normal
    cv2.imshow("Rastreando Tela no Escuro", frame)
    # Linha opcional abaixo para você ver o que o OpenCV está isolando:
    cv2.imshow("Apenas a Luz da Tela", bordas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
