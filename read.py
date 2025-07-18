import serial
from serial.tools import list_ports
import time

# Настройки порта (измените под вашу мишень)
PORT = "COM3"          # Проверьте в Диспетчере устройств
BAUDRATE = 115200      # Попробуйте другие скорости, если не работает
TIMEOUT = 1            # Таймаут в секундах

def monitor_target():
    try:
        # Подключаемся к порту
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        print(f"Подключено к {PORT} на скорости {BAUDRATE} бод")

        # Отправка тестовой команды (если требуется)
        ser.write(b'\n')  # Раскомментируйте, если мишень требует активации

        while True:
            # Вариант 1: Чтение строки (если мишень отправляет текст)
            data_str = ser.readline().decode('ascii', errors='ignore').strip()
            if data_str:
                print("Строка:", data_str)

            # Вариант 2: Чтение байт (если данные бинарные)
            data_bytes = ser.read(4)  # Читаем 4 байта (подберите размер)
            if data_bytes:
                print("Байты:", data_bytes)

            # Задержка для уменьшения нагрузки на CPU
            time.sleep(0.1)

    except serial.SerialException as e:
        print("Ошибка порта:", e)
    except KeyboardInterrupt:
        print("Остановлено пользователем")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Порт закрыт")

if __name__ == "__main__":
    # Проверка доступных портов
    print("Доступные порты:")
    for port in list_ports.comports():
        print(f"  {port.device} - {port.description}")

    monitor_target()