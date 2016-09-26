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
unsigned int read_easy(void);
unsigned int trig(unsigned short pin);
void sendfile(FILE *fd);
void send_word(int GPIOpin, unsigned short word_to_send);

FILE *f;

int main(int argc, char **argv)
{  
  unsigned int buff;
  int count = 0;
  char name[20];
  
  int g,rep,i,j;
  cmd_std command;
  cmd_easy comm_e;
  unsigned short comando;
  char filename[48];
  FILE *fp;
  
  setup_io();
  set_pin_output(DLAY_CLK);
  set_pin_output(READ_PIN);
  set_pin_output(DTK);
  set_pin_output(CLK);
  set_pin_output(CHPSEL);
  set_pin_output(MOSI);
  set_pin_output(START_FIFO);
  INP_GPIO(MISO);
  
  GPIO_CLR = 1 << READ_PIN;
  GPIO_CLR = 1 << CHPSEL;
  send_word(MOSI, CMD_CLR);
  send_word(MOSI, CMD_CTRLWD);
  send_word(MOSI, CMD_RUN_DLY);
  GPIO_SET =1 <<CHPSEL;
  GPIO_SET =1 <<READ_PIN;
  
  // Set up gpi pointer for direct register access
  printf("input Conf file name : %s\n", argv[2]);
  fp=fopen(argv[2], "r");
  if(fp==NULL) {
	  fprintf(stderr, "Could not open file %s\n", filename);
	  return(-1);
  }
  sendfile(fp);
  fclose(fp);
  
  sleep(atoi(argv[1]));
  
  printf("input Conf file name : %s\n", argv[3]);
  fp=fopen(argv[3], "r");
  if(fp==NULL) {
	  fprintf(stderr, "Could not open file %s\n", filename);
	  return(-1);
  }
  sendfile(fp);
  fclose(fp);
  
  sprintf(name,"cTrigger_Counts");
  f=fopen(name,"a+");
  for (;;) {
	while(count < 1){
		buff=read_easy();
		fprintf (f,"%x\t",buff);
		printf ("%x\t",buff);
		count += 1; 
	}
	break;
  }
  fprintf(f,"\n");
  fclose(f);
  
  GPIO_CLR = 1 << READ_PIN;
  GPIO_CLR = 1 << CHPSEL;
  send_word(MOSI, CMD_CTRLWD);
  send_word(MOSI, CMD_DIAG_DLY);  
  GPIO_SET =1 <<CHPSEL;
  GPIO_SET =1 <<READ_PIN;
  
  return 0;

}


void set_pin_output(unsigned short pin)
{
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

void sendfile(FILE *fp) {
	int size=0;
	int i, j;
	unsigned short *buff, *temp;
	i = 0;
	buff = (unsigned short*) malloc(sizeof(unsigned short));
	while (!feof(fp)) {
		size=fscanf(fp, "%04x\n", &buff[i]);
		if(size ==0) {
			fprintf(stderr, "Could not read\n");
			return;
		}
		temp = realloc(buff, (2*i+1)*sizeof(unsigned short));
		if (temp != NULL)
			buff = temp;
		i += 1;
	}
  
	set_pin_output(READ_PIN);
	GPIO_CLR = 1 << READ_PIN;
	set_pin_output(CHPSEL);
	GPIO_CLR = 1 << CHPSEL;
	set_pin_output(MOSI);
	
	for(j=0; j<i;j+=1) {
		send_word(MOSI, buff[j]);
		//printf("line=%d buff=%04x\n",j, buff[j]);
	}
  
	GPIO_SET =1 <<CHPSEL;
	GPIO_SET =1 <<READ_PIN;
	free(buff);
	return;
}

unsigned int read_easy()
{
  int i;
  unsigned int buffer=0;
  unsigned int value;
  unsigned char pin_value ;

  set_pin_output(CHPSEL);
  set_pin_output(READ_PIN);
  set_pin_output(DTK);
  INP_GPIO(MISO);
  INP_GPIO(MISO);
  GPIO_SET = 1 << READ_PIN;
  GPIO_CLR = 1 << CHPSEL;
  GPIO_SET = 1 << DTK;
  GPIO_SET = 1 << DTK;
  GPIO_SET = 1 << DTK;
  GPIO_SET = 1 << DTK;
  GPIO_CLR = 1 << DTK;
  GPIO_CLR = 1 << CLK;
  GPIO_CLR = 1 << CLK;
  GPIO_CLR = 1 << CLK;
  for (i = 31; i>=0; i--)
    {
      value = GPIO_LEV;               // reading all 32 pins
      pin_value = ((value & (1 << MISO)) != 0); // get pin MISO value 
      buffer|=((pin_value&1)<<i);
      ciclo_clock();
    }
  GPIO_SET = 1 << CHPSEL;

  return(buffer);
}


void setup_io()
{
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

unsigned int trig(unsigned short pin)
{
  unsigned int value;
  unsigned char pin_value ;

  INP_GPIO(pin);
  //GPIO_CLR = 1 << CHPSEL;
    
  value = GPIO_LEV;               // reading all 32 pins
  pin_value = ((value & (1 << pin)) != 0); // get pin MISO value 
  //GPIO_SET = 1 << CHPSEL;
  return(pin_value);
}

void ciclo_clock() {
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_CLR = 1 << CLK;
}
