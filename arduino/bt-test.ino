/*
  Analog input, analog output, serial output

 Reads an analog input pin, maps the result to a range from 0 to 255
 and uses the result to set the pulsewidth modulation (PWM) of an output pin.
 Also prints the results to the serial monitor.

 The circuit:
 * potentiometer connected to analog pin 0.
   Center pin of the potentiometer goes to the analog pin.
   side pins of the potentiometer go to +5V and ground
 * LED connected from digital pin 9 to ground

 created 29 Dec. 2008
 modified 9 Apr 2012
 by Tom Igoe

 This example code is in the public domain.

 */
#include <avr/io.h>
#include <stdint.h>
#include <SoftwareSerial.h>

#define TOP_VAL 550
#define BOT_VAL 470
#define DEBUG 0
// These constants won't change.  They're used to give names
// to the pins used:
const uint8_t analogInPin = A0;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0;        // value read from the pot
bool active, check = false;
uint16_t ticks = 0;
uint8_t cups = 0;
int tries = 100;

SoftwareSerial softSerial(10, 11); // RX, TX

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  softSerial.begin(9600);
}

void loop() {
  if(!active)
  {
      sensorValue = analogRead(analogInPin);
      if(sensorValue < 470 || sensorValue > 550)
      {
        active = true;
        ticks = 0;
        tries = 100;
        delay(1000);
      }
      delay(2);
  }
  if(active)
  {
      while(tries)
      {
        sensorValue = analogRead(analogInPin);
        if(sensorValue < 470 || sensorValue > 550)
        {
          ticks++;
#ifdef DEBUG
          softSerial.print("tick\n");
          Serial.print("tick\n");
#endif          
          tries = 100;
          // Send 'active' at tick 1 to reduce false positives
          if(ticks == 1)
          {
            softSerial.print("active\n"); 
#ifdef DEBUG
            Serial.print("active\n");
#endif
          }
          delay(1000);
        }
        else
        {
          tries--;
          if(tries == 0)
          {
            active = false;
            softSerial.print("done ");
            softSerial.print(ticks);
            softSerial.print("\n");
#ifdef DEBUG
            Serial.print("done ");
            Serial.print(ticks);
            Serial.print("\n");
#endif              
          }
          delay(2);
        }
      }
  }
}
