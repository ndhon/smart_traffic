#include <SoftwareSerial.h>

#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>

#define FIREBASE_HOST "signal-light-2d04c.firebaseio.com" //Thay bằng địa chỉ firebase của bạn
#define FIREBASE_AUTH "hGM9jFagI7Wf63fAXcMBbsmFrA9YaNXktSMvrirG"   //Không dùng xác thực nên không đổi
#define WIFI_SSID "Hi"   //Thay wifi và mật khẩu
#define WIFI_PASSWORD "987654321"

SoftwareSerial mySerial(13, 15); // RX, TX
FirebaseData firebaseData_red;

int red_time ;
int short_lane = 23;
int long_lane = 59;
int medium_cycle = 77;
int cycle = 0;
void setup()
{
  pinMode(13, INPUT);
  pinMode(15, OUTPUT);
  digitalWrite(13, LOW);
  digitalWrite(15, LOW);

  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  mySerial.begin(9600);

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

}

void loop()
{
  int old_red = red_time;
  Firebase.getInt(firebaseData_red, "Lane1/red_timing");
  red_time = firebaseData_red.intData();
  if (old_red != red_time)
  {
    mySerial.println(red_time);
    Serial.println(red_time);
    if (red_time == short_lane)
    {
      cycle = ((short_lane-3) * 2) + 1;
      Serial.println(cycle);
      delay(cycle * 1000);
    }
    else if (red_time == long_lane)
    {
      cycle = ((long_lane-3) * 2) + 1;
      Serial.println(cycle);
      delay(cycle * 1000);
    }
    else
    {
      cycle = medium_cycle;
      Serial.println(cycle);
      delay(cycle * 1000);
    }

  }

  //  b=0;
  //  Firebase.setInt(firebaseData, "Lane1/feedback", b);
  //  delay(1000);
}
