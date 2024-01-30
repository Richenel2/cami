import chardet

def detect_and_decode(text):
    # Détecter l'encodage
    result = chardet.detect(text.encode())



    return result