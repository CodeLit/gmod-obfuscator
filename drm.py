from pathlib import Path

from helpers.enl_lib.files import format_path, run_file
from drm.collector import collect_addon
from drm.obfuscator import obf_addon
from drm.settings import DRM_DIR, ADDONS_FOLDER_ENC, ADDONS_FOLDER, do_not_collect, drm_debug, \
    stop_scripts_time


def proceed_addon(addon_name, addon_url):
    pre_file = Path(DRM_DIR / 'pre.sh')

    commands = '''
        cd {0} || exit
        git init
        git remote add origin {1}
        git fetch origin
        git reset --hard origin/master
    '''.format(format_path(ADDONS_FOLDER / addon_name), addon_url)
    if drm_debug:
        commands += '\n sleep ' + stop_scripts_time
    pre_file.write_text(commands)
    output = run_file(pre_file, 30)
    if pre_file.exists() and not drm_debug:
        pre_file.unlink()

    output += obf_addon(addon_name)
    if not do_not_collect:
        output += collect_addon(addon_name)

    post_file = Path(DRM_DIR / 'post.sh')

    commands = '''
        cd {0} || exit
        git init
        git remote add origin {1}
        git branch encrypted
        git checkout encrypted
        git rm --cached -r .
        git add .
        git commit -m "autocommit `date +'%d-%m-%Y %H:%M:%S'`"
        git push origin encrypted
        # rm -r {0}
        echo DONE!
    '''.format(format_path(ADDONS_FOLDER_ENC/addon_name), addon_url)
    if drm_debug:
        commands += '\n sleep ' + stop_scripts_time
    # post_file.write_text(commands)
    # output += run_file(post_file, 30)
    if post_file.exists() and not drm_debug:
        post_file.unlink()

    return output


# proceed_addon('enl-base', 'git@github.com:Neowolk/enl-base.git')
