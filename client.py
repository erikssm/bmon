#!/usr/bin/env python

import socket
import sys

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	server_address = ('ubox.local', 3333)
	
	#message = 'test message'
	message = "Now drawing from 'Battery Power'\n -InternalBattery-0 	 31%; discharging; 9:06 remaining present: true\n"
	if not sys.stdin.isatty():
		message = sys.stdin.read()
		
	try:
	    #print 'sending "%s"' % message
	    sent = sock.sendto(message, server_address)
	except Exception as ex:
		print "error: %s" % str( ex )
	finally:
	    sock.close()

if __name__ == "__main__":
    main()
