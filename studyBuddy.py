import board
import neopixel
import time
import RPi.GPIO as GPIO

def wheel(pos):
    if pos <= 127:
        r = 255 - int((pos / 127) * 255)
        g = int((pos / 127) * 255)
        b = 0
    else:
        pos -= 128
        r = 0
        g = 255 - int((pos / 127) * 255)
        b = int((pos / 127) * 255)
    return (r,g,b)

def callback(micChannelIn, soundScore):
    if GPIO.input(micChannelIn):
        soundScore += 1
    else:
        soundsScore -= 1

    if soundScore > 10:
        soundsScore = 10
    elif soundScore < 0:
        soundScore = 0

    return soundScore

def activatePanicLED(pin):
    GPIO.output(pin, GPIO.HIGH)

def deactivatePanicLED(pin):
    GPIO.output(pin, GPIO.LOW)

nPixels = 16
pixels = neopixel.Neopixel(board.D18, nPixels, auto_write=True)

dataPin = 18
downBrightnessPin = 26
upBrightnessPin = 20
downColourPin = 19
upColourPin = 16
panicLEDPin = 21
panicButtonPin = 12
micChannelIn = 27
micChannelOut = 22
panicButtonPressed = False
soundScore = 0
soundThreshold = 2
brightness = 125
colour = 125

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(upColourPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(downColourPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(upBrightnessPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(downBrightnessPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(panicButtonPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(panicLEDPin, GPIO.OUT)
GPIO.setup(micChannelIn, GPIO.IN)
GPIO.setup(micChannelOut, GPIO.OUT)


try:
    while True:
        if GPIO.input(upColourPin) == GPIO.HIGH:
            colour += 5
        elif GPIO.input(downColourPin) == GPIO.HIGH:
            colour -= 5

        if colour > 255:
            colour = 255
        elif colour < 0:
            colour = 0

        if GPIO.input(upBrightnessPin) == GPIO.HIGH:
            brightness += 15
        elif GPIO.input(upBrightnessPin) == GPIO.HIGH:
            brightness -= 15

        if brightness > 255:
            brightness = 255
        elif brightness < 0:
            brightness = 0

        if GPIO.input(panicButtonPin) == GPIO.HIGH:
            time.sleep(0.1)
            if GPIO.input(panicLEDPin) == GPIO.LOW:
                panicButtonPressed = True

                if soundScore < soundThreshold:
                    soundThreshold -= 1

                    if soundThreshold < 0:
                        soundThreshold = 0

            else:
                panicButtonPressed = False
        
        pixels.fill(wheel(colour))
        pixels.brightness = brightness / 255
        soundScore = callback(micChannelIn, soundThreshold)

        if panicButtonPressed or soundScore < soundThreshold:
            activatePanicLED(panicLEDPin)
        else:
            deactivatePanicLED(panicLEDPin)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program...")
    
finally:
    pixels.fill((0,0,0))
    pixels.show()
    GPIO.output(panicLEDPin, GPIO.LOW)
    print("LEDs cleared")
    GPIO.cleanup()
