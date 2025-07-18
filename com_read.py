import serial

ser = serial.Serial('COM1', 115200, timeout=1)  # Укажите ваш COM-порт и скорость

while True:
	try:
		data = ser.readline()
		if data:
			print('выстрел')
			print(data)
			# x, y = map(int, data.split(','))  # Разделяем X и Y
			# print(f"Попадание: X={x}, Y={y}")
	except Exception as _e:
		print("ошибка чтения порта: " + _e)
	# data = ser.readline().decode().strip()  # Читаем строку (например, "120,240")