import cv2
import pytesseract
from deep_translator import GoogleTranslator

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cap = cv2.VideoCapture(0)

print("Pressione ESPAÇO para tirar foto")
print("Depois: ENTER = confirmar | ESPAÇO = tirar outra | ESC = sair")

while True:
    # loop da camera
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro na câmera")
            break

        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            exit()

        elif key == 32:  # ESPAÇO
            imagem = frame
            break

    # pré-processamento
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    #  conferência
    cv2.imshow("Verificação", gray)

    print("\nENTER = usar imagem | ESPAÇO = tirar outra")

    #  loop de decisão
    while True:
        key = cv2.waitKey(0)

        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            exit()

        elif key == 32:  # ESPAÇO → refazer
            cv2.destroyWindow("Verificação")
            break

        elif key == 13:  # ENTER → confirmar
            cv2.destroyWindow("Verificação")

            # OCR
            texto = pytesseract.image_to_string(gray, lang='eng', config='--psm 6')

            print("\nTexto detectado:")
            print(repr(texto))

            if texto.strip():
                traducao = GoogleTranslator(source='auto', target='pt').translate(texto)

                print("\nTradução:")
                print(traducao)
            else:
                print("\n Nenhum texto detectado.")

            print("\nPressione qualquer tecla para continuar...")
            cv2.waitKey(0)
            break
