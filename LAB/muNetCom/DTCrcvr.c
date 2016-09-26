#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>

FILE *f;

int main (void)
{
        void *context_s = zmq_ctx_new ();
        void *sender = zmq_socket (context_s, ZMQ_REP);
        int rc = zmq_bind (sender, "tcp://0.0.0.0:5000");
        int count = 0;
        char buffer[10];
	char name[20];
	sprintf(name, "/home/DatiTB/DTC/DTC.txt");
	f = fopen(name, "w");
	strcpy(buffer, "");
	while (count < 2) {
		zmq_recv (sender, buffer, 10, 0);
		//printf ("Received %s\n", buffer);
		if (count == 0) fprintf(f, "$PEDS\t%s\n", buffer);
		if (count == 1) fprintf(f, "$EVTS\t%s\n", buffer);
		zmq_send (sender, strcat(buffer, "Ok"), 10, 0);
		count = count+1;
    	}
	fclose(f);
	sleep(1);
    	return 0;
}

