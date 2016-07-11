/*



 */
#include <avr/io.h>
#include <stdint.h>
#include <SoftwareSerial.h>

#define TOP_VAL 550
#define BOT_VAL 470
#define DEBUG 0
// Analog input pin that the sensor is attached to
const uint8_t analogInPin = A0;  
// value read from the sensor
int sensorValue = 0;        
bool active, check = false;
uint16_t ticks = 0;
uint8_t cups = 0;
int tries = 100;

SoftwareSerial softSerial(10, 11); // RX, TX

void setup() {
// initialize serial communications at 9600 bps:
#ifdef DEBUG
    Serial.begin(9600);
#endif
    softSerial.begin(9600);
}

void loop() {
    if(!active)
    {
        // Read the sensor value
        sensorValue = analogRead(analogInPin);
        // If the value is outside the span there is current
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
        // Check if there is current every second.
        while(tries)
        {
            sensorValue = analogRead(analogInPin);
            // If there is still current, count ticks (seconds)
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
                // If there is no current, go back to initial state
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
