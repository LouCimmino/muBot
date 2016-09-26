#define MISO 9
#define MOSI 10
#define CHPSEL 7
#define READ_PIN 25
#define START_FIFO 18

#define RST 8
#define CLK 11
#define DLAY_CLK 4
#define ACK 23
#define FIFO_READY 24
#define DTK 17
#define TRG_IRQ 22

// Command words
#define CMD_CLR 0x000D
#define CMD_CTRLWD 0x000E
#define CMD_RSTFIFO 0x000F
#define CMD_MUX0 0x0001
#define CMD_MUX1 0x0002
#define CMD_MUX2 0x0003
#define CMD_MUX3 0x0004
#define CMD_MUX4 0x0005
#define CMD_EASY 0x000B

#define CMD_RUN 0x0001
#define CMD_DIAG 0x0000
#define CMD_RUN_DLY 0x0003
#define CMD_DIAG_DLY 0x0002

#define CMD_READ 0x00C0 //rimodula per indirizzo scheda
#define CMD_RST_RR 0x0160 //rimodula per indirizzo scheda
#define CMD_RST_PR 0x0240 //rimodula per indirizzo scheda
#define CMD_RST_SCR 0x0260 //rimodila per indirizzo scheda

#define FUCKTRIG 0x8220 //Fake Trigger per procedura PIEDISTALLI

typedef struct command_std 
{
  unsigned short cmd;
  unsigned short data;
}cmd_std;

typedef struct command_easyrock 
{
  unsigned short cmd;
  unsigned short *data;
}cmd_easy;

