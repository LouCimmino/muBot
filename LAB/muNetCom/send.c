#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <stdlib.h>
int main (void)
{
    //  Socket to talk to clients
    void *context = zmq_ctx_new ();
    void *responder = zmq_socket (context, ZMQ_REQ);
    int rc = zmq_connect (responder, "tcp://192.168.77.14:5000");
    assert (rc == 0);
    int count = 0;
    while (count < 5) {
	char buffer [10];
	sprintf(buffer,"%d",count+1);
       	//zmq_recv (responder, buffer, 10, 0);
        //printf ("Received %s\n", buffer);
        zmq_send (responder, buffer, 5, 0);
	zmq_recv (responder, buffer, 10, 0);
	printf ("%s\n",buffer);
	count += 1;
    }
    return 0;
}
