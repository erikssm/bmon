#!/usr/bin/env python

import pynotify
import socket
import sys
import signal
import time

class Battery:
    'class description'

    def __init__(self, status_string):
        self.percentage = 0
        self.charging = False

        charge_lines = [line for line in status_string.split('\n') if "Battery Power" in line]
        if len(charge_lines) < 1:
            self.charging = True

        percent_lines = [line for line in status_string.split('\n') if "InternalBattery" in line]
        if len(percent_lines) < 1:
            return

        try:
            pct_text = percent_lines[0].split("\t")[1].split(";")[0].replace( "%", "" ).replace( " ", "" )
            self.percentage = int( pct_text )
        except:
            self.percentage = 0

    def status(self):
        return "percent: %s charging: %s" % (str(self.percentage), str(self.charging))

def log(s):
    # print s
    return

    #f = open('/tmp/bm-log.txt', 'a')
    #f.write( "%s\n" % str( s ) )
    #f.close();

def signal_handler(signal, frame):
    log('exiting..')
    sys.exit(0)

def notification( caption, msg ):
    # notification-message-im, dialog-information, dialog-warning, dialog-error
    pynotify.Notification(
        caption,
        msg,
        "dialog-warning"
    ).show()

def bm_server():
    if not pynotify.init("icon-summary-body"):
        log( "failed to init pynotify" )
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
                server_address = ('192.168.0.106', 3333)
                log( 'starting udp server on %s port %s' % server_address )
                sock.bind(server_address)

                while True:
                    data, address = sock.recvfrom(4096)
                    if data:
                        #print "received '%s' from %s" % ( data, str(address) )
                        batt = Battery( data )
                        pct = getattr( batt, 'percentage', 0 )
                        charging = getattr( batt, 'charging', False )
                        if (pct > 40 and not charging) or (charging and pct < 90):
                            continue

                        ip, port = address
                        notification(
                            "Battery monitor",
                            "battery percent: %s%% charging: %s" % (
                                str( pct ),
                                str( charging )
                            )
                        )
                        #sent = sock.sendto(data, address)

        except Exception as ex:
            log( "error: %s" % str( ex ) )
            log( "restarting in 15 sec.." )
            time.sleep( 15 )

        finally:
            sock.close()

def test():
    src = "Now drawing from 'Battery Power'\n -InternalBattery-0 (id=1234123)	94%; discharging; 3:25 remaining present: true"
    batt = Battery(src)
    print "battery: %d%%" % getattr( batt, 'percentage', 0 )

if __name__ == "__main__":
    bm_server()
    # test()
