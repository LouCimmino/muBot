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
void ciclo_clock();
void set_pin_output(unsigned short pin);
void send_word(int GPIOpin, unsigned short word_to_send);
unsigned short send_cmd_easy(cmd_easy *cmd, int n);

int main(int argc, char **argv) {
	cmd_easy comm_e;
	int n;
	// Set up gpi pointer for direct register access
	setup_io();
	n=1;
	comm_e.data = calloc(n, sizeof(unsigned short));
	comm_e.cmd = CMD_EASY;
  
	comm_e.data[0]=CMD_RST_RR;
	send_cmd_easy(&comm_e, n);
	usleep(50);
	comm_e.data[0]=CMD_RST_PR;
	send_cmd_easy(&comm_e, n);
	usleep(50);
	comm_e.data[0]=CMD_RST_SCR;
	send_cmd_easy(&comm_e, n);
	free(comm_e.data);
}

unsigned short send_cmd_easy(cmd_easy *cmd, int n) {
	int i;
	set_pin_output(READ_PIN);
	GPIO_CLR = 1 << READ_PIN;
	set_pin_output(CHPSEL);
	GPIO_CLR = 1 << CHPSEL;
	set_pin_output(MOSI);
	send_word(MOSI, cmd->cmd);
	for (i=0; i<n; i++) {
		send_word(MOSI, cmd->data[i]);
		//printf ("%s %04x\n",__FUNCTION__, cmd->data[i]);
    }
	GPIO_SET =1 <<CHPSEL;
	GPIO_SET =1 <<READ_PIN;
	set_pin_output(START_FIFO);
	for(i=0;i<3; i++)
		GPIO_SET = 1 << START_FIFO;
	GPIO_CLR = 1 << START_FIFO;
	return (0);
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

void send_word(int GPIOpin, unsigned short word_to_send) {

	int bit[16];
	int i = 0;
	int modulo;
	int quoziente;
	
	for (i=0; i<16; i++)
		bit[15-i] = ((word_to_send & 1<<i)>>i);

	GPIO_CLR = 1<<GPIOpin; //DOpening

	for (i=0; i<16; i++) {
		switch (bit[i]) {
			case 0:
				GPIO_CLR = 1<<GPIOpin;
				break;
			default :
				GPIO_SET = 1<<GPIOpin;
				break;
		}
		ciclo_clock();
	}

	GPIO_CLR = 1<<GPIOpin; //DClosure
}

void ciclo_clock() {
	GPIO_SET = 1<<CLK;
	GPIO_SET = 1<<CLK;
	GPIO_CLR = 1<<CLK;
}