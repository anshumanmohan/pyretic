
import pytest

from frenetic.netcore import *
from frenetic.netcore_lib import *

h = Header(srcip=IP("1.2.3.4"))
p = Packet(h, None)

w = Wildcard(8)(bitarray("00000000"), bitarray("00000000"))
w2 = Wildcard(8)(bitarray("00000000"), bitarray("11111111"))

def test_Wildcard_match():
    assert w <= w
    assert w2 > w

def test_Wildcard_intersect():
    assert w & w2 == w2 & w

def test_MatchExact():
    return MatchExact(Switch)(10).match(Switch(10))


def test_Predicate_eval():
    assert eval(PredTop(), p)
    assert not eval(PredBottom(), p)
    assert eval(PredMatch("srcip", Wildcard(32)(IP("1.2.3.4").to_bits(),
                                                bitarray([False] * 32))), p)
    assert eval(PredMatch("srcip", IPWildcard("1.2.3.*")), p)
    assert eval(PredMatch("srcip", IPWildcard("1.2.3.4", "255.255.255.0")), p)

act = ActMod(frozendict({"srcport": FixedInt(16)(30)}))
pol = PredMatch("srcip", IPWildcard("1.2.3.*")) >> mod({"srcport": FixedInt(16)(30)})

def test_Action():
    assert not mod_packet(ActDrop(), p)
    assert mod_packet(act, p)[0].header["srcport"] == FixedInt(16)(30)
    assert len(mod_packet(act + act, p)) == 2
    with pytest.raises(KeyError):
        mod_packet(ActMod(frozendict({"srcip": None})), p)[0].header["srcip"]
    
def test_Policy():
    assert eval(pol, p) == act

lact = ModPolicy({"switch": Switch(10)})
l = PolLet("x", pol, "srcport", PredMatch("x", MatchExact(FixedInt(16))(30)) >> lact)

def test_Let():
    assert eval(l, p) == ActMod(frozendict({"switch": Switch(10)}))

ipol = PredMatch("switch", MatchExact(Switch)(10)) >> ModPolicy({"switch": Switch(25)})
cpol = l * ipol

def test_Composition():
    assert mod_packet(eval(cpol, p), p)[0].header["switch"] == Switch(25)

#
#

h2 = Header(srcip=IP("127.0.0.1"),
           srcport=FixedInt(16)(30),
           switch=Switch(14),
           dstport=FixedInt(16)(30))

p2 = Packet(h2, None)

hafter = Header(srcip=IP("127.0.0.1"),
                srcport=FixedInt(16)(30),
                switch=Switch(14),
                dstport=FixedInt(16)(30),
                outport=FixedInt(16)(30))

p5 = p2.replace(header=hafter)

ip = IPWildcard("1.2.3.*")
ip2 = IPWildcard("1.2.3.4", "255.255.255.0")

def test_IPWildcard():    
    assert ip == ip2
    assert ip <= ip2
    assert ip2 <= ip
    assert not ip != ip2
    
    assert ip2 == IPWildcard("1.2.3.8", "255.255.255.0")
    assert not IPWildcard("255.255.255.255").match(IP("255.255.255.252"))

def test_fwd():
    assert mod_packet(eval(fwd(30), p2), p2) == [p5]

def test_match_ips():
    assert eval(match("srcip", "127.0.0.1"), p2)
    assert eval(match("srcip", "127.*.*.*"), p2)
    assert eval(match("srcip", "*.*.*.1"), p2)
    assert eval(match("srcip", "127.0.0.1/32"), p2)
    assert eval(match("srcip", "127.0.0.255/24"), p2)
    assert not eval(match("srcip", "124.0.0.255/24"), p2)
    assert eval(match("srcip", "127.0.0.255/24"), p2)
    assert eval(match("srcip", ("127.0.0.255", 24)), p2)
    assert eval(match("srcip", ("127.0.0.255", "255.255.255.0")), p2)
    assert eval(match("srcip", "127.0.0.255/255.255.255.0"), p2)

    assert eval(match_missing("meow"), p2)
    assert not eval(match_missing("srcip"), p2)
    
def test_match_ints():    
    assert eval(match("dstport", 30), p2)
    assert not eval(match("dstport", 31), p2)
    assert not eval(match("dstport", "1000100010001000"), p2)
    assert not eval(match("dstport", "???????????????1"), p2)
    assert     eval(match("dstport", "????????????????"), p2)
    assert     eval(match("dstport", "???????????1111?"), p2)
    assert     eval(match("dstport", "0000000000011110"), p2)
    
# def test_match_locations():
#     pmod = mod_packet(fwd(30), p)[0]
#     assert eval(match("location", ("out", 30)), pmod)
#     assert not eval(match("location", ("out", 31)), pmod)
#     assert not eval(match("location", ("in", 30)), pmod)
#     assert eval(match("location", "100011110"), pmod)
    