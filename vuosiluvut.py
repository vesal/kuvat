from PIL import Image, ImageDraw, ImageFont

# Fontin määrittäminen (muista vaihtaa polku fonttitiedostoon, joka tukee suomen kieltä ja on saatavilla koneellasi)
font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Muuta tämä sopivaksi poluksi
font_size = 300

# Luodaan kuvat vuosille 1935-2024
for year in range(1935, 2024+1):
    # Luodaan uusi kuva (valkoinen pohja, koko 800x800 pikseliä)
    image = Image.new("RGB", (800, 800), "black")
    draw = ImageDraw.Draw(image)

    # Fontti
    font = ImageFont.truetype(font_path, font_size)

    # Vuosiluku tekstinä
    text = str(year)

    # Tekstin koko ja sijainti
    text_width, text_height = draw.textsize(text, font=font)
    position = ((800 - text_width) / 2, (800 - text_height) / 2)

    # Piirretään teksti kuvaan
    draw.text(position, text, fill="yellow", font=font)

    # Tallennetaan kuva
    image.save(f"{year}.png")

print("Kuvien luominen valmis!")
