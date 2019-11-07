import gpiozero as gpio
import time

lights = gpio.LED(18, initial_value=False)
on_led = gpio.LED(23, initial_value=False)
off_led = gpio.LED(24, initial_value=True)


lights.on()
on_led.on()
off_led.off()

time.sleep(0.5)

lights.off()
on_led.off()
off_led.on()

print("FLASH_ACKNOWLEDGE")