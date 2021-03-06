from pyretic.lib.myeval import *
from pyretic.core.language import *

#some sample packets are below.
p1 = {"header":{"srcmac":"00:0a:95:9d:68:16", "dstmac":"00:0a:95:9d:68:18", "srcip":"192.0.0.1", "dstip":"192.0.0.2", "tos":56, "srcport":8008, "dstport":9900, "ethtype":0x0800, "protocol":"tcp"},"pktcount":40,"bytecount":4000}
p2 = {"header":{"srcmac":"00:0a:95:9d:78:16", "dstmac":"00:0a:9d:95:68:18", "srcip":"192.0.0.6", "dstip":"192.0.0.9", "tos":38, "srcport":8800, "dstport":9000, "ethtype":0x0800, "protocol":"tcp"},"pktcount":40,"bytecount":3000}

#some sample filters
#base cases:
f1 = match(srcip="192.0.0.1")          #p1 = pass. p2 = fail.
f2 = match(srcip="192.0.0.6")          #p2 = pass. p1 = fail.
f3 = match(dstmac='00:0a:9d:95:68:18') #p2 = pass. p1 = fail.
f4 = match(dstip='192.0.0.9')          #p2 = pass. p1 = fail.
#compound cases:
f5 = f1 | f3  #both pass
f6 = f3 & f2  #p2 = pass. p1 = fail
f7 = ~f2      #p1 = pass, p2 = fail
f8 = f2 & f1  #both fail. f8 is just a drop. try `print f8`!
f9 = f3 & f4  #p2 = pass, p1 = fail
f10 = identity

assert myEval(f1,p1) is p1 and myEval(f1,p2) is not p2
assert myEval(f2,p1) is not p1 and myEval(f2,p2) is p2
assert myEval(f3,p1) is not p1 and myEval(f3,p2) is p2
assert myEval(f4,p1) is not p1 and myEval(f4,p2) is p2

assert myEval(f5,p1) is p1 and myEval(f5,p2) is p2
assert myEval(f6,p1) is not p1 and myEval(f6,p2) is p2
assert myEval(f7,p1) is p1 and myEval(f7,p2) is not p2
assert myEval(f8,p1) is not p1 and myEval(f8,p2) is not p2
assert myEval(f9,p1) is not p1 and myEval(f9,p2) is p2
assert myEval(f10,p1) is p1 and myEval(f10,p2) is p2

assert myEval(f1,p2) == myEval(f2,p1) == myEval(f3,p1) == myEval(f4,p1) == set()
assert myEval(f6,p1) == myEval(f7,p2) == myEval(f8,p1) == myEval(f8,p2) == myEval(f9,p1) == set()
