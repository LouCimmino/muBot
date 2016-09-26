#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/time.h>
#include "map.h"
#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)
int  mem_fd;
void *gpio_map;
#define BCM2708_PERI_BASE        0x20000000
#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000)

volatile unsigned *gpio;
// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))
#define GPIO_LEV *(gpio+13)                  // pin level
#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0

void setup_io();
void reset();
void set_pin_output(unsigned short pin);

int main(int argc, char **argv) {
	setup_io();
	
	reset();
}

void setup_io() {
	if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
		printf("Error no /dev/mem \n");
		exit(-1);
	}

	/* mmap GPIO */
	gpio_map = mmap(
		NULL,             //Any adddress in our space will do
		BLOCK_SIZE,       //Map length
		PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
		MAP_SHARED,       //Shared with other processes
		mem_fd,           //File to map
		GPIO_BASE         //Offset to GPIO peripheral
	);

	close(mem_fd);

	if (gpio_map == MAP_FAILED) {
		printf("mmap error %d\n", (int)gpio_map);//errno also set!
		exit(-1);
	}
	gpio = (volatile unsigned *)gpio_map;
}

void set_pin_output(unsigned short pin) {
	INP_GPIO(pin);
	OUT_GPIO(pin);
}

void reset() {
	/* Reset board */ 
	set_pin_output(RST);
	GPIO_CLR = 1 << RST;
	GPIO_SET = 1 << RST; 	// 5 SET di RST producono un reset di 60 nani
	GPIO_SET = 1 << RST;
	GPIO_SET = 1 << RST;
	GPIO_SET = 1 << RST;
	GPIO_SET = 1 << RST;
	GPIO_CLR = 1 << RST;
}
