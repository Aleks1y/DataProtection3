import math
import sys

from PIL import Image


def set_last_bit(m, val):
    m &= ~1
    m |= int(val)
    return m


# внедряем строку
def hide(input_name, message, output_name):
    # загружаем фото
    img = Image.open(input_name)
    (width, height) = img.size
    max_size = width * height * 3

    # переводим строку в бинарный формат
    binary_message = ''.join([format(ord(i), "08b") for i in message])

    req_pixels = math.ceil(len(binary_message) / 3)

    # проверяем, что в изображении достаточно пикселей
    if len(binary_message) > max_size:
        print("Message is too long for this picture")
        exit(1)

    data_img = img.convert("RGB").getdata()
    steg_img = data_img

    # изменяем последние биты пикселей
    for i in range(req_pixels):
        h = i // height
        w = i % width
        (r, g, b) = data_img.getpixel((w, h))
        r = set_last_bit(r, binary_message[i * 3])
        if len(binary_message) > i * 3 + 1:
            g = set_last_bit(g, binary_message[i * 3 + 1])
        if len(binary_message) > i * 3 + 2:
            b = set_last_bit(b, binary_message[i * 3 + 2])
        steg_img.putpixel((w, h), (r, g, b))

    # сохраняем полученное изображение
    new_img = Image.new("RGB", (width, height))
    new_img.putdata(steg_img)
    new_img.save(output_name)


# извлекаем строку
def extract(input_name):
    img = Image.open(input_name)
    (width, height) = img.size

    data_img = img.convert("RGB").getdata()

    # извлекаем младшие биты пикселей
    m = []
    for h in range(height):
        for w in range(width):
            (r, g, b) = data_img.getpixel((w, h))
            m.append(r & 1)
            m.append(g & 1)
            m.append(b & 1)

    # переводим биты в строку
    str = ""
    for i in range(0, len(m), 8):
        byte = 0
        for j in range(0, 8):
            if j + i < len(m):
                byte = (byte << 1) + m[j + i]

        if chr(byte) == '\n':
            return str

        str += chr(byte)
    return str


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Wrong arguments")
        exit(1)

    if sys.argv[1] == "hide":
        print("Enter message")
        message = sys.stdin.readline()
        hide(sys.argv[2], message, 'steg_' + sys.argv[2])
    elif sys.argv[1] == "extract":
        print(extract(sys.argv[2]))
