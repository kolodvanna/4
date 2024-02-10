import RPi.GPIO as GPIO
import time
import speech_recognition as sr

# Устанавливаем режим нумерации пинов
GPIO.setmode(GPIO.BCM)

# Определяем пины для подключения к драйверу A4988
step_pin1 = 17
dir_pin1 = 26
enable_pin1 = 7
ms1_pin1 = 4
ms2_pin1 = 12
ms3_pin1 = 25

step_pin2 = 22
dir_pin2 = 11
enable_pin2 = 8
ms1_pin2 = 19
ms2_pin2 = 13
ms3_pin2 = 5
# Устанавливаем пины как выходы
GPIO.setup(step_pin1, GPIO.OUT)
GPIO.setup(dir_pin1, GPIO.OUT)
GPIO.setup(enable_pin1, GPIO.OUT)
GPIO.setup(ms1_pin1, GPIO.OUT)
GPIO.setup(ms2_pin1, GPIO.OUT)
GPIO.setup(ms3_pin1, GPIO.OUT)

GPIO.setup(step_pin2, GPIO.OUT)
GPIO.setup(dir_pin2, GPIO.OUT)
GPIO.setup(enable_pin2, GPIO.OUT)
GPIO.setup(ms1_pin2, GPIO.OUT)
GPIO.setup(ms2_pin2, GPIO.OUT)
GPIO.setup(ms3_pin2, GPIO.OUT)

# Устанавливаем направление вращения (CW - по часовой стрелке, CCW - против часовой стрелки)
def set_direction1(direction):
    if direction == "CW":
        GPIO.output(dir_pin1, GPIO.HIGH)
    elif direction == "CCW":
        GPIO.output(dir_pin1, GPIO.LOW)

def set_direction2(direction):
    if direction == "CW":
        GPIO.output(dir_pin2, GPIO.HIGH)
    elif direction == "CCW":
        GPIO.output(dir_pin2, GPIO.LOW)
# Функция для установки режима микрошагов
def set_microstep_mode1(ms1, ms2, ms3):
    GPIO.output(ms1_pin1, ms1)
    GPIO.output(ms2_pin1, ms2)
    GPIO.output(ms3_pin1, ms3)
    
def set_microstep_mode2(ms1, ms2, ms3):
    GPIO.output(ms1_pin2, ms1)
    GPIO.output(ms2_pin2, ms2)
    GPIO.output(ms3_pin2, ms3)
    

button_pin = 6  # Измените на фактический пин GPIO, к которому подключена кнопка

# Настройте пин для кнопки
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Функция, которая будет выполнена при нажатии кнопки
def button_callback(channel):
    print("Кнопка нажата")
    speech_to_braille2()
# Добавьте слушатель событий для  нажатия кнопки
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Функция для вращения шагового двигателя на заданное количество шагов
def rotate_motor1(steps, direction):
    set_direction1(direction)
    for i in range(steps):
        GPIO.output(step_pin1, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(step_pin1, GPIO.LOW)
        time.sleep(0.005)
        
def rotate_motor2(steps, direction):
    set_direction2(direction)
    for i in range(steps):
        GPIO.output(step_pin2, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(step_pin2, GPIO.LOW)
        time.sleep(0.005)

# Устанавливаем режим микрошагов (например, 1/16 микрошага)
set_microstep_mode1(GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
set_microstep_mode2(GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
# Определяем пины для сервоприводов
servo_pins = [16, 20, 21, 18, 23, 24]


# Устанавливаем пины для сервоприводов как выходы
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)

# Словарь соответствия букв, цифр и знаков к символам Брайля для русского алфавита
braille_dict = {
    'а': '⠁',
    'б': '⠃',
    'в': '⠺',
    'г': '⠛',
    'д': '⠙',
    'е': '⠑',
    'ё': '⠡',
    'ж': '⠚',
    'з': '⠵',
    'и': '⠊',
    'й': '⠯',
    'к': '⠅',
    'л': '⠇',
    'м': '⠍',
    'н': '⠝',
    'о': '⠕',
    'п': '⠏',
    'р': '⠗',
    'с': '⠎',
    'т': '⠞',
    'у': '⠥',
    'ф': '⠋',
    'х': '⠓',
    'ц': '⠉',
    'ч': '⠟',
    'ш': '⠱',
    'щ': '⠭',
    'ъ': '⠷',
    'ы': '⠮',
    'ь': '⠾',
    'э': '⠪',
    'ю': '⠳',
    'я': '⠫',
    '0': '⠼⠚',
    '1': '⠼⠁',
    '2': '⠼⠃',
    '3': '⠼⠉',
    '4': '⠼⠙',
    '5': '⠼⠑',
    '6': '⠼⠋',
    '7': '⠼⠛',
    '8': '⠼⠓',
    '9': '⠼⠊',
    ',': '⠂',
    '.': '⠲',
    '!': '⠖',
    '?': '⠢',
    ';': '⠰',
    ':': '⠒',
    '-': '⠤',
    '(': '⠣',
    ')': '⠜',
    '"': '⠐',
    "'": '⠄',
    '/': '⠌',
    '@': '⠩',
    '+': '⠬',
    '=': '⠿',
    '#': '⠼', 
}
# Словарь для преобразования символов Брайля в биты
braille_doc = {
    '⠁': [0, 0, 0, 3, 0, 0],
    '⠃': [0, 0, 0, 3, 4, 0],
    '⠺': [2, 2, 6, 0, 4, 0],
    '⠛': [2, 2, 0, 3, 4, 0],
    '⠙': [2, 2, 0, 3, 0, 0],
    '⠑': [0, 2, 0, 3, 0, 0],
    '⠡': [0, 0, 6, 3, 0, 0],	
    '⠚': [2, 2, 0, 0, 4, 0],
    '⠵': [0, 2, 6, 3, 0, 5],
    '⠊': [2, 0, 0, 0, 4, 0],
    '⠯': [2, 0, 6, 3, 4, 5],
    '⠅': [0, 0, 0, 3, 0, 5],
    '⠇': [0, 0, 0, 3, 4, 5],
    '⠍': [2, 0, 0, 3, 0, 5],
    '⠝': [2, 2, 0, 3, 0, 5],
    '⠕': [0, 2, 0, 3, 0, 5],
    '⠏': [2, 0, 0, 3, 4, 5],
    '⠗': [0, 2, 0, 3, 4, 5],
    '⠎': [2, 0, 0, 0, 4, 5],
    '⠞': [2, 2, 0, 0, 4, 5],
    '⠥': [0, 0, 6, 3, 0, 5],
    '⠋': [2, 2, 0, 3, 0, 0],
    '⠓': [2, 0, 0, 3, 4, 0],
    '⠉': [2, 0, 0, 3, 0, 0],
    '⠟': [2, 2, 0, 3, 4, 5],
    '⠱': [0, 2, 6, 3, 0, 0],
    '⠭': [2, 0, 6, 3, 0, 5],
    '⠷': [0, 2, 6, 3, 4, 5],
    '⠮': [2, 0, 6, 0, 4, 5],
    '⠾': [2, 2, 6, 0, 4, 5],
    '⠪': [2, 0, 6, 0, 4, 0],
    '⠳': [0, 2, 6, 3, 4, 0],
    '⠫': [2, 0, 6, 3, 4, 0],
    '0': [2, 2, 6, 3, 4, 5],
    '1': [2, 0, 0, 0, 0, 5],
    '2': [2, 0, 0, 0, 4, 5],
    '3': [2, 0, 0, 3, 0, 5],
    '4': [2, 0, 0, 3, 4, 0],
    '5': [2, 0, 6, 0, 0, 5],
    '6': [2, 0, 6, 0, 4, 0],
    '7': [2, 0, 6, 3, 0, 0],
    '8': [2, 2, 0, 0, 4, 0],
    '9': [2, 2, 0, 0, 0, 5],
    ',': [0, 0, 6, 0, 0, 0],
    '.': [0, 2, 6, 0, 4, 5],
    '!': [2, 0, 0, 0, 4, 0],
    '?': [2, 0, 0, 3, 0, 0],
    ';': [0, 0, 6, 3, 0, 5],
    ':': [0, 0, 6, 0, 4, 0],
    '-': [2, 0, 6, 0, 4, 5],
    '(': [0, 0, 6, 3, 4, 0],
    ')': [2, 0, 6, 3, 0, 0],
    '"': [0, 0, 6, 0, 0, 0],
    "'": [2, 2, 6, 0, 0, 0],
    '/': [2, 0, 6, 3, 0, 5],
    '@': [0, 1, 0, 0, 4, 5],
    '+': [2, 2, 0, 0, 4, 5],
    '=': [2, 2, 6, 3, 4, 0],
    '#': [2, 0, 6, 0, 4, 5],
}

# Функция для преобразования текста в шрифт Брайля
def text_to_braille(text):
    result = ''
    for char in text.lower():
        if char in braille_dict:
            result += braille_dict[char]
        else:
            result += ' '  # Возможно, стоит заменить на другой символ или удалить, чтобы не было пробелов
    return result

def control_servos(braille_symbol):
    num_servos = len(braille_symbol)
    pwm_list = []

    # Поворачиваем все сервоприводы на 30 градусов
    for i in range(num_servos):
        pin = servo_pins[i]
        bit_value = braille_symbol[i]


            
        if bit_value == 6:
            p = GPIO.PWM(pin, 50)
            p.start(3.5)  # Начальная позиция 0 градусов
            p.ChangeDutyCycle(3.8)  # Поворачиваем на 30 градусов
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)  # Возвращаем в начальное положение
            time.sleep(0.5)
            p.stop()
            
        if bit_value == 3:
            p = GPIO.PWM(pin, 50)
            p.start(2.5)  # Начальная позиция 0 градусов
            p.ChangeDutyCycle(3)  # Поворачиваем на 30 градусов
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)  # Возвращаем в начальное положение
            time.sleep(0.5)
            p.stop()
        
        if bit_value == 5:
            p = GPIO.PWM(pin, 50)
            p.start(2.5)  # Начальная позиция 0 градусов
            p.ChangeDutyCycle(3.8)  # Поворачиваем на 30 градусов
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)  # Возвращаем в начальное положение
            time.sleep(0.5)
            p.stop()
            
        if bit_value == 2:
            p = GPIO.PWM(pin, 50)
            p.start(3.5)  # Начальная позиция 0 градусов
            p.ChangeDutyCycle(1)  # Поворачиваем на 30 градусов
            time.sleep(0.5)
            p.ChangeDutyCycle(3.5)  # Возвращаем в начальное положение
            time.sleep(0.5)
            p.stop()
        
        if bit_value == 4:
            p = GPIO.PWM(pin, 50)
            p.start(2.5)  # Начальная позиция 0 градусов
            p.ChangeDutyCycle(3.8)  # Поворачиваем на 30 градусов
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)  # Возвращаем в начальное положение
            time.sleep(0.5)
            p.stop()

    
def speech_to_braille2():
        braille_text = text_to_braille(text)
        
        if braille_text:
            total_steps = 0
            for symbol in braille_text:
                if symbol == ' ':
                    rotate_motor1(600, "CCW")
                    total_steps += 600
                    time.sleep(1)
                else:
                    control_servos(braille_doc[symbol])
                    time.sleep(1)
                    rotate_motor1(300, "CCW")
                    total_steps += 300
                    time.sleep(1)

                # Проверяем, достигли ли мы общего количества шагов 29 * 200
                if total_steps >= 25 * 300:
                    # Сбрасываем общее количество шагов
                    total_steps = 0

                    # Поворачиваем второй мотор на 3.8 мм
                    rotate_motor1(10000, "CW")   # Повернуть против часовой стрелки для возвращения в начальное положение
                    time.sleep(1)  # Настройте задержку в соответствии с характеристиками вашего мотора
                    rotate_motor2(1500, "CCW")  # Повернуть по часовой стрелке для перемещения второго мотора
                    time.sleep(1)  # Настройте задержку в соответствии с характеристиками вашего мотора
    
if __name__ == "__main__":
    try:
        print("Нажмите кнопку, чтобы начать преобразование речи в шрифт Брайля...")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Выход...")

    finally:
        # Освободите GPIO при выходе
        GPIO.cleanup()

