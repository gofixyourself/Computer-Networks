from smtplib import *
from operator import itemgetter
import argparse

parser = argparse.ArgumentParser(description='Send mail over SMTP')
parser.add_argument('dest', metavar='dest', type=str,
                    help='destination email')

parser.add_argument('acc', metavar='acc', type=str,
                    help='your email')

parser.add_argument('pswd', metavar='pswd', type=str,
                    help='password for your email')

parser.add_argument('msgfile', metavar='msgfile', type=str,
                    help='a file with messages')

parser.add_argument('keyword', metavar='keyword', type=str,
                    help='search keyword')

args = parser.parse_args()

sender = args.acc

message_file = open(args.msgfile, "r").read().split("\n")
messages = {i: message_file[i] for i in range(len(message_file))}
freq_table = [(i, message_file[i], message_file[i].count(args.keyword)) for i in range(len(message_file))]
print(messages, freq_table)
sorted_messages = sorted(freq_table, key=itemgetter(2))

for message in sorted_messages:
    if message[2] == 0:
        message = f"""From: gaben@valvesoftware.com
        To: To Person {args.dest}
        Subject: Message !

        {message}
        """

        smtp_obj = SMTP_SSL('smtp.yandex.ru', 465)
        smtp_obj.login(sender.split("@")[0], args.pswd)
        smtp_obj.sendmail(sender, args.dest, message)
        print("Successfully sent email")
