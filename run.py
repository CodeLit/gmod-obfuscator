from files import format_path
import sys
from obfuscator import obf_folder
from collector import collect_folder
from settings import do_not_collect, do_not_obfuscate

inp_folder = format_path(sys.argv[1])
inp_folder = inp_folder.rstrip('/')
out_folder = inp_folder+'-public'

if not do_not_obfuscate:
    print('-------- [Obfuscating...] --------')
obf_folder(inp_folder, out_folder)

if not do_not_collect:
    print('-------- [Collecting...] --------')
    collect_folder(out_folder)

print('-------- [Done!] --------')
