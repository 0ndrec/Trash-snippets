from types import NoneType
import time
import subprocess
import argparse
import os

parser = argparse.ArgumentParser(
    description='Important: Before running this script, make sure that all connections on the development board are made correctly. Also make sure that all required libraries are installed correctly and do not conflict with any other software.')
parser.add_argument('--buzzer', type=int, default=None,
                    help='Buzzer pin number')
parser.add_argument('--led', type=int, default=None, help='LED pin number')
parser.add_argument('--target', type=str, help='Target IP or URL')
args = parser.parse_args()

os_type = os.name

if type(args.buzzer) is NoneType or type(args.led) is NoneType:
    pass
else:
    from gpiozero import Buzzer, LED
    bz_ = Buzzer(args.buzzer)
    led_ = LED(args.led)


def alert(os_type):
    if os_type == 'nt':
        subprocess.call('powershell [console]::beep(900,500)')
    else:
        try:
            bz_.beep(on_time=0.1, off_time=0.1, n=2)
            led_.led.blink(on_time=0.1, off_time=0.1, n=2)
        except:
            subprocess.call(["echo", "-en", "\007"])


while True:
    if subprocess.Popen(["ping", "-n", "1", args.target], stdout=subprocess.DEVNULL).wait() == 0:
        pass
    else:
        alert(os_type)
    time.sleep(5)
