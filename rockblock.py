import serial
ser = serial.Serial('/dev/ttyUSB0',19200, timeout = 10)

rb_signal = 'AT+CSQ\r' #checks sattelite signal 0-5 (5 is best)
rb_test = 'AT\r' #checks rockblock status
rb_write_to_buffer = 'AT+SBDWT=hello world\r' #writes a message to the rockblocks buffer
rb_attempt_sat_session = 'AT+SBDI\r' #attempts a sattelite session

def parse_response(message,command):
	print(message)
	response = message.split()


	if command == rb_signal:
		if len(response) > 1:
			rb_response = str(response[1]).split(':')[1].split("'")[0]
			rb_response = int(rb_response)
			print('signal strength: ' + str(rb_response))
			if rb_response > 0:
				print('beam me up scotty! we got a signal!')

	if command == rb_write_to_buffer:
		if len(response) > 1:
			rb_response = str(response[2]).split("'")[1]
			print(rb_response)
	print(response)
def rockblock_action(cmd):
	global ser

	ser.write(cmd.encode())
	msg = ser.read(1000)


	if cmd == rb_write_to_buffer:
		print('Writing message to Rock Block MO buffer...')
		command1 = rb_write_to_buffer
		parse_response(msg,command1)
	if cmd == rb_signal:
		print('Looking for GSS reception...')
		command1 = rb_signal
		parse_response(msg,command1)

rockblock_action(rb_signal)
rockblock_action(rb_write_to_buffer)
