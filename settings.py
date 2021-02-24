from pathlib import Path

from files import format_path

obf_level = 2
do_not_collect = False
do_not_obfuscate = False

# Debug
drm_debug = False

# Пути
DRM_DIR = Path(__file__).parent.absolute()
OBF_DIR = DRM_DIR / 'LuaObfuscator'
PYTHON_CMD = 'py'
cmd_file_path = DRM_DIR / 'commands.sh'

ignored_files_start = '-- [do not obfuscate]'
ignored_folders = [
    format_path(Path('lua') / 'cyber-langs'),
    format_path(Path('lua') / 'cyber-external'),
]

cl_common_file = '__cl.lua'
sv_common_file = '__sv.lua'
sh_common_file = '___sh.lua'

collect_file_name = '__collectfolder__.lua'


def is_cl_file(f):
    return f == 'cl.lua' or '_cl.lua' in f


def is_sv_file(f):
    return f == 'sv.lua' or '_sv.lua' in f


def get_common_file(f):
    return is_cl_file(f) and cl_common_file or is_sv_file(f) and sv_common_file or sh_common_file
