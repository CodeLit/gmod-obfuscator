from files import format_path
import sys
from obfuscator import obf_folder

inp_folder = format_path(sys.argv[1])
inp_folder = inp_folder.rstrip('/')
out_folder = inp_folder+'-public'

obf_folder(inp_folder, out_folder)
