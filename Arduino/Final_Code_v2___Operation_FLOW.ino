//~~~Libraries
//~~~~~~~~~~~~~~~~~~~~~~~~Stepper Motor (Washing)
#include <Stepper.h>

//~~~~~~~~~~Water Level Sensor pins
#define SIGNAL_PIN 52

//~~~~~~~~~~Water Inlet Valve represented by Green LED
#define LEDinlet 3
//~~~~~~~~~~Water Outlet Valve represented by Orange LED
#define LEDdrain 4
//~~~~~~~~~~Ultra Sonic Cleaner 
#define UltraSonic 5
//~~~~~~~~~~Fan
#define Fan 2
//~~~~~~~~~LED UV
#define LEDUV 9
//~~~~~~~~~Temp/Humidity
#include "dht.h"
#define dht_apin A0
dht DHT;
//~~~~~~~~~LED for ML
#define LEDML 30

//~~~~~~~~~~Value for storing water level
//int WaterLevel = 0;
int WaterLevel = digitalRead(SIGNAL_PIN);

//~~~~~~~~~~Stepper Motor (Washing)Settings
const float STEPS_PER_REV = 32; 
const float GEAR_RED = 64;
const float STEPS_PER_OUT_REV = STEPS_PER_REV * GEAR_RED;
int StepsRequired;
Stepper steppermotor(STEPS_PER_REV, 22, 24, 23, 25);
int countWASHING = 0;
int countDRYING = 0;
int countDRYING2 = 0;

void setup() 
{
  Serial.begin(9600);
  //~~~~~~~ Ultra Sonic Cleaner
  pinMode(UltraSonic, OUTPUT);
  //~~~~~~~~~~~~~~~~~~ Water Level Sensor Setup
  // Set D52 as an OUTPUT
  pinMode(SIGNAL_PIN, INPUT);
  Serial.begin(9600);

  //~~~~~~~~~~~~~~~~~ Water Inlet Valve
  pinMode(LEDinlet, OUTPUT);
  LEDinlet == HIGH;
  //~~~~~~~~~~~~~~~~~ Water Outlet Valve
  pinMode(LEDdrain, OUTPUT);
  LEDdrain == HIGH;
  //~~~~~~~~~~~~~~~~~ Fan
  pinMode(Fan, OUTPUT);
  //~~~~~~~~~~~~~~~~~~LED UV
  pinMode(LEDUV, OUTPUT);
  //LEDUV == HIGH;
  //~~~~~~~~~~~~~~~~~ LED for ML
  pinMode(LEDML, OUTPUT);
}


//~~~~~~~~~~~ Functions
void Washing()
{
  countWASHING = 0;
  while (countWASHING < 3) // 1 min 3 sec
  {
    // Slow - 4-step CW sequence to observe lights on driver board
    // Rotate CW 
    StepsRequired  =  STEPS_PER_OUT_REV / 2.2; 
    steppermotor.setSpeed(1000);   
    steppermotor.step(StepsRequired);
    delay(1000);
    
    // Rotate CCW
    StepsRequired  =  - STEPS_PER_OUT_REV / 2.2;   
    steppermotor.setSpeed(1000);  
    steppermotor.step(StepsRequired);
    delay(1000);

    Serial.print("Cycle :");
    Serial.println(countWASHING);
    countWASHING++;
  }
  
}
void Drying()
{
  countDRYING = 0;
  while (countDRYING <= 5)// 2min 6 sec
  {
    // Slow - 4-step CW sequence to observe lights on driver board
    // Rotate CW 
    StepsRequired  =  STEPS_PER_OUT_REV / 2.2; 
    steppermotor.setSpeed(870);   
    steppermotor.step(StepsRequired);
    delay(1000);
    
    // Rotate CCW
    StepsRequired  =  - STEPS_PER_OUT_REV / 2.2;   
    steppermotor.setSpeed(870);  
    steppermotor.step(StepsRequired);
    delay(1000);
    
    Serial.print("Cycle :");
    Serial.println(countDRYING);
    countDRYING++;
  }
  
}
void Drying2()
{
  countDRYING2 = 0;
  while (countDRYING2 <= 2)// 2min 6 sec
  {
    // Slow - 4-step CW sequence to observe lights on driver board
    // Rotate CW 
    StepsRequired  =  STEPS_PER_OUT_REV / 2.2; 
    steppermotor.setSpeed(870);   
    steppermotor.step(StepsRequired);
    delay(1000);
    
    // Rotate CCW
    StepsRequired  =  - STEPS_PER_OUT_REV / 2.2;   
    steppermotor.setSpeed(870);  
    steppermotor.step(StepsRequired);
    delay(1000);
    
    Serial.print("Cycle :");
    Serial.println(countDRYING2);
    countDRYING2++;
  }
  
}
void Sterilization ()
{
  digitalWrite(LEDUV, LOW); // Turn the LED on
  Serial.println("UV on");
  delay(10000);
  digitalWrite(LEDUV, HIGH);
  Serial.println("UV off");
}

void Humidity()
{
  DHT.read11(dht_apin);
  Serial.print("Current humidity = ");
  Serial.print(DHT.humidity);
  Serial.print("%  ");
  Serial.print("temperature = ");
  Serial.print(DHT.temperature); 
  Serial.println("C  ");
  if(DHT.humidity >= 75 && DHT.humidity < 78)
    {
      Serial.println("Normal");
    }

  else if (DHT.humidity < 74)
    {
      Serial.println("Low");
    }

  else 
    {
      Serial.println("High");
    }

  delay(1000);
}

void LightsForML()
{
  digitalWrite(LEDML, HIGH); // Turn the LED on
  Serial.println("Lights for ML ON");
  delay(30000);
  digitalWrite(LEDML, LOW); // Turn the LED on
  Serial.println("Lights for ML OFF");
}

void DoneWashing()
{
  Serial.println("Done Washing");
  delay(100);
}

void DoneDrying()
{
  Serial.println("Done Drying");
  delay(100);
}

void loop() 
{
   digitalWrite(LEDUV, HIGH); // Turning OFF UV
  //get the reading from the function below and print it

  if (Serial.available() > 0) 
  {
  int data = Serial.read();
  //Serial.println(data);

       switch (data) 
       {
         case 'a': //~~~~~~~~~~~~~~~~~~~Begin Filling and washing
                Serial.print("Water level: ");
                Serial.println(WaterLevel);
                digitalWrite(LEDdrain, LOW); // Close Draining Valve
               
                while(WaterLevel == 0)
                {
                  digitalWrite(LEDinlet, HIGH); // Open water inlet valve
                  Serial.println("Inlet Valve open, Filling water ");
                  int WaterLevel = digitalRead(SIGNAL_PIN);
                  if(WaterLevel == 1)
                  {
                    digitalWrite(LEDinlet, LOW); // Close water inlet valve
                    Serial.println("Inlet Valve Close ");
                    delay(2000);
                    digitalWrite(UltraSonic, HIGH);
                    Serial.println("Ultra Sonic Cleaner ON ");
                    Serial.println("Washing Begins ");
                    Washing();
                    Serial.println("Washing Ends ");
                    delay(2000);
                    digitalWrite(UltraSonic, LOW);
                    Serial.println("Ultra Sonic Cleaner OFF ");
                    delay(2000);
                    digitalWrite(LEDdrain, HIGH);// Open Draining Valve
                    Serial.println("Drain Valve Open ");
                    delay(1000);
                    //Need to send "Done Washing" to RPI 1
                    Serial.println("Done Washing");
                    DoneWashing();
                    
                    break;
                  }   
                }
           break;

           case 'b' : //~~~~~~~~~~~~~~~~~~~~~~~~~~Drying Process
                digitalWrite(LEDdrain, HIGH);// Open Draining Valve
                Serial.println("Drying Begins");
                Serial.println("Fan turn ON");
                digitalWrite(Fan, HIGH);
                delay(2000);
                Drying();
                delay(2000);
                Sterilization (); // Turn ON BLUE LED
                delay(1000);
                digitalWrite(Fan, LOW);
                Serial.println("Fan turn OFF");
                delay(3000);
                DoneDrying();
            break;
           
           case 'c' : //~~~~~~~~~~~~~~~~~~~~~~~~~Additional Drying
                digitalWrite(LEDdrain, HIGH);// Open Draining Valve
                Serial.println("Drying Begins Round 2");
                Serial.println("Fan turn ON");
                digitalWrite(Fan, HIGH);
                delay(2000);
                Drying2();
                delay(2000);
                digitalWrite(Fan, LOW);
                Serial.println("Fan turn OFF");
                //Need to send "Done Drying" to RPI 1
                DoneDrying();
            break;

            case 'd' : //~~~~~~~~~~~~~~~~~~~~~Hiumidity
                Humidity();
                delay (2000);
            break;

            case 'e' : //~~~~~~~~~~~~~~~~~~~~~LED for ML
                LightsForML();
                delay(2000);
            break;
            
          }
  }
}
         
        
  //}
//}
