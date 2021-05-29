#include <SoftwareSerial.h>
/*
  shiftOut ra 1 Module LED 7 đoạn đơn
*/
SoftwareSerial Arduino(0, 1);

#define led_green 2
#define led_yellow 3
#define led_red 4

//int green_time, red_time;
int cycle ;
int short_lane = 20;
int long_lane = 56;
int medium_cycle = 82;

int yellow = 3;
int green_time;
int green_old;

//chân ST_CP của 74HC595
int latchPin = 8;
//chân SH_CP của 74HC595
int clockPin = 12;
//Chân DS của 74HC595
int dataPin = 11;

// Ta sẽ xây dựng mảng hằng số với các giá trị cho trước
// Các bit được đánh số thứ tự (0-7) từ phải qua trái (tương ứng với A-F,DP)
// Vì ta dùng LED 7 đoạn chung cực dương nên với các bit 0
// thì các đoạn của LED 7 đoạn sẽ sáng
// với các bit 1 thì đoạn ấy sẽ tắt

//mảng có 10 số (từ 0-9) và
const byte Seg[10] = {
  0b11000000,//0 - các thanh từ a-f sáng
  0b11111001,//1 - chỉ có 2 thanh b,c sáng
  0b10100100,//2
  0b10110000,//3
  0b10011001,//4
  0b10010010,//5
  0b10000010,//6
  0b11111000,//7
  0b10000000,//8
  0b10010000,//9
};


void setup() {
  //Bạn BUỘC PHẢI pinMode các chân này là OUTPUT
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  //Led output
  pinMode(led_green, OUTPUT);
  pinMode(led_yellow, OUTPUT);
  pinMode(led_red, OUTPUT);

  digitalWrite(led_green, LOW);
  digitalWrite(led_yellow, LOW);
  digitalWrite(led_red, LOW);

  //  pinMode(0, INPUT);
  //  pinMode(1, OUTPUT);
  //  digitalWrite(0, LOW);
  //  digitalWrite(1, HIGH);

  Serial.begin(115200);
  Arduino.begin(9600);
}

void loop() {
  while (Arduino.available() > 0)
  {
    int a = Arduino.available();
    Serial.println (a);
    green_time = Arduino.parseInt();
    if (green_time != 0 )
    {
      green_old = green_time;
      if (green_old == short_lane)
        cycle = (green_old + 3) * 2;
      else if (green_old == long_lane)
        cycle = (green_old + 3) * 2;
      else
        cycle = medium_cycle;
    }
    Serial.println(green_time);
    while (green_time == 0)
    {
      Serial.println(green_old);
      show_control(green_old, yellow, (cycle - (green_old + 3)));
      green_time = Arduino.parseInt();
      if (green_time != 0)
      {
        green_old = green_time;
        if (green_old == short_lane)
          cycle = (green_old + 3) * 2;
        else if (green_old == long_lane)
          cycle = (green_old + 3) * 2;
        else
          cycle = medium_cycle;
      }
    }
    Serial.println(green_old);
    show_control(green_old, yellow, (cycle - (green_old + 3)));
  }
}

void HienThiLED7doan(unsigned long Giatri, byte SoLed = 2)
{
  byte *array = new byte[SoLed];
  for (byte i = 0; i < SoLed; i++) {
    //Lấy các chữ số từ phải quá trái
    array[i] = (byte)(Giatri % 10UL);
    Giatri = (unsigned long)(Giatri / 10UL);
  }
  digitalWrite(latchPin, LOW);
  for (int i = SoLed - 1; i >= 0; i--)
    shiftOut(dataPin, clockPin, MSBFIRST, Seg[array[i]]);

  digitalWrite(latchPin, HIGH);
  free(array);
}

void show_control(int green, int yellow, int red )
{
  while (green >= 0)
  {
    HienThiLED7doan(green, 2);
    digitalWrite(led_green, HIGH);
    green--; // Vòng tuần hoàn từ 0--99
    delay(1000);//Đợi 0.5 s cho mỗi lần giảm số
    if (green == 0); digitalWrite(led_green, LOW);
  }
  while (yellow >= 0)
  {
    HienThiLED7doan(yellow, 2);
    digitalWrite(led_yellow, HIGH);
    yellow--;
    delay(1000);
    if (yellow == 0); digitalWrite(led_yellow, LOW);
  }
  while (red >= 0)
  {
    HienThiLED7doan(red, 2);
    digitalWrite(led_red, HIGH);
    red --;
    delay(1000);
    if (red == 0); digitalWrite(led_red, LOW);
  }
}
