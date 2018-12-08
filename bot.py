import socket
import re
from requests import get

def envia_comando(sock, cmd):
	cmd += '\r\n'
	sock.send(cmd.encode('utf8'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('irc.rizon.net', 6667))

nick = 'TDCBot'
envia_comando(s, f'NICK {nick}')
envia_comando(s, f'USER {nick} {nick} {nick} :{nick}')

while True:
	msg = s.recv(2048).decode('utf8')
	print(msg)
	
	ping_match = re.match('PING :(.*)', msg)
	if ping_match:
		pong = ping_match.group(1)
		envia_comando(s, f'PONG :{pong}')
	
	url_match = re.match(f':([a-zA-Z]+)!.* PRIVMSG {nick} :.*(https?://[a-zA-Z0-9.]+)', msg)
	if url_match:
		req = get(url_match.group(2))
		title = re.search('<title>(.*)</title>', req.text)
		if title:
			envia_comando(s, f'PRIVMSG {url_match.group(1)} :{title.group(1)}')