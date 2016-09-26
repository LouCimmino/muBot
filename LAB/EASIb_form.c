#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "EASIdict.h"

  void main(int argc, char **argv) {
  FILE *f;

  unsigned short SC_EASI[456];
  unsigned short ReversedSC_EASI[456];
  unsigned short PR_EASI[160];
  unsigned short ReversedPR_EASI[160];
  unsigned short hexSC_EASI[120];
  unsigned short hexPR_EASI[44];
  int i = 0;
  int j = 0;
  int error;

  for (i=0; i<456; i++) SC_EASI[i]=0;
  for (i=0; i<160; i++) PR_EASI[i]=0;

  for (i=0; i<118; i++) hexSC_EASI[i]=0x0;
  for (i=0; i<44; i++) hexPR_EASI[i]=0x0;

  initSC_EASI(SC_EASI);
  //HGfeedbackSC_EASI(SC_EASI, 2);
  
//DAC8
for (i=0; i<32; i++) error = DACbiasSC_EASI(SC_EASI, i, 0);

  for (i=0; i<32; i++) DACswitchSC_EASI(SC_EASI, i, 1); // 1 = ON
  for (i=0; i<32; i++) PAMPdisSC_EASI(SC_EASI, i, 0); // 0 = enabled
  for (i=0; i<32; i++) TCAPenblSC_EASI(SC_EASI, i, 0); // 1 = cap test on
  
  HGtimecSC_EASI(SC_EASI, 6);
  for (i=0; i<32; i++) DISCRmaskSC_EASI(SC_EASI, i, 0); // 1 = nomask
  
//CHNL
DISCRmaskSC_EASI(SC_EASI, 31, 1);

  DAC10thrsSC_EASI(SC_EASI,855);
  setPR_EASI(PR_EASI, 12, 9);// con 9  il file di prob e' tutti 0 tranne il comando
  
  ReverseSC_EASI(SC_EASI, ReversedSC_EASI);
  ReversePR_EASI(PR_EASI, ReversedPR_EASI);

  SCtoHEXSC(hexSC_EASI, ReversedSC_EASI);
  PRtoHEXPR(hexPR_EASI, ReversedPR_EASI);  
  hexSC_EASI[118]=hexSC_EASI[119]=0;
  f = fopen("EASIconf/EASI_Slow_Control.txt", "w");
  
  for (i=0; i<120; i++) {
    if (i%4 == 0 && i !=0) fprintf(f, "\n");
	fprintf(f, "%x", hexSC_EASI[i]);
  }
  fclose(f);
  
  f = fopen("EASIconf/EASI_Probe.txt","w");
  for (i=0; i<44; i++) {
    if (i%4 == 0 && i!=0) fprintf(f, "\n");
    fprintf(f, "%x", hexPR_EASI[i]);
  }
  fclose(f);
  
}
