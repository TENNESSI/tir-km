import serial
import time


commands = [
    b"\\ON\r\n",     # Включение
    b"\\START\r\n",  # Старт передачи
    b"\\RUN\r\n",    # Запуск
    b"\\FIRE\r\n",   # Режим стрельбы
    b"\\MODE 1\r\n", # Установка режима
    b"\\TRG\r\n",    # Триггер (иногда активирует датчик)
    b"\\STAT?\r\n",  # Запрос статуса
    b"\\CONFIG?\r\n",# Запрос конфигурации
    b"\\ID?\r\n",    # Запрос идентификатора
    b"\\HELP\r\n"    # Справка (если реализовано)
]


def test_commands(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print("Подключено к " + port + ". Тестирование команд...")
        
        for cmd in commands:
            ser.write(cmd)
            print("Отправка: " + cmd.decode('ascii', errors='replace').strip())
            time.sleep(0.5)
            
            # Чтение ответа
            response = ser.read_all()
            if response:
                print("Ответ (hex): " + str(response.hex()))
                print("Ответ (raw): " + str(response))
                print("-" * 40)
                
        ser.close()
    except Exception as e:
        print("Ошибка: " + str(e))

# Укажите ваш COM-порт
test_commands("COM1", 115200)