const int prox1 = A4;
const int prox2 = A5;
const int switchPin = 13;

const int AIN1 = 7;
const int AIN2 = 6;
const int PWMA = 5;

const int BIN1 = 10;
const int BIN2 = 11;
const int PWMB = 9;

float distance[2];
float ref;
int factor = 200;

void setup(){
  pinMode(prox1,INPUT); 
  pinMode(prox2,INPUT);
  pinMode(switchPin,INPUT_PULLUP);
  
  pinMode(AIN1,OUTPUT);
  pinMode(AIN2,OUTPUT);
  pinMode(PWMA,OUTPUT);
  pinMode(BIN1,OUTPUT);
  pinMode(BIN2,OUTPUT);
  pinMode(PWMB,OUTPUT);
  
  digitalWrite(AIN1,LOW);
  digitalWrite(BIN1,LOW);
  digitalWrite(AIN2,HIGH);
  digitalWrite(BIN2,HIGH);
  
  analogWrite(PWMA,0);
  analogWrite(PWMB,0);
  
  Serial.begin(9600);
}

void loop(){
  //Initialize reference
  if (digitalRead(switchPin) == HIGH){
    getDistance();
    ref = distance[0];
    
    analogWrite(PWMA,0);
    analogWrite(PWMB,0);
  }
  else{
    getDistance(); // Sensor 0 is on the left side of the vehicle
    
    float diff = distance[0]-ref;
    //B faster if diff>0
    
    int spA = min(max(127-factor*diff,0),255);
    int spB = min(max(127+factor*diff,0),255);
    
    Serial.print("A: ");
    Serial.print(spA);
    Serial.print("   B: ");
    Serial.println(spB);
    //Serial.println((6762/((distance[0]*1024/5)-9))-4);
    
    analogWrite(PWMA,spA);
    analogWrite(PWMB,spB);
    
    
//    Serial.print("Distance0:   ");
//    Serial.print(distance[0]);
//    Serial.print("   Distance1:   ");
//    Serial.println(distance[1]);
  }
}

void getDistance(){
  int numSamples = 5;
  float totDist[2] = {
    0,0  }; 
  float dist[2] = {
    0,0  };
  for(int i = 0;i<numSamples;i++){
    dist[0] = analogRead(prox1);
    dist[0] = dist[0]*5/1024;
    dist[1] = analogRead(prox2);
    dist[1] = dist[1]*5/1024;
    totDist[0] = dist[0] + totDist[0];
    totDist[1] = dist[1] + totDist[1];
    delay(40);
  }
  distance[0] = totDist[0]/numSamples;
  distance[1] = totDist[1]/numSamples;
}

