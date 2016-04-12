#!/usr/bin/python
import binascii
from os import system, name # Its only for clear!

# In methods all input_data is named data, transitional data is ndata, and return is ret
# All transform methods begin with tf_name


def cls():
    system('cls' if name=='nt' else 'clear')

def print_help():
    ret = "HexFsck: A Conversion tool for the many hex formats...   @vvalien1\n"
    ret += "------------------------------------------------------------------\n"
    ret += "mshex: 41-41-10-00-ff-20-41-41       == \"\\x41\\x41\\x10\\x00\\xff\\x20\\x41\\x41\" \n"
    ret += "wshark: 41411000 ff 20 41 41         == \"\\x41\\x41\\x10\\x00\\xff\\x20\\x41\\x41\" \n"
    ret += "hexbyte: \\x41\\x41\\x10\\x00\\xff\\x20    == {65, 65, 16, 0, 255, 32 }\n"
    ret += "ints: 65 065 016 00 255 32 65 65     == \"\\x41\\x41\\x10\\x00\\xff\\x20\\x41\\x41\" \n"
    ret += "zhex: 0x410x410x10 or 0x41,0x41,0x10 == \"\\x41\\x41\\x10\" and \"\\x41\\x41\\x10\" \n"
    ret += "unicode: \"A\\xff\\x10\\x41\"             == \"\\x41\\x00\\xff\\x00\\x10\\x00\\x41\\x00\" \n"
    ret += "toms: \"\\x41\\x41\\x10\\x00\\xff\\x20\\x41\" == \"41-41-10-00-ff-20-41\" \n"
    print(ret)


def hex_format(data):
    ret = "\\x" + "\\x".join(x.encode("hex") for x in str(data))
    return ret

def data_replace(data, name):
    data = data.replace(name, "")
    data = data.replace(": ", "")
    data = data.replace(":", "")
    ret = data.replace("\"", "")
    return ret

def tf_toms(data):
    data = data_replace(data, "toms")
    data = data.decode("string-escape")
    data = binascii.hexlify(data)
    ndata = ""
    for i in range(2, len(data)+2, 2):
        ndata += data[i-2:i]
        if i == len(data): break
        else: ndata += "-"
    ret = "MShex = \"" + ndata + "\""
    print(ret)

# dumb unicode, but works!
def tf_unicode(data):
    data = data_replace(data, "unicode")
    data = data.decode("string-escape") #life saver!
    ndata = ""
    for i in range(len(data)):
        ndata += data[i] + "\x00"
    ret = hex_format(ndata)
    print("RealHex = \"%s\"" % ret)

# lazy = just subout "0x ,"
def tf_zhex(data):
    data = data_replace(data, "zhex")
    data = data.replace("0x", "")
    data = data.replace(",", "")
    data = data.replace(" ", "")
    ret = hex_format(binascii.unhexlify(data))
    print("RealHex = \"%s\"" % ret)

def tf_ints(data):
    data = data_replace(data, "ints")
    data = data.split(" ")
    ndata = ""
    for i in range(len(data)):
        ndata += chr(int(data[i]))
    ret = hex_format(ndata)
    print("RealHex = \"%s\"" % ret)

def tf_hexbyte(data):
    data = data_replace(data, "hexbyte")
    data = data.decode("string-escape") #life saver!
    ndata = ""
    for i in range(len(data)):
        ndata += "%s" % ord(data[i])
        if i == len(data)-1: break
        else: ndata += ", "
    ret = "byte[] int_array = {" + ndata + " };\n"
    ndata = "0x" + ", 0x".join(x.encode("hex") for x in str(data))
    ret += "byte[] hex_array = { " + ndata + " };"
    print(ret)
    
def tf_wshark(data):
    data = data_replace(data, "wshark")
    data = data.replace(" ", "")
    ret = hex_format(binascii.unhexlify(data))
    print("RealHex = \"%s\"" % ret)

def tf_mshex(data):
    data = data_replace(data, "mshex")
    data = data_replace(data, "-")
    ret = hex_format(binascii.unhexlify(data))
    print("RealHex = \"%s\"" % ret)

def parse_input(data):
    if data.startswith("?"):
        print_help()
    if data.startswith("clear"):
        cls()
    if data.startswith("mshex"):
        tf_mshex(data)
    if data.startswith("wshark"):
        tf_wshark(data)
    if data.startswith("hexbyte"):
        tf_hexbyte(data)
    if data.startswith("zhex"):
        tf_zhex(data)
    if data.startswith("ints"):
        tf_ints(data)
    if data.startswith("unicode"):
        tf_unicode(data)
    if data.startswith("toms"):
        tf_toms(data)

if __name__ == '__main__':
    print_help()
    while True:
        data = raw_input("hex:# ")
        parse_input(data)
