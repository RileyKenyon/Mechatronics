#include <Wire.h>
#define DEVICE_ADD 0x04

char command[13];
char value_arr[13];
int value;
boolean command_flag = false;
boolean value_flag = false;
const int AIN1 = 13;
const int AIN2 = 12;
const int PWMA = 11;

void setup()
{
  Serial.begin(115200);
  Wire.begin(DEVICE_ADD);
  Wire.onReceive(receiveEvent);
  pinMode(AIN1,OUTPUT);
  pinMode(AIN2,OUTPUT);
  pinMode(PWMA,OUTPUT);
}

void loop()
{
  delay(1000);
  //Serial.println(c[1]); 
}

void receiveEvent(int howMany)
{
  int bufferIndex = 0;
  while (Wire.available() > 0)
  {
    int temp = Wire.read();
    if (temp == 0){
      continue;
    }
    if (command_flag == true)
      command[bufferIndex] = temp;
    if (value_flag == true)
      value_arr[bufferIndex] = temp;
    if (char(temp) == '|'){
      command_flag = false;
      value_flag = true;
      command[bufferIndex] = '\0';
      bufferIndex = 0; 
    }
    else if (char(temp) == '<'){
     command_flag = true;
     bufferIndex = 0; 
    }
    else if (char(temp) == '>'){
      value_flag = false;
      value_arr[bufferIndex] = '\0';
      value = atoi(value_arr);
      bufferIndex = 0;  
    }
    else{
    //Serial.println(byte(temp));
    bufferIndex++;
    }
  }
  Serial.println(String(command));
  Serial.println(value);
  if (strcmp(command,"MOT-CCW") == 0)
  {
    driveMotor(true,value);
  }  
  else if (strcmp(command,"MOT-CWO") == 0)
  {
    Serial.println("Clockwise");
    driveMotor(false,value);
  }
  
}

void driveMotor(boolean dir,int sp)
{
  sp = map(sp,0,100,0,255);
  if (sp == 0)
  {
    digitalWrite(AIN1,LOW);
    digitalWrite(AIN2,LOW);
  }
  else if (dir == true)
  {
    digitalWrite(AIN1,HIGH);
    digitalWrite(AIN2,LOW);
  } 
  else if(dir == false)
  {
    digitalWrite(AIN1,LOW);
    digitalWrite(AIN2,HIGH); 
  }
  analogWrite(PWMA,sp);
  //Serial.println(sp);
  //Serial.println(dir);
}


