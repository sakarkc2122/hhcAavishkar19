// for the data to send to server


#include<ESP8266WiFi.h>
#include<ESP8266HTTPClient.h>
#include<WiFiClient.h>
char* ssid = "KU Wireless";
char* password = "";

const int trigPin1 = 5;  //D1
const int echoPin1 = 4;  //D2
//const int trigPin2 = 2;  //D4
//const int echoPin2 = 0;  //D3

long duration1;
float distance1;

void setup() {
pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
//pinMode(trigPin2, OUTPUT); // Sets the trigPin as an Output
//pinMode(echoPin2, INPUT);
Serial.begin(115200); // Starts the serial communication
WiFi.begin(ssid, password);
while(WiFi.status() != WL_CONNECTED)
{
  Serial.println("Wifi not connecetd");
  delay(1000);
}
Serial.println("WiFi Connected");
Serial.println("IP ADDRESS:");
Serial.println(WiFi.localIP());
}

void loop() {

// Clears the trigPin
digitalWrite(trigPin1, LOW);
//digitalWrite(trigPin2, LOW);
//delayMicroseconds(2);

// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin1, HIGH);
//digitalWrite(trigPin2, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin1, LOW);
//digitalWrite(trigPin2, LOW);
                                                                                           
// Reads the echoPin, returns the sound wave travel time in microseconds
duration1 = pulseIn(echoPin1, HIGH);
//duration2 = pulseIn(echoPin2, HIGH);
// Calculating the distance
distance1= duration1*0.034/2;
//distance2= duration2*0.034/2;
// Prints the distance on the Serial Monitor
Serial.print("Distance1: ");
Serial.println(distance1);
//Serial.print("Distance2: ");
//Serial.println(distance2);

if(WiFi.status() == WL_CONNECTED)
{
  HTTPClient http;
  http.begin("http:// 192.168.137.1/Hackathon/insert.php?distance1="+String(distance1));
  http.addHeader("Content-Type", "application/json");
  int httpCode =  http.GET();
  if(httpCode>0)
  {
     String payload = http.getString();
      Serial.println(httpCode);
      Serial.println(payload);
  }
  else
  {
    Serial.println("Error on HTTP request");
  }
  http.end();
}
delay(100);
}
