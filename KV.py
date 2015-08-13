# source - jonathan matthew
#	   aka moch

import socket
import random
import struct
import select

KV_OP_CREATE = 0
KV_OP_CREATED = 1
KV_OP_REQUEST = 2
KV_OP_VALUE = 3
KV_OP_NOVALUE = 4
KV_OP_DELETE = 5
KV_OP_DELETED = 6
KV_OP_SYNC = 7

class KV(object):
    def __init__(self, addr, retries=10):
	self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.socket.connect((addr, 1080))
	self.retries = retries

    def __cookie(self):
	possible = "0123456789abcdefghijlkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	return ''.join([possible[random.randrange(0, 
	    len(possible))] for x in xrange(32)])

    def __reply(self, length):
	fd = self.socket.fileno()
	(rout, wout, eout) = select.select([fd], [], [fd], 0.1)
	if fd in rout:
	    return self.socket.recv(length)
	else:
	    return ''

    def put(self, payload):
	c = self.__cookie()
	req = struct.pack("> B x H 32s %ds" % (len(payload)), 
		KV_OP_CREATE, len(payload), c, payload)

	for r in xrange(self.retries):
	    try:
		self.socket.send(req)

		reply = self.__reply(4 + 32 + 32)
		if reply is None:
		    continue

		if len(reply) != 4 + 32 + 32:
		    continue

		(opcode, rlen, rcookie, key) = struct.unpack("> B x H 32s 32s", reply)
		if opcode != KV_OP_CREATED or rcookie != c:
		    continue

		return key
	    except Exception, e:
		if r < self.retries-1:
		    continue
		raise

	return None

    def get(self, key):
	req = struct.pack("> B x H 32s", KV_OP_REQUEST, 0, key)
	for r in xrange(self.retries):
	    try:
		self.socket.send(req)

		reply = self.__reply(65536)
		if len(reply) < 4 + 32:
		    continue

		(opcode, length, rkey) = struct.unpack("> B x H 32s", reply[0:4+32])
		if key != rkey:
		    continue

		if opcode == KV_OP_NOVALUE:
		    return ""

		(opcode, length, rkey, payload) = struct.unpack(">B x H 32s %ds" % length, reply)
		return payload
	    except Exception, e:
		if r < self.retries-1:
		    continue
		raise

	return None

    def rm(self, key):
	req = struct.pack("> B x H 32s", KV_OP_DELETE, 0, key)
	for r in xrange(self.retries):
	    try:
		self.socket.send(req)

		reply = self.__reply(4 + 32)
		if len(reply ) != 4 + 32:
		    continue

		(opcode, length, rkey) = struct.unpack("> B x H 32s", reply)
		if key != rkey:
		    continue

		if opcode != KV_OP_DELETED:
		    continue
		return 1
	    except Exception, e:
		if r < self.retries-1:
		    continue
		raise
	return 0
