#!/usr/bin/python
# -*- coding: utf-8 -*-

# This tool expects data from the serial terminal in a format like this
# CFE> dm b8020000 160     
# b8020000: 36 00 00 00 42 72 6f 61 64 63 6f 6d 20 43 6f 72    6...Broadcom Cor
# b8020010: 70 6f 72 61 74 69 6f 00 76 65 72 2e 20 32 2e 30    poratio.ver. 2.0
# b8020020: 00 00 00 00 00 00 36 33 36 38 00 00 39 36 33 36    ......6368..9636
# b8020030: 38 4d 56 57 47 00 00 00 00 00 00 00 31 00 34 30    8MVWG.......1.40
# b8020040: 36 32 39 38 30 00 00 00 30 00 00 00 00 00 00 00    62980...0.......
# b8020050: 00 00 00 00 30 00 00 00 00 00 00 00 00 00 33 32    ....0.........32
# b8020060: 31 37 31 36 32 34 39 36 00 00 32 36 30 31 35 32    17162496..260152
# b8020070: 38 00 00 00 33 32 31 37 31 36 32 34 39 36 00 00    8...3217162496..
# b8020080: 31 34 36 31 34 35 32 00 00 00 32 00 00 00 00 00    1461452...2.....
# b8020090: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
# 
# *** command status = 0
# CFE> 

from __future__ import division

import re
from argparse import ArgumentParser

import serial
from serial import SerialBase
from tqdm import trange, tqdm

lineregex = re.compile(r"[0-9a-f]{8}:(?P<bytes>( [0-9a-f]\s?).*) {4}")


def skip_prompt(ser: SerialBase):
    while ser.read(1):
        pass


def wait_prompt(ser: SerialBase):
    tqdm.write("Waiting for a prompt...", end="")
    while True:
        ser.write(bytes.fromhex("03"))
        echo = b"^C\r\n"
        prompt = b"CFE>"

        line = ser.read(len(echo))
        skip = False

        if line == echo and ser.read(len(prompt)) == prompt:
            skip = True
        elif line == prompt:
            skip = True

        if skip:
            skip_prompt(ser)
            tqdm.write(" OK")
            return


def memreadblock(ser: SerialBase, addr, size):
    skip_prompt(ser)
    command = b"dm %x %d\r" % (addr, size)
    ser.write(command)
    buf = bytearray()
    m = False
    while not m:
        line = ser.readline()
        m = lineregex.match(line.strip().decode())
    while m:
        for chunk in m.group("bytes")[1:].split(' '):
            buf += bytearray.fromhex(chunk)
        line = ser.readline().strip().decode()
        m = lineregex.match(line)
    return buf


def memreadblock2file(ser: SerialBase, fd, addr, size):
    while True:
        buf = memreadblock(ser, addr, size)
        if len(buf) == size:
            break
        tqdm.write(f"Expected size {size}, got {len(buf)}")

    fd.write(buf)
    return len(buf)


def memread(ser: SerialBase, path, addr, size, block, prog):
    wait_prompt(ser)

    end = addr + size

    fd = None
    if path is not None:
        fd = open(path, "wb")

    iterable = range(addr, end, block)

    if prog:
        iterable = trange(
            addr, end, block,
            unit="chunk",
            desc="Dumping firmware",
        )

    for pos in iterable:
        block = min(block, end - pos)

        if path is not None:
            memreadblock2file(ser, fd, pos, block)
            fd.flush()
        else:
            tqdm.write(memreadblock(ser, pos, block), end="")

    if path is not None:
        fd.close()


def main():
    def int_parse(i): return int(i, 0)

    parser = ArgumentParser()
    parser.add_argument("--block", help="buffer block size", default="10240", type=int_parse)
    parser.add_argument("--serial", dest="serial", help="specify serial port", default="/dev/ttyUSB0", metavar="dev")
    parser.add_argument("--no-prog", dest="prog", action="store_false", default=True)
    parser.add_argument("--output", help="Path to read to")
    parser.add_argument("addr", help="mem address", type=int_parse)
    parser.add_argument("size", help="size to copy", metavar="bytes", type=int_parse)
    args = parser.parse_args()

    ser = serial.Serial(args.serial, 115200, timeout=1)
    memread(ser, args.output, args.addr, args.size, args.block, args.prog)


if __name__ == '__main__':
    main()
