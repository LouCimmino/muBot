#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int SCtoHEXSC(unsigned short *hexSC_EASI, unsigned short *SC_EASI){
  // ****************************************************************************
  // Funzione che converte il vettore di 456 bit dello SC, contenente solo 0 o 1,
  // in un vettore di 118 elementi, contenente 114 elementi dello SC + 4 per il comando
  // ****************************************************************************
  int i,offset;
  hexSC_EASI[0]=0x0;
  hexSC_EASI[1]=0x0;
  hexSC_EASI[2]=0xE;
  hexSC_EASI[3]=0x0; // Marcatore comando per la scheda a 16 bit

  for (i=0 ; i<114 ; i++){
    offset = i*4;
    hexSC_EASI[i+4]= SC_EASI[offset]*8 +
      SC_EASI[offset+1]*4 +
      SC_EASI[offset+2]*2 +
      SC_EASI[offset+3];
  }

  return 0;

}






int PRtoHEXPR(unsigned short *hexPR_EASI, unsigned short *PR_EASI){
  // ****************************************************************************
  // Funzione che converte il vettore di 456 bit dello SC, contenente solo 0 o 1,
  // in un vettore di 118 elementi, contenente 114 elementi dello SC + 4 per il comando
  // ****************************************************************************
  int i,offset;
  hexPR_EASI[0]=0x0;
  hexPR_EASI[1]=0x1;
  hexPR_EASI[2]=0x0;
  hexPR_EASI[3]=0x0; // Marcatore comando per la scheda a 16 bit

  for (i=0 ; i<40 ; i++){
    offset = i*4;
    hexPR_EASI[i+4]= PR_EASI[offset]*8 +
      PR_EASI[offset+1]*4 +
      PR_EASI[offset+2]*2 +
      PR_EASI[offset+3];
  }

  return 0;

}






int initSC_EASI (unsigned short *SC_EASI) {

  SC_EASI[0] = 1; // Enable 32 input 8 bit DACs
  SC_EASI[1] = 1; // 8 bit DAC ref.: ExtRef = 1
  SC_EASI[290] = 0; //Low gain preamp bias: weak bias =1
  SC_EASI[291] = 1; // Disable high gain preamp power pulsing mode: preamp on = 1
  SC_EASI[292] = 1; // Enable high gain preamp
  SC_EASI[293] = 1; // Disable low gain preamp power pulsing mode: preamp off = 0
  SC_EASI[294] = 1; // Enable low gain preamp
  SC_EASI[295] = 0; // High gain preamp compensation capacitances 295 -> 298
  SC_EASI[296] = 0; //
  SC_EASI[297] = 0; //
  SC_EASI[298] = 0; //
  //----- H.G.P.A.
  SC_EASI[299] = 0; // High gain preamp feedback capacitances 299 -> 302 (MSB -> LSB)
  SC_EASI[300] = 0; //
  SC_EASI[301] = 1; //
  SC_EASI[302] = 0;  //
  //-----
  SC_EASI[303] = 0; // Low gain preamp feedback capacitances 303 -> 306 (LSB -> MSB)
  SC_EASI[304] = 1; //
  SC_EASI[305] = 1; //
  SC_EASI[306] = 0; //
  SC_EASI[307] = 0; // Low gain preamp compensation capacitances 307 -> 310
  SC_EASI[308] = 0; //
  SC_EASI[309] = 0; //
  SC_EASI[310] = 0; //
  SC_EASI[375] = 1; // Disable low gain slow shaper power pulsing mode: slow shaper off = 0
  SC_EASI[376] = 1; // Enable low gain slow shaper
  SC_EASI[377] = 1; // low gain shaper time constant MSB
  SC_EASI[378] = 1; //
  SC_EASI[379] = 0; // low gain shaper time constant LSB
  SC_EASI[380] = 1; // Disable high gain slow shaper power pulsing mode: slow shaper off = 0
  SC_EASI[381] = 1; // Enable high gain slow shaper
  //----- H.G.S.S.
  SC_EASI[382] = 1; // high gain shaper time constant MSB
  SC_EASI[383] = 0; //
  SC_EASI[384] = 0; // high gain shaper time constant LSB
  //-----
  SC_EASI[385] = 1; // Disable fast shaper follower power pulsing mode: fast shaper on = 1
  SC_EASI[386] = 1; // Enable fast shaper
  SC_EASI[387] = 1; // Disable fast shaper power pulsing mode: fast shaper on = 1
  SC_EASI[388] = 1; // Disable track & hold power pulsing mode: T&H on = 1
  SC_EASI[389] = 1; // Enable track & hold
  SC_EASI[390] = 0; // Track & hold bias: weak = 1
  SC_EASI[391] = 1; // Enable discriminator
  SC_EASI[392] = 1; // Disable trigger discriminator power pulsing mode: discriminator on = 1
  SC_EASI[393] = 0; // select latched or direct output: direct out (trigger) = 0, latched = 1
  SC_EASI[436] = 1; // DAC slope: fine = 1, coarse = 0
  SC_EASI[437] = 1; // Disable DAC power pulsing mode: DAC on = 1
  SC_EASI[438] = 1; // Enable 10 DAC
  SC_EASI[439] = 1; // Disable bandgap power pulsing mode:bandgap on = 1
  SC_EASI[440] = 1; // Enable band gap
  SC_EASI[441] = 1; // Disable high gain OTA power pulsing mode
  SC_EASI[442] = 1; // Disable low gain OTA power pulsing mode
  SC_EASI[443] = 1; // Disable probe OTA power pulsing mode
  SC_EASI[444] = 1; // Disable LVDS receivers power pulsing mode
  SC_EASI[445] = 1; // Enable high gain OTA
  SC_EASI[446] = 1; // Enable low gain OTA
  SC_EASI[447] = 1; // Enable probe OTA
  SC_EASI[448] = 1; // Enable LVDS receivers
  SC_EASI[449] = 1; // Enable digital multiplexed output
  SC_EASI[450] = 0; // Enable digital OR32 output (ATTENZIONE :: ATTIVO BASSO) OR32 enabled = 0
  SC_EASI[451] = 0; // Enable 32 chn triggers output (ATTENZIONE :: ATTIVO BASSO) Triggers enabled = 0
  SC_EASI[452] = 0; // Not used!!!
  SC_EASI[453] = 0; // Not used!!!
  SC_EASI[454] = 0; // Not used!!!
  SC_EASI[455] = 0; // Not used!!!

  return 0;

}


int HGfeedbackSC_EASI(unsigned short *SC_EASI, unsigned short capValue) {
  // Imposta le capacità di feedback del HG Amp
  // il valore viene scritto un binario con notazione LSB -> MSB
  // il valore massimo di capacita' e' 0 (1.5 pF corrispondente a HG = 10) e rappresenta il minimo guadagno
  // il valore minimo di capacita' e' 14 (100 fF corrispondente a HG = 150) e rappresenta il massimo guadagno
  // il valore 15 e' da evitare perche' corrisponde a disaccoppiare tutte le capacita' e di fatto utilizzando capacita' parassite

  int modulo;
  int i;
  int quoziente;
  int temp[4];
  int offset;

  for(i=0;i<4;i++)
    temp[i]=0;

  modulo = 0;                //conversione da decimale a binario e memorizzazione in un vettore di 4 elementi che conterranno o 0 o 1
  quoziente = capValue;
  i = 0;
  offset = 299;

  while((quoziente!=0) && (i<4)){
    modulo = quoziente%2;
    quoziente = quoziente/2;
    temp[i] = modulo;
    i++;
  }
  for(i=0;i<4;i++) {
    //printf("----------------------vettore temp:%d\n",temp[i]); 
    SC_EASI[offset+i] = temp[3-i];
  }
  return 0;
}






int DACbiasSC_EASI(unsigned short *SC_EASI, unsigned SipmCh, int DAC8) {
  // La funzine imposta i bit relativi ai DAC di polarizzazione dei singoli canali
  // SipmCh ha valore tra 0 a 31 e corrisponde al SiPM che si desidera impostare
  // DAC8 ha valore tra 0 e 255 corrispondeti a circa 0 Volt e 4.5 V rispettivamente se ExtRef = 1
  // La funzione restituisce 0 se DAC8 >=0 e <=255 (nessun errore), altrimenti restituisce DAC8 (condizione di errore)
  // Se DAC8 < 0 allora il DAC = 0, se DAC8 > 255 allora il DAC = 255

  int modulo;
  int i;
  int quoziente;
  int temp[8];
  int offset;
  int errorDAC;


  for(i=0;i<8;i++)
    temp[i]=0;

  modulo = 0;                //conversione da decimale a binario e memorizzazione in un vettore di 8 elementi che conterranno o 0 o 1
  quoziente = DAC8;
  i = 0;
  offset = SipmCh*9 + 2;
  errorDAC = 0;
  if (DAC8 < 0) {
    errorDAC = DAC8;
    DAC8 = 0;
  }
  if (DAC8 > 255) {
    errorDAC = DAC8;
    DAC8 = 255;
  }
  
  while((quoziente!=0) && (i<8)){
    modulo = quoziente%2;
    quoziente = quoziente/2;
    temp[i] = modulo;
    i++;
  }
  for(i=0;i<8;i++) {
	SC_EASI[offset+i] = temp[i];
  }
  
  return errorDAC;
}






int DACswitchSC_EASI(unsigned short *SC_EASI, unsigned SipmCh, int DACsw) {
  // La funzione accende o spegne il DAC di polarizzazione dei singoli canali
  // SipmCh ha valore tra 0 a 31 e corrisponde al SiPM che si desidera impostare
  // Se DACsw = 0 allora il DAC e'spento ( se DAC8 = 1 allora il DAC e' acceso

  int offset=0;

  offset = SipmCh*9 + 2;
  SC_EASI[offset+8] = DACsw;
   
  return 0;
}






int PAMPdisSC_EASI(unsigned short *SC_EASI, unsigned SipmCh, int disable) {
  SC_EASI[311 + 2*SipmCh] = disable;
}






int TCAPenblSC_EASI(unsigned short *SC_EASI, unsigned SipmCh, int enable) {
  SC_EASI[312 + 2*SipmCh] = enable;
}






int HGtimecSC_EASI(unsigned short *SC_EASI, int timec) {
  // Imposta il peaking time del HG shapper
  // timec = 1 -> 7 (peaking time rispettivamente 25 ns -> 175 ns : step 25 ns)
  // il valore viene scritto un binario con notazione MSB -> LSB

  int modulo;
  int i;
  int quoziente;
  int temp[3];
  int offset;

  for(i=0;i<3;i++)
    temp[i]=0;

  modulo = 0;                //conversione da decimale a binario e memorizzazione in un vettore di 8 elementi che conterranno o 0 o 1
  quoziente = timec;
  i = 0;
  offset = 382;

  while((quoziente!=0) && (i<3)){
    modulo = quoziente%2;
    quoziente = quoziente/2;
    temp[i] = modulo;
    i++;
  }
  for(i=0;i<3;i++) {
    // printf("----------------------vettore temp:%d\n",temp[i]);
    SC_EASI[offset+i] = temp[i];
  }
  // printf("------ dac_value = %d\n",DAC_Value);
  return 0;
}






int DISCRmaskSC_EASI(unsigned short *SC_EASI, unsigned SipmCh, int enable) {
  // il canale e' mascherato se enable = 0

  SC_EASI[394 + SipmCh] = enable;
}






int DAC10thrsSC_EASI(unsigned short *SC_EASI, int DAC10) {
  // Imposta il DAC a 10 bit della soglia dei discriminatori.
  // DAC10 compreso tra 0 e 0 e 1023 corrispondenti a soglie 1.1 V a 2.4 V : step 1.3 mV
  // il valore viene scritto un binario con notazione LSB -> MSB

  int modulo;
  int i;
  int quoziente;
  int temp[10];
  int offset;
  int errorDAC;


  for(i=0;i<10;i++)
    temp[i]=0;

  modulo = 0;                //conversione da decimale a binario e memorizzazione in un vettore di 8 elementi che conterranno o 0 o 1
  quoziente = DAC10;
  i = 0;
  offset = 426;
  errorDAC = 0;
  if (DAC10 < 0) {
    errorDAC = DAC10;
    DAC10 = 0;
  }
  if (DAC10 > 1023) {
    errorDAC = DAC10;
    DAC10 = 1023;
  }

  while((quoziente!=0) && (i<10)){
    modulo = quoziente%2;
    quoziente = quoziente/2;
    temp[i] = modulo;
    i++;
  }
  for(i=0;i<10;i++) {
    // printf("----------------------vettore temp:%d\n",temp[i]);
    SC_EASI[offset+i] = temp[i];
  }
  // printf("------ dac_value = %d\n",DAC_Value);
  return errorDAC;
}






int setPR_EASI(unsigned short *PR_EASI, unsigned SipmCh, unsigned short signal) {

  int i;
  int offset;

  if (signal == 0) offset = SipmCh*2; // caso Out_PA_HG
  else if (signal == 1) offset = 1 + SipmCh*2; // caso Out_PA_LG
  else if (signal == 2) offset = 64 + SipmCh*2; // caso Out_SS_HG
  else if (signal == 3) offset = 65 + SipmCh*2; // caso Out_SS_LG
  else if (signal == 4) offset = 128 + SipmCh; // caso Out_FS
  
  if (signal != 9) PR_EASI[offset] = 1; // se non voglio il probe metto 9


  return 0;
}

int ReverseSC_EASI(unsigned short *SC_EASI, unsigned short *ReversedSC_EASI) {
  int i;
  for (i=0; i<456; i++) {
	ReversedSC_EASI[i]= SC_EASI[455-i];
	printf("%d",SC_EASI[i]);
  }
  printf("\n");
  return 0;
}






int ReversePR_EASI(unsigned short *PR_EASI, unsigned short *ReversedPR_EASI) {
  int i;
  for (i=0; i<160; i++) {
	ReversedPR_EASI[i]= PR_EASI[159-i];
	printf("%d",PR_EASI[i]);
  }
  printf("\n");
  return 0;
}

