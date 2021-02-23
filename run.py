import sys
from obfuscator import obf_folder

inp_folder = sys.argv[1]
out_folder = inp_folder+'-public'

obf_folder(inp_folder, out_folder)
