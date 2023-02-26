from PIL import Image

# Größe des Bildes
width = 100
height = 100

# Größe des Schachbrettmusters
size = 2

# Erstellen eines neuen Bildes
image = Image.new('1', (width, height), color='white')

# Setzen der Pixel
for x in range(0, width, size):
    for y in range(0, height, size):
        # Wechsel zwischen Schwarz und Weiß für jedes 2x2 Feld
        if (x//size + y//size) % 2 == 0:
            color = 0  # Schwarz
        else:
            color = 1  # Weiß
        # Färben des 2x2 Feldes
        for i in range(size):
            for j in range(size):
                image.putpixel((x+i, y+j), color)

# Speichern des Bildes
image.save('bild.png')