Title: CP2102 and Arduino
Date: 2015-12-16 21:01
Category: Electronics Projects
Tags: arduino, electronics, usb, serial
Slug: cp2102-and-arduino
Authors: Craig J Perry
Summary: Connecting A CP2102 To An Arduino Pro Mini

There are 4 main USB to Serial chips sold on eBay:

* Genuine FTDI, rare and most expensive. Has the best drivers.
* Fake FTDI, common and cheap. Shares the best drivers.
* CP2102, common and cheap. Now has good drivers on all platforms
* CH340G, ultra cheap and currently has terrible drivers although it's still quite new so this may change

To connect a CP2102 to an Arduino Pro Mini:

    |  CP2102   |  Arduino |
	| 5v / 3.3v | Vcc      |
	| Txd       | Txd      |
	| Rxd       | Rxd      |
	| GND       | GND      |
	| DTR       | DTR      |

**NB:** the pinouts are confusing here, i'd expect Txd to connect to Rxd and vice versa. Similarly i'd
expect DTR to be labelled RTS. The above is correct on my version of the cp2102 but it did cause me
some consternation to find this!

Different versions of the CP2102 breakout board are available. Some make for neater wiring connections
than others but all work just as well.