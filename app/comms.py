from PyQt5.QtCore import QObject
import logging
import logging.handlers
import argparse
import sys
import os
import time
from bluetooth import *

class Comms(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self)
		self.response="msg:Press Get Data,Press Get Data"


	def main(self):
		# Setup logging
		#setup_logging()

		# We need to wait until Bluetooth init is done
		time.sleep(10)

		# Make device visible
		os.system("hciconfig hci0 piscan")

		# Create a new server socket using RFCOMM protocol
		server_sock = BluetoothSocket(RFCOMM)
		# Bind to any port
		server_sock.bind(("", PORT_ANY))
		# Start listening
		server_sock.listen(1)

		# Get the port the server socket is listening
		port = server_sock.getsockname()[1]

		# The service UUID to advertise
		uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

		# Start advertising the service
		advertise_service(server_sock, "RaspiBtSrv",
						   service_id=uuid,
						   service_classes=[uuid, SERIAL_PORT_CLASS],
						   profiles=[SERIAL_PORT_PROFILE])


		# Main Bluetooth server loop
		while True:
			i=1
			print ("Waiting for connection on RFCOMM channel %d" % port)

			try:
				client_sock = None
				
				# This will block until we get a new connection
				client_sock, client_info = server_sock.accept()
				print("Accepted connection from ", client_info)
				
				#Read the data sent by the client
				data = client_sock.recv(1024)
				#if len(data) == 0:
					 #break

			   # print "Received [%s]" % data

				# Handle the request
				#if data == "getop":
				   # response = "op:%s" % ",".join(operations)




				#----------------- replace numbers 1 and 3 with variables containing width ----------#  
				# if data == "ping":
				# 	self.response = "msg:1,3"
				#-------------------------------------------------------------------------------------#


					
			   # elif data == "example":
				   # response = "msg:This is an example"
				# Insert more here
			   # else:
				#	response = "msg:Not supported"
				# else:
				# 	self.response="msg:Press Get Data,Press Get Data"
				client_sock.send(response)
				print ("Sent [%s]" % response)
				

			except IOError:
				pass

			except KeyboardInterrupt:

				if client_sock is not None:
					client_sock.close()

				server_sock.close()

				print("Server going down")
				break

		