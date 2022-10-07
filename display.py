import drivers
import time
from gpiozero import Button

btnOui = Button(20)
btnNon = Button(21)
lcd = drivers.lcd()  

def lcdClear():
   lcd.lcd_display_string("                ",1)
   lcd.lcd_display_string("                ",2)

def newFruit():
   lcdClear()
   lcd.lcd_display_string("Posez votre  ",1)
   lcd.lcd_display_string("  panier  ",2)

def helloUser(name):
      lcdClear()
      lcd.lcd_display_string("   Bienvenue    ",1)
      lcd.lcd_display_string(" %s             "%name,2)
      time.sleep(2)

def qrCode():
      lcdClear()
      lcd.lcd_display_string("   Presentez    ",1)
      lcd.lcd_display_string("  votre QRcode  ",2)

def loading():
      lcdClear()
      lcd.lcd_display_string("   Analyse      ",1)
      time.sleep(0.1)
      lcd.lcd_display_string("   Analyse .    ",1)
      time.sleep(0.1)
      lcd.lcd_display_string("   Analyse ..   ",1)
      time.sleep(0.1)
      lcd.lcd_display_string("   Analyse ...  ",1)
      time.sleep(0.1)
      lcd.lcd_display_string("   Analyse ..   ",1)
      time.sleep(0.1)
      lcd.lcd_display_string("   Analyse .    ",1)
      time.sleep(0.1)
      lcd.lcd_display_string("   Analyse      ",1)


def callUser(label):
    if label == 'tomato':
       label = "Tomate"
    if label == 'apple':
       label = "Pomme"
    pressed = False
    lcd = drivers.lcd()
    lcd.lcd_display_string("    %s ?"%label, 1)
    lcd.lcd_display_string("Faux        Vrai", 2)
    while not pressed:
        if btnOui.is_pressed:
            lcdClear()
            lcd.lcd_display_string(" Achat effectue ", 1)
            lcd.lcd_display_string("                ", 2)
            time.sleep(3)
            return True
        elif btnNon.is_pressed:
            return False

def otherProduct():
    pressed = False
    lcd = drivers.lcd()
    lcd.lcd_display_string("Un autre panier?", 1)
    lcd.lcd_display_string("Non          Oui", 2)
    while not pressed:
        if btnOui.is_pressed:
            lcdClear()
            return True
        elif btnNon.is_pressed:
            lcdClear()
            lcd.lcd_display_string("Au revoir       ", 1)
            lcd.lcd_display_string("Bonne Journee   ", 2)
            time.sleep(2)
            return False

def fonc1():
    lcdClear()
    lcd.lcd_display_string("oui", 1)
    
def fonc2():
    lcdClear()
    lcd.lcd_display_string("non", 1)
    
    

