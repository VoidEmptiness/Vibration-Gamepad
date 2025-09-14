import ctypes
import time
import keyboard  # pip install keyboard

# Загружаем XInput
try:
    xinput = ctypes.windll.xinput1_4  # Windows 10/11
except:
    xinput = ctypes.windll.xinput1_3  # для старых систем

class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [
        ("wLeftMotorSpeed", ctypes.c_ushort),
        ("wRightMotorSpeed", ctypes.c_ushort)
    ]

# стартовое значение
intensity = 255  
left_enabled = True
right_enabled = True

print("Вибрация включена.")
print("↑/↓ = сила (шаг 5, 255 = OFF)")
print("← = включить/выключить левый мотор")
print("→ = включить/выключить правый мотор")
print("ESC = выход")

try:
    while True:
        # вычисляем значения моторов
        left_value = 0 if not left_enabled or intensity == 255 else intensity
        right_value = 0 if not right_enabled or intensity == 255 else intensity

        vib = XINPUT_VIBRATION(left_value, right_value)
        xinput.XInputSetState(0, ctypes.byref(vib))

        # управление ↑/↓
        if keyboard.is_pressed("up"):
            intensity = min(65535, intensity + 5)
            print(f"Intensity: {intensity}")
            time.sleep(0.05)

        if keyboard.is_pressed("down"):
            if intensity > 255:
                intensity = max(255, intensity - 5)
            print(f"Intensity: {intensity}")
            time.sleep(0.05)

        # переключение левого мотора
        if keyboard.is_pressed("left"):
            left_enabled = not left_enabled
            print(f"Left motor: {'ON' if left_enabled else 'OFF'}")
            time.sleep(0.2)  # антидребезг

        # переключение правого мотора
        if keyboard.is_pressed("right"):
            right_enabled = not right_enabled
            print(f"Right motor: {'ON' if right_enabled else 'OFF'}")
            time.sleep(0.2)

        if keyboard.is_pressed("esc"):
            break

        time.sleep(0.01)

finally:
    # выключаем оба мотора при выходе
    xinput.XInputSetState(0, ctypes.byref(XINPUT_VIBRATION(0, 0)))
    print("Вибрация остановлена")
