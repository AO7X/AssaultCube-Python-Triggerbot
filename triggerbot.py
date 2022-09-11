import time, keyboard, psutil
from pymeow import *


def enable_patch(proc):
    bytes_to_patch = [
        [0x4D9A81, b"\xE8\x3A\x6D\xF8\xFF"],
        [0x4D9A86, b"\x85\xC0"],
        [0x4D9A88, b"\x75\x13"],
        [0x4D9A8A, b"\x50"],
        [0x4D9A8B, b"\xA1\xF4\xF4\x50\x00"],
        [0x4D9A90, b"\xC6\x80\x50\x02\x00\x00\x00"],
        [0x4D9A97, b"\x58"],
        [0x4D9A98, b"\xE9\x05\x13\xF3\xFF"],
        [0x4D9A9D, b"\x50"],
        [0x4D9A9E, b"\xA1\xF4\xF4\x50\x00"],
        [0x4D9AA3, b"\xC6\x80\x50\x02\x00\x00\x01"],
        [0x4D9AAA, b"\x58"],
        [0x4D9AAB, b"\xE9\xF2\x12\xF3\xFF"],
        [0x40AD9D, b"\xE9\xDF\xEC\x0C\x00"],
    ]
    p = psutil.Process(proc["pid"])
    p.suspend()
    for i in range(len(bytes_to_patch)):
        patch_bytes(proc, bytes_to_patch[i][0], bytes_to_patch[i][1])
    p.resume()


def disable_patch(proc):
    p = psutil.Process(proc["pid"])
    p.suspend()
    patch_bytes(proc, 0x40AD9D, b"\xE8\x1E\x5A\x05\x00")
    p.resume()


def triggerbot(proc):
    can_shoot = read_int(proc, pointer_chain(proc, 0x50F4F4, [0x250], 4))
    shoot_addr = pointer_chain(proc, 0x50F4F4, [0x224], 4)
    if can_shoot:
        write_byte(proc, shoot_addr, 1)
    else:
        write_byte(proc, shoot_addr, 0)


def main():
    proc = process_by_name("ac_client.exe")
    cheat_enabled = False
    while True:
        if keyboard.is_pressed("END"):
            break
        if keyboard.is_pressed("F"):
            cheat_enabled = not cheat_enabled
            if cheat_enabled:
                print("Triggerbot enabled")
                enable_patch(proc)
            else:
                print("Triggerbot disabled")
                disable_patch(proc)
            time.sleep(0.25)
        if cheat_enabled:
            triggerbot(proc)
        time.sleep(0.001)


if __name__ == "__main__":
    main()
