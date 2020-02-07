#!/usr/bin/env python

import optparse
from OSC import *
from OSC import _readString, _readFloat, _readInt

ADDRESS = '192.168.0.110' # listening address of device
PORT = 10023 # listening and sending port of devices
points = 0
damage = 0
result = 0

listen_address = (ADDRESS, PORT)

# message1 = OSCMessage('/connection')
# message1 += ['start', 'stop', 2]
#
# message2 = OSCMessage('/game')
# message2 += [points, damage, 'start', 'stop']
#
# message3 = OSCMessage('/interaction')
# message3 += ['start', 'stop', result]

# bundle = OSCBundle()
# bundle.append("/print")
# bundle.append({'addr':"/print", 'args':["bundled messages:", 2]})
# bundle.setAddress("/*print")

print "\n#######Instantiating OSCStreamingServer:"

# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
	msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
	msg_string = "SERVER: Got '%s' from %s" % (msg_string, getUrlStr(source))
	print msg_string

	# send a reply to the client.
	msg = OSCMessage("/printed")
	msg.append(msg_string)
	return msg

def connection_handler(addr, tags, stuff, source):
	msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
	msg_string = "SERVER: Got '%s' from %s" % (msg_string, getUrlStr(source))
	print msg_string

	# send a reply to the client.
	msg = OSCMessage("/printed")
	msg.append(msg_string)
	return msg

def interaction_handler(addr, tags, stuff, source):
	msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
	msg_string = "SERVER: Got '%s' from %s" % (msg_string, getUrlStr(source))
	print msg_string

	# send a reply to the client.
	msg = OSCMessage("/printed")
	msg.append(msg_string)
	return msg

def game_handler(addr, tags, stuff, source):
	msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
	msg_string = "SERVER: Got '%s' from %s" % (msg_string, getUrlStr(source))
	print msg_string

	# send a reply to the client.
	msg = OSCMessage("/printed")
	msg.append(msg_string)
	return msg

# define a message-handler function for the server to call.
def info_handler(addr, tags, stuff, source):
	print "SERVER: Info ", addr

def default_handler(addr, tags, stuff, source):
	print "SERVER: No handler registered for ", addr
	return None

class DemoOSCStreamRequestHandler(OSCStreamRequestHandler):
	""" A basic OSC connection/stream handler. For each connection the
	server instantiates a new object of this type. A reference to the
	server is available under self.server but it must be payed attention
	to multi threading design guide lines to avoid corrupted data and
	race conditions (the shared variable in this example
	"""
	def setupAddressSpace(self):
		self.addMsgHandler("/exit", self.exit_handler)
		self.addMsgHandler("/print", printing_handler)
		self.addMsgHandler("/info", info_handler)
		self.addMsgHandler("/connection", connection_handler)
		self.addMsgHandler("/game", game_handler)
		self.addMsgHandler("/interaction", interaction_handler)
		self.addMsgHandler("default", default_handler)
		print "SERVER: Address space:"
		for addr in self.getOSCAddressSpace():
			print addr

	def exit_handler(self, addr, tags, stuff, source):
		print "SERVER: EXIT ", addr
		self.server.run = False
		return None

class DemoServer(OSCStreamingServerThreading):
	RequestHandlerClass = DemoOSCStreamRequestHandler
	def __init__(self, listen_address):
		OSCStreamingServerThreading.__init__(self, listen_address)
		self.run = True

s = DemoServer(listen_address)

print "#########Starting ", s
s.start()

# Instantiate OSCClient
print "#########Instantiating OSCStreamingClient:"
def printed_handler(addr, tags, stuff, source):
	print "CLIENT: Printed Handler: ", addr
def broadcast_handler(addr, tags, stuff, source):
	print "CLIENT: Broadcast Handler: ", addr

c = OSCStreamingClient()
c.connect(listen_address)
c.addMsgHandler("/printed", printed_handler)
c.addMsgHandler("/interaction", interaction_handler)
c.addMsgHandler("/game", game_handler)
c.addMsgHandler("/connection", connection_handler)
c.addMsgHandler("/broadcast", broadcast_handler)

# print "\n#####Sending Messages"
#
# for m in (message1,message2,message3):
# 	print "Sending: ", m
# 	c.sendOSC(m)
# 	time.sleep(0.1)

# print "\nThe next message's address will match both the '/print' and '/printed' handlers..."
# print "sending: ", blob
# c.sendOSC(blob)
# time.sleep(0.1)

# print "\nBundles can be given a timestamp.\nThe receiving server should 'hold' the bundle until its time has come"

# waitbundle = OSCBundle("/print")
# waitbundle.setTimeTag(time.time() + 5)
# waitbundle.append("Note how the (single-thread) server blocks while holding this bundle")

# print "Set timetag 5 s into the future"
# print "sending: ", waitbundle
# c.sendOSC(waitbundle)
# time.sleep(0.1)

# print "Recursing bundles, with timetags set to 10 s [25 s, 20 s, 10 s]"
# bb = OSCBundle("/print")
# bb.setTimeTag(time.time() + 1)

# b = OSCBundle("/print")
# b.setTimeTag(time.time() + 3)
# b.append("held for 3 sec")
# bb.append(b)

# b.clearData()
# b.setTimeTag(time.time() + 5)
# b.append("held for 5 sec")
# bb.append(b)

# b.clearData()
# b.setTimeTag(time.time() + 4)
# b.append("held for 4 sec")
# bb.append(b)
#
# print "sending: ", bb
# c.sendOSC(bb)
# time.sleep(0.1)

# try:
# 	# we let the server run autonomously for some seconds
# 	count = 3
# 	while s.run :
# 		time.sleep(1)
# 		# test broadcasting to all connected clients
# 		msg = OSCMessage("/broadcast")
# 		msg.append(count)
# 		s.broadcastToClients(msg)
#
# #		msg = OSCMessage("/print")
# #		msg.append(count)
# #		c.sendOSC(msg)
# 		count -= 1
# 		if count == 0:
# 			# send termination message (test context message handlers)
# 			msg = OSCMessage("/exit")
# 			c.sendOSC(msg)
#
# except KeyboardInterrupt:
# 	print "Interrupted."
#
# print "Closing client"
# c.close()
#
# print "Closing server"
# # make sure server receiving thread is scheduled before we close the server
# # so that it can recognize, that the client disconnected itself
# time.sleep(1)
# s.stop()

# print "Done. Closing!"
# sys.exit()
