import serial
ser = serial.Serial('/dev/ttyUSB0',19200, timeout = 10)

rb_signal = 'AT+CSQ\r' #checks sattelite signal 0-5 (5 is best)
rb_test = 'AT\r' #checks rockblock status
rb_write_to_buffer = 'AT+SBDWT=hello world\r' #writes a message to the rockblocks buffer
rb_attempt_sat_session = 'AT+SBDI\r' #attempts a sattelite session
rb_read_message = 'AT+SBDRT\r'
rb_clear_mo_buffer = 'AT+SBDD0\r'
rb_check_buffer = 'AT+SBDS\r'
rb_test_read = 'AT+SBDTC\r'
rb_clear_all_buffers = 'AT+SBDD2\r'
def parse_response(message,command):
#	print(message)
	response = message.split()

	if command == rb_signal:
		if len(response) > 1:
			rb_response = str(response[1]).split(':')[1].split("'")[0]
			rb_response = int(rb_response)
			print('signal strength: ' + str(rb_response)+ '\n')
			if rb_response > 0:
				print('beam me up scotty! we got a signal!\n')
#				rockblock_action(rb_attempt_sat_session)
#				rockblock_action(rb_read_message)
	if command == rb_write_to_buffer:
		if len(response) > 1:
			rb_response = str(response[2]).split("'")[1]
			print(rb_response+ '\n')

	print(response)
def rockblock_action(cmd):
	global ser

	ser.write(cmd.encode())
	msg = ser.read(1000)
#	print(msg)

	if cmd == rb_write_to_buffer:
		print('Writing message to Rock Block MO buffer...\n')
		parse_response(msg,rb_write_to_buffer)

	if cmd == rb_signal:
		print('Looking for GSS reception...\n')
		parse_response(msg,rb_signal)

	if cmd == rb_attempt_sat_session:
		print('attempting sat session\n')
		parse_response(msg,rb_attempt_sat_session)

	if cmd == rb_read_message:
		print('reading message from buffer\n')
		parse_response(msg,rb_read_message)

	if cmd == rb_clear_mo_buffer:
		print('clearing MO buffer\n')
		parse_response(msg,rb_clear_mo_buffer)

	if cmd == rb_check_buffer:
		print('checking the buffer\n')
		parse_response(msg,rb_check_buffer)

	if cmd == rb_clear_all_buffers:
		print('clearing all buffers\n')

	if cmd == rb_test_read:
		print('test read\n')

rockblock_action(rb_signal)
rockblock_action(rb_write_to_buffer)
rockblock_action(rb_check_buffer)
rockblock_action(rb_test_read)
rockblock_action(rb_check_buffer)
rockblock_action(rb_read_message)
rockblock_action(rb_clear_mo_buffer)
rockblock_action(rb_check_buffer)
rockblock_action(rb_clear_all_buffers)
rockblock_action(rb_check_buffer)
