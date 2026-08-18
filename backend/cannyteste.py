import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Escala de cinza
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Desfoque leve (reduz ruído antes do Canny)
    desfoque = cv2.GaussianBlur(cinza, (5, 5), 0)

    # 3. Detecta bordas
    bordas = cv2.Canny(desfoque, 50, 150)

    # 4. Dilata as bordas pra fechar gaps (essencial pro Canny funcionar com findContours)
    kernel = np.ones((5, 5), np.uint8)
    bordas_dilatadas = cv2.dilate(bordas, kernel, iterations=2)

    # 5. Encontra contornos
    contornos, _ = cv2.findContours(bordas_dilatadas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos:
        area = cv2.contourArea(c)
        if area < 2000:
            continue

        x, y, largura, altura = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + largura, y + altura), (0, 255, 0), 3)

    cv2.imshow("Rastreando Tela", frame)
    cv2.imshow("Bordas (Canny + Dilate)", bordas_dilatadas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()