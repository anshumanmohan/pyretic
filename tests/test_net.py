
import pytest

from frenetic.netcore import *
from frenetic.netcore_lib import *

def make_header():
    return Header(switch=None, location=None, srcmac=None, dstmac=None, dltype=None,
                  vlan=None, vlan_pcp=None, srcip=None, dstip=None, protocol=None, srcport=None, dstport=None)


def test_Packet_strange_bug():
    assert Packet(None, None) is not None

    
def test_FixedInt_bitarray():
    i1 = FixedInt(32)("00000000000000000000000000000000")
    assert i1.to_bits().to01() == "00000000000000000000000000000000"
    
    i2 = FixedInt(32)(0)
    assert i2.to_bits().to01() == "00000000000000000000000000000000"

    assert i1 == i2
    
    i = FixedInt(16)(222)
    assert i.to_bits().to01() == "0000000011011110"

    assert i1 != i

def test_FixedInt_operators():
    i1 = FixedInt(16)(222)
    i2 = FixedInt(16)(111)
    i3 = i1 + i2
    
    assert i3.width == 16


@pytest.mark.xfail
def test_FixedInt_mismatch():
    i1 = FixedInt(16)(222)
    i2 = FixedInt(32)(111)

    i1 + i2


    
def test_Switch():
    assert repr(Switch(2)) == "<switch 2>"


# def test_Location():
#     x = Location("in", 70)

#     assert x.to_bits().to01() == "001000110"
#     assert x.replace(at="out").to_bits().to01() == "101000110"

def test_MAC():
    MAC("09-00-2B-00-00-04")
    MAC(FixedInt(48)(3))

@pytest.mark.xfail
def test_MAC_fail():
    MAC(FixedInt(32)(3))
    
@pytest.mark.xfail
def test_MAC_fail():
    MAC("09-00-2B-00-00")
def test_IP():
    IP("1.5.3.2")

@pytest.mark.xfail
def test_IP_fail():
    IP("1.3.3.5heytest")