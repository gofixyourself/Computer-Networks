#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUFLEN 512
#define PORT 9930

void diep(char *s)
{
	perror(s);
	exit(1);
}

int main(void)
{
	struct sockaddr_in socket_info, other_info;
	int my_socket, i, string_len = sizeof(other_info);
	char buf[BUFLEN];

	printf("Server started\n");

	if ((my_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
		diep("socket");

	memset((char *)&socket_info, 0, sizeof(socket_info));
	socket_info.sin_family = AF_INET;
	socket_info.sin_port = htons(PORT);
	socket_info.sin_addr.s_addr = htonl(INADDR_ANY);
	if (bind(my_socket, &socket_info, sizeof(socket_info)) == -1)
		diep("bind");

	while (1)
	{
		if (recvfrom(my_socket, buf, BUFLEN, 0, &other_info, &string_len) == -1)
			diep("recvfrom()");
		printf("Received packet from %s:%d\nData: %s\n\n",
				inet_ntoa(other_info.sin_addr), ntohs(other_info.sin_port), buf);
	}

	close(my_socket);
	return 0;
}
