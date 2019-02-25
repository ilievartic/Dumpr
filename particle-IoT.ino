#include <Serial2/Serial2.h>
char inData[64];
char inChar=-1;
int n = 0;

void setup(){
   Serial.begin(9600);
   Serial1.begin(9600);
   Serial.println("Waiting for Raspberry Pi to send a signal...\n");
}


void loop(){
    
    if (Serial1.available()){
        inChar = Serial1.read();
        if(inChar == '\n'){
            inData[n] = '\0'; 
            n=0;
            Particle.publish("lic", String(inData), PRIVATE);
            Serial.println(inData);
        }else{
            inData[n] = inChar;
            n++;
        }
    }
    
    
}
