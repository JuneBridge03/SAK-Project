import os

NUMBER_OF_MEDICINE_CONTAINER = 8
RESOURCE_DIR_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "\\" + "resources" + "\\"

'''
Rpi Pin setting
'''

#GPIO setting
GPIO_BUZZER = 23
GPIO_BUTTON = 22

#ADC setting
ADC_SPI_BUS_NUM = 1
ADC_SPI_DEVICE_NUM = 2
ADC_CHANNEL_BPM = 0
