import gpiozero as gpio
import time

lights = gpio.LED(12, initial_value=False)

lights.on()

time.sleep(0.5)

lights.off()

print("FLASH_ACKNOWLEDGE")