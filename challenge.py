from Crypto.Util import number
import socket, threading, subprocess
import argparse

def check_flag(guess):
	flag = open("flag", "r").read().strip()
	if flag == guess:
		return True
	else:
		return False

def allowed_command(cmd):
	whitelist = ["echo", "ls", "whoami"]
	blacklist = [";", "&", "|", "\"", "\\", "'", "$", "(", ")", "`", "<", ">>", "#", ".", "/"]

	for item in blacklist:
		if item in cmd:
			return False

	parts = cmd.split()
	if not parts or parts[0] not in whitelist:
		return False
	
	return True

def exec_commands(s):
	while True: 
		s.sendall(b"$ ")
		cmd = s.recv(1024).decode().strip()
		if cmd == 'exit':
			return
		if allowed_command(cmd):
			try:
				output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
			except subprocess.CalledProcessError as e:
				output = e.output
			s.sendall(output)
		else:
			s.sendall(b"Not allowed\n")


def server_respond(s):
	global FLAG

	s.sendall(b"Welcome to my echo chamber.");
	while True:
		s.sendall(b"\nCommands:\n\t1. Execute Commands\n\t2. Get Flag\n\t3. Make Guess\n>>")
		cmd = s.recv(1024).decode().strip()
		if cmd == "1":
			exec_commands(s)

		elif cmd == "2":
			p = number.getPrime(1024)
			q = number.getPrime(1024)
			e = 65537
			N = p * q

			cipher = pow(number.bytes_to_long(FLAG.encode('utf-8')), e, N)
			p, q = None, None
			s.sendall(f"Here is the Encrypted Flag:\n{(cipher, e, N)}\n".encode())

		elif cmd == "3":
			s.sendall(b"Make a guess:\n>>")
			guess = s.recv(1024).decode().strip()
			if (check_flag(guess)):
				s.sendall(f"Wow that was a great guess! You got it right!\n{FLAG=}\n".encode())
				break
			else:
				s.sendall(b"Wrong!\n")

	s.close()

with open("flag", "r") as file:
	FLAG = file.read().strip()
	file.close()
	
def main():
	parser = argparse.ArgumentParser(description="Run the server")
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
	
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen(1)
	print(f"Challenge Started\n{FLAG=}\n")
	print(f"Server listening on {HOST}:{PORT}")
	

	while True:
		try:
			sock, addr = server.accept()
			print(f"Connection from {addr}")
			threading.Thread(target=server_respond, args=(sock,)).start()
		except KeyboardInterrupt:
			print("Server shutting down.")
			server.close()
			break
		except Exception as e:
			print(f"An error occured: {e}")
			pass

if __name__ == "__main__":
	main()