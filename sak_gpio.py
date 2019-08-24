import spidev
import RPi.GPIO as GPIO
import time
import sak_setting


def set_gpios():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sak_setting.GPIO_BUZZER, GPIO.OUT)
    GPIO.setup(sak_setting.GPIO_BUTTON, GPIO.IN)


def get_from_adc(bus_num = 0, device_num: int = 0, channel: int = 0):
    spi = spidev.SpiDev()
    spi.open(bus_num, device_num)
    #r = spi.xfer2([6 + ((4&channel) >> 2), (3&channel) << 6, 0])
    r = spi.xfer2([0x06 | ((channel & 0x07) >> 7), (channel & 0x07)<<6, 0x00])
    print(0x06 | ((channel & 0x07) >> 7))
    acd_out = ((r[1] & 15) << 8) | r[2]
    spi.close()
    return acd_out


def get_bpm():
    return get_from_adc()
    #return get_from_adc(sak_setting.ADC_SPI_BUS_NUM, sak_setting.ADC_SPI_DEVICE_NUM, sak_setting.ADC_CHANNEL_BPM)


def out_beep_sound():
    while True:
        GPIO.output(sak_setting.GPIO_BUZZER, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(sak_setting.GPIO_BUZZER, GPIO.LOW)
        time.sleep(0.5)

def get_button():
        return GPIO.input(sak_setting.GPIO_BUTTON)


def gpio_cleanup():
        GPIO.cleanup()
        
