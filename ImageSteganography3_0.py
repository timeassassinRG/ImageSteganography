import cv2
import numpy as np

def messageToBinary(message):
  if type(message) == str:                                        # se il messaggio è una stringa
    return ''.join([ format(ord(i), "08b") for i in message ])    # converto il messaggio in binario
  elif type(message) == bytes or type(message) == np.ndarray:     # se il messaggio è una lista di bytes o una numpy array
    return [ format(i, "08b") for i in message ]                  
  elif type(message) == int or type(message) == np.uint8:         # se il messaggio è un intero o una numpy uint8
    return format(message, "08b")                                 # restituisce una stringa di 8 bit

def hideText(img, secretText):
    input_image = img                                             # backup immagine originale
  
    n_bytes = img.shape[0] * img.shape[1] * 3 // 8                # (3 byte per pixel) diviso per 8 perchè ci sono 8 bit per byte
    print("Dimensione massima testo da nascondere:", n_bytes)   

    if len(secretText) > n_bytes:
        print("errore testo troppo lungo")
        return

    secretText += "###"                                            # aggiungo una stringa di fine messaggio (un delimitatore)
    secretText = messageToBinary(secretText)      # converto il messaggio in binario
    index = 0                                     # indice del messaggio 
    dataLen = len(secretText)                     # lunghezza del messaggio da nascondere
    for values in img:                          
        for pixel in values:                    # per ogni valore del pixel (r, g, b) (0-255, 0-255, 0-255)
            r, g, b = messageToBinary(pixel)    # converto il pixel(numpy array) in binario
            if index < dataLen:
                pixel[0] = int(r[:-1] + secretText[index], 2) # eseguo un somma in base binaria tra il bit meno significativo di ogni colore e i bit del messaggio 
                index += 1
            if index < dataLen:
                pixel[1] = int(g[:-1] + secretText[index], 2)
                index += 1
            if index < dataLen:
                pixel[2] = int(b[:-1] + secretText[index], 2)
                index += 1
            if index >= dataLen:
                break
    cv2.imshow("immagine originale", input_image)                
    cv2.imshow("immagine contentente testo", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img

def showData(image):
  binary_data = ""  # stringa di binario
  for values in image:
      for pixel in values:
          r, g, b = messageToBinary(pixel) 
          binary_data += r[-1] # prendo il bit meno significativo di ogni colore
          binary_data += g[-1] 
          binary_data += b[-1] 
  
  all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]  
  
  decoded_data = ""
  for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-3:] == "###":
          break
  return decoded_data[:-3]



img = cv2.imread('prova.jpg')   #immagine di default
while True:
  s = input("Steganografia: \n1. scegli immagine da usare \n2. visualizza immagine \n3. nascondi testo \n4. visualizza testo \n5. Exit \n")
  a = int(s)
  if a == 1:
    img = cv2.imread(input("Immagine da usare: "))
  elif a == 2:
    cv2.imshow("Immagine", img)
    cv2.waitKey(0)
  elif a == 3:
    hideText(img, input("Testo da nascondere: "))
  elif a == 4:
    print()
    print("Testo:", showData(img))
    print()
  elif a == 5:
    break
  else:
    print("errore")
    break
cv2.destroyAllWindows()