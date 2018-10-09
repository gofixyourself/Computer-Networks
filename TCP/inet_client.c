#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <time.h>

#define SOCKETID "filesocket"
#define BUFFSIZE 1250
#define MSGSIZE 5000
#define PORT 8079
#define SERVIP "127.0.0.1"

int main (void)
{
	char* buffer;
	struct sockaddr_in servname;

	buffer = malloc((MSGSIZE + 5)*sizeof(char));

	int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (sock < 0)
	{
		perror("Couldn't allocate socket!");
		return -1;
	}

	servname.sin_family = AF_INET;
	servname.sin_port = htons(PORT);
	if (inet_aton(SERVIP, &servname.sin_addr) == 0)
	{
		fprintf(stderr, "inet_aton() failed\n");
		exit(1);
	}

	if (connect(sock, (struct sockaddr *)&servname, sizeof(servname)) < 0)
	{
		printf("Connect failed \n");
		return 1;
	}

	while(strlen(buffer) < MSGSIZE)
		strcat(buffer, "cat");

	buffer[MSGSIZE] = 0;

	char* pointer = buffer;
	while (pointer - buffer < MSGSIZE)
	{
		printf("%p %p\n", (void*)pointer, (void*)buffer);
		int stat = send(sock, pointer, BUFFSIZE, 0);
		printf("stat: %d\n", stat);
		pointer += BUFFSIZE;
		sleep(1);
	}

	close(sock);
	return 0;
}
