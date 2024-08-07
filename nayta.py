import os
from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Ohjelma joka näyttää kansion kuvat aakkosjärjestyksessä
# näppäimet näet funktios bind_keys
# Käyttämiseksi asenna jos ei ole
# pip install Pillow
#
# käynnistä oikeassa hakemistossa
#   python nayta.py
#
# Vesa Lappalainen 5.8.2024


def bind_keys():
    root.bind('<Left>', lambda e: show_next_image(-1))  # Vasen nuoli edelliseen
    root.bind('<Right>', lambda e: show_next_image(1))  # Oikea nuoli seuraavaan
    root.bind('<Return>', lambda e: show_next_image(1))  # Enter seuraavaan
    root.bind('<Prior>', lambda e: show_next_image(10))  # PgUp 10 eteen
    root.bind('<Next>', lambda e: show_next_image(-10))  # PgDown 10 taakse
    root.bind('<Home>', lambda e: show_next_image(1000000))  # Home 1- kuvaan
    root.bind('<End>', lambda e: show_next_image(-1000000))  # End viimeiseen kuvaan
    root.bind('p', pause_showing)  # p = Pause
    root.bind('r', resume_showing)  # r = Resume (jatka)
    root.bind('q', stop_program)  # q = lopeta
    root.bind('<Escape>', stop_program)  # ESC = lopeta
    root.bind('<space>', toggle_pause_resume)  # välilyönti = pysäytä/jatka
    root.bind('+', lambda e: change_time(1))  # + = lisää kuvan näyttöaikaa
    root.bind('-', lambda e: change_time(-1))  # - = vähennä kuvan näyttöaikaa


# Fontin määrittäminen (käytetään Arial-fonttia, joka löytyy Windowsista)
font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Arial-fontin polku Windowsissa
font_size = 30

image_index = 0
image_shown = False

# Globaali muuttuja aikakatkaisun ID:lle
after_id = ""
paused = False
image_delay = 5


# Funktio tiedostopäätteen poistamiseen
def remove_file_extension(filename):
    return os.path.splitext(os.path.basename(filename))[0]


# Funktio kuvan näyttämiseen ja tiedostonimen piirtämiseen
def show_image_with_filename(image_path, display_time):
    global image_shown, after_id, paused
    image_shown = True
    try:
        # Avataan kuva
        image = Image.open(image_path)

        font = ImageFont.truetype(font_path, font_size)

        # Luodaan uusi kuva, johon piirretään teksti ja alkuperäinen kuva
        new_image = Image.new('RGB', (root.winfo_width(), root.winfo_height()), 'black')

        # Piirretään tiedostonimi kuvan yläreunaan
        draw = ImageDraw.Draw(new_image)
        text = remove_file_extension(image_path).replace('_', ' ')  # Poistetaan tiedostopääte
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((root.winfo_width() - text_width) / 2, 10)  # Keskitetään teksti yläreunaan
        draw.text(text_position, text, fill="yellow", font=font)

        # Skaalataan alkuperäinen kuva
        img_aspect = image.width / image.height
        screen_aspect = root.winfo_width() / (root.winfo_height() - text_height)  # Varaamme tilaa tekstille

        if img_aspect > screen_aspect:
            # Jos kuva on leveämpi kuin näyttö
            scale_factor = (root.winfo_width() / image.width)
        else:
            # Jos kuva on korkeampi kuin näyttö
            scale_factor = ((root.winfo_height() - text_height) / image.height)

        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        image = image.resize(new_size, Image.LANCZOS)

        # Keskitetään kuva mustalle taustalle

        x_offset = (root.winfo_width() - new_size[0]) // 2
        y_offset = (root.winfo_height() - new_size[1] - text_height) // 2 + text_height
        new_image.paste(image, (x_offset, y_offset))

        # Tekstin taustan väri (musta)
        padding = 10
        background_width = text_width + 2 * padding
        background_height = text_height + padding

        # Taustasuorakulmion sijainti
        background_x = (root.winfo_width() - background_width) / 2
        background_y = 10  # Tekstin yläreuna

        # Piirretään taustasuorakulmio tekstin taakse
        draw.rectangle(
            (background_x, background_y, background_x + background_width, background_y + background_height),
            fill='black'
        )

        draw.text(text_position, text, fill="yellow", font=font)

        # Piirretään punainen pallo, jos näyttö on pysäytetty
        if paused:
            radius = 20
            ball_x = root.winfo_width() - 50
            ball_y = 50
            draw.ellipse([ball_x - radius, ball_y - radius, ball_x + radius, ball_y + radius], fill='red')

        # Muutetaan `Pillow`-kuva `PhotoImage`-objektiksi
        img_tk = ImageTk.PhotoImage(new_image)
        label.config(image=img_tk)
        label.image = img_tk  # Säilytetään referenssi kuvalle

        # Odotetaan määrätty aika
        if after_id:
            root.after_cancel(after_id)  # Peruuta aikakatkaisin, jos se on jo määritelty
        if not paused:
            after_id = root.after(int(display_time * 1000), lambda: show_next_image())
            # Muutetaan sekunnit millisekunneiksi

    except Exception as e:
        print(f"Error showing image {image_path}: {e}")


def show_current_image():
    global image_index, image_delay

    while True:
        if image_index < 0:
            image_index = len(image_files) - 1
        if image_index >= len(image_files):
            image_index = 0

        image_file = image_files[image_index]
        name = os.path.splitext(os.path.basename(image_file))[0]
        if not image_file.strip() or image_file.startswith(';'):
            image_index += 1
            continue
        break

    display_time = 1 if len(name) == 4 else image_delay  # jos pelkkä vuosiluku
    show_image_with_filename(image_file, display_time)


def show_next_image(step=1):
    global image_index
    image_index += step
    show_current_image()


def pause_showing(_):
    global image_shown, after_id, paused
    if image_shown:
        if after_id:
            root.after_cancel(after_id)  # Peruutetaan aikakatkaisin
        image_shown = False
        paused = True
        show_current_image()


def toggle_pause_resume(_):
    if paused:
        resume_showing(_)
    else:
        pause_showing(_)


def stop_program(_):
    root.destroy()  # Sulkee koko ohjelman


def resume_showing(_):
    global paused
    paused = False
    show_current_image()


def change_time(d):
    global image_delay
    image_delay += d
    if image_delay < 1:
        image_delay = 1


# Tkinter-ikkunan määrittäminen
root = Tk()
root.title("Kuvien näyttäminen")
root.attributes('-fullscreen', True)  # Asetetaan ikkuna täyttämään koko näyttö

label = Label(root)
label.pack(fill='both', expand=True)

# Luetaan kaikki kuvat hakemistosta 'muisto'
image_folder = '.'
image_files = \
    sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png'))])

bind_keys()

# Näytetään ensimmäinen kuva
root.update_idletasks()  # Päivitetään ikkunan tehtävät (muuten eka ei näy)
show_current_image()

root.mainloop()

print("Kuvien näyttäminen valmis!")
