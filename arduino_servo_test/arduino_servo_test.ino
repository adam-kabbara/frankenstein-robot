#include <Servo.h> 

Servo servo; 
int min_ = -20;    // variable to store the servo position 
int max_ = 40;
int pos = min_;
void setup() {
    Serial.begin(9600);

  servo.attach(3); // servo is wired to Arduino on digital pin 3
  Serial.println();    
}

void loop() {
  //  servo.write(25);
    Serial.println(servo.read());    
    delay(2000);         
//    servo.write(123); 
    Serial.println(servo.read())  ;     
    delay(2000);         
  
}
