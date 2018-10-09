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
#define PORT 8079

int main (void)
{
	struct sockaddr_in servname, recvname;
	struct sockaddr_storage servstore;
	char buffer[BUFFSIZE + 5];
	char result[6 * BUFFSIZE];

	// Allocation of socket
	int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	int nsock = 0;
	if (sock < 0)
	{
		perror("Couldn't allocate socket!\n");
		return -1;
	}

	// Filling in servname struct:
	memset((char *)&servname, 0, sizeof(servname));
	servname.sin_family = AF_INET;
	servname.sin_port = htons(PORT);
	servname.sin_addr.s_addr = htonl(INADDR_ANY);


	// Binding struct to socket:
	if (bind(sock, &servname, sizeof(servname))<0)
	{
		perror("Couldn't bind!\n");
		return -1;
	}
	listen(sock, 3);

	// Receiving from client:
	nsock = accept(sock, (struct sockaddr *)NULL, NULL);

	while(1)
	{
		int bytes = recv(nsock, buffer, BUFFSIZE, 0);
		if (bytes < 0)
		{
			perror("Couldn't receive!\n");
			return -1;
		}

		if (bytes == 0)
		{
			printf("Rx:%s\n", result);
			return 1;
		}

		strcat(result, buffer);
		printf("Rx(%d):\n", bytes);
	}

	close(sock);
}
