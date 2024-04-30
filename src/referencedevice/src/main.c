// 
// Compatible with ATtiny13A/ATtiny85/ATtiny2313A microcontroller
// Bit shift (counter) through PB0-4 pins
//

#include <avr/io.h>
#include <util/delay.h>


/**
 * DDRB  - direction registry (0 input; 1 output)
 * PORTB - set output to pins
 * _BV   - shift bit by given number of places (usually pin index)
 */


#define set_on(pin_code) {              \
    PORTB = PORTB | _BV(pin_code);      \
}


#define set_off(pin_code) {            \
    PORTB = PORTB & ~_BV(pin_code);    \
}


#define toggle(pin_code) {             \
    PORTB = PORTB ^ _BV(pin_code);     \
}


/// led blinks with frequency 4Hz
void blink_led() {
    while(1) {
    	_delay_ms(250);
    	toggle(0);
    }
}


/// state change frequencies:
/// PB0 100 Hz
/// PB1  50 Hz
/// PB2  25 Hz
/// PB3  12.5 Hz
/// PB4  6.25 Hz
void standard_counter() {
    unsigned int counter = 0;		/// 16 bit

    while(1) {
    	_delay_ms(10);

    	PORTB = counter;

    	counter = (counter + 1) % 0x40;		/// 0010 0000 = 64
    }
}


//void div_counter() {
//    unsigned int counter = 0;		/// 16 bit
//    unsigned int pinval = 0;		/// 16 bit
//
//    while(1) {
//        /// 10 us gives 100kHz base frequency
//        /// pin PB0 will toggle with frequency 100 000 Hz
//        /// pin PB1 will toggle with frequency  25 000 Hz
//        /// pin PB2 will toggle with frequency   6 250 Hz
//        /// pin PB3 will toggle with frequency   1 562 Hz
//        /// pin PB4 will toggle with frequency     390 Hz
//
//        _delay_us(10);        /// influenced by fuses but should be compensated by value of F_CPU (e.g. internal clock and divider)
//
//        pinval  =  counter & 0x0001;
//        pinval |= (counter & 0x0004) >> 1;
//        pinval |= (counter & 0x0010) >> 2;
//        pinval |= (counter & 0x0040) >> 3;
//        pinval |= (counter & 0x0100) >> 4;
//
//        PORTB = pinval;
//
//        if (counter >= 0x0400) {
//        	counter = 0;
//        }
//    }
//}


/**
 *
 */
int main() {
    /// set output pins
    DDRB |=  _BV(PB0);
    DDRB |=  _BV(PB1);
    DDRB |=  _BV(PB2);
    DDRB |=  _BV(PB3);
    DDRB |=  _BV(PB4);

    PORTB = 0;				    	/// set all low

    standard_counter();

    /// div_counter()

    return 0;
}
