#define TX_TIME 40       // time (in µs) spent by the clock high or low.
#define CLOCK   50       // WHITE wire.
#define DATA    52       // PURPLE wire.
#define BAUDRATE 115200  // the rate of the communication.
#define TIMEOUT 1        // timeout for the communication.





void setup() {
  // initialize the pins.
  pinMode(CLOCK, OUTPUT);
  pinMode(DATA, OUTPUT);

  // open the Serial communication stream.
  Serial.begin(BAUDRATE);
  Serial.setTimeout(TIMEOUT);
}





// the loop function runs over and over again forever
void loop() {
  while (!Serial.available());
  char inChar = Serial.read();
  send_with_ps2(inChar);
}





/**
 * Sends a character to the 6502.
 */
void send_with_ps2(char c){
  // the first bit is always 0.
  digitalWrite(DATA, 0);
  pulse_us(CLOCK, HIGH, TX_TIME);
  delayMicroseconds(TX_TIME);

  int b;
  int parity = 1;
  for (int i = 0; i < 8; i++){
    b = (c >> i) & 1;
    parity = parity + b;
    digitalWrite(DATA, b);
    pulse_us(CLOCK, HIGH, TX_TIME);
    delayMicroseconds(TX_TIME);
  }

  int parity_bit = parity & 1;
  // send the parity bit.
  digitalWrite(DATA, parity_bit);
  pulse_us(CLOCK, HIGH, TX_TIME);
  delayMicroseconds(TX_TIME);

  // the last bit is always 1.
  digitalWrite(DATA, 1);
  pulse_us(CLOCK, HIGH, TX_TIME);
  delayMicroseconds(TX_TIME);

  digitalWrite(DATA, 0);
  pulse_us(CLOCK, HIGH, TX_TIME);
  delayMicroseconds(TX_TIME);
}


/**
 * Pulses to the desired pin, any logic level for any
 * duration.
 * time is expressed in ms.
 */
void pulse_ms(int pin, int level, int time){
    digitalWrite(pin, 1 - level);
    digitalWrite(pin, level);
    delay(time);
    digitalWrite(pin, 1 - level);
}


/**
 * Pulses to the desired pin, any logic level for any
 * duration.
 * time is expressed in µs.
 */
void pulse_us(int pin, int level, int time){
    digitalWrite(pin, 1 - level);
    digitalWrite(pin, level);
    delayMicroseconds(time);
    digitalWrite(pin, 1 - level);
}

