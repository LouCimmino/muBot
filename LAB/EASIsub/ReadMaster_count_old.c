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

FILE *f;

int main(int argc, char **argv)
{  
  unsigned int buff;
  int count = 0;
  char name[20];
  
  
  setup_io();
  sprintf(name,"SlaveCounts");
  f=fopen(name,"a+");
  while(count < 4){
  	buff=read_easy();
  	fprintf (f,"%x\t",buff);
 	count += 1; 
  } 
  fprintf(f,"\n");
  fclose(f);
  return 0;

}


void set_pin_output(unsigned short pin)
{
  INP_GPIO(pin);
  OUT_GPIO(pin);
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
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  //GPIO_SET = 1 << CLK;
  //GPIO_SET = 1 << CLK;
  GPIO_CLR = 1 << CLK;

  for (i = 30; i>=0; i--)
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

void ciclo_clock() {
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_CLR = 1 << CLK;
}
