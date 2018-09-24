#define SRV_IP "127.0.0.1"
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
	struct sockaddr_in other_info;
	int my_socket, string_len = sizeof(other_info);
	char buf[BUFLEN];

	if ((my_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
		diep("socket");

	memset((char *)&other_info, 0, sizeof(other_info));
	other_info.sin_family = AF_INET;
	other_info.sin_port = htons(PORT);

	if (inet_aton(SRV_IP, &other_info.sin_addr) == 0)
    {
		fprintf(stderr, "inet_aton() failed\n");
		exit(1);
	}

	printf("Input message: ");
	fgets(buf, BUFLEN, stdin);
	if (sendto(my_socket, buf, BUFLEN, 0, &other_info, string_len) == -1)
		diep("sendto()");

	close(my_socket);
	return 0;
}
