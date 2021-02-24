import os
import shutil
from os import walk
from pathlib import Path

from settings import PYTHON_CMD
from files import format_path, run_file
from settings import OBF_DIR, cmd_file_path, ignored_files_start, obf_level, do_not_obfuscate, drm_debug, ignored_folders, collect_file_name


def obf_folder(in_folder, out_folder):
    in_folder = Path(in_folder)
    out_folder = Path(out_folder)
    Path(out_folder).mkdir(parents=True, exist_ok=True)
    # СОЗДАЕМ ФАЙЛИК
    if Path(cmd_file_path).exists():
        Path(cmd_file_path).unlink()
    commands = ''
    # ЗАНОСИМ ТУДА КОМАНДЫ
    commands += '# bin/sh\n'
    commands += 'cd ' + format_path(OBF_DIR) + '|| exit\n'
    # Удаляем старую папку изнутри, и шифруем по новой
    for (_, dirs, _) in walk(str(out_folder)):
        for d in dirs:
            if d != '.git':
                shutil.rmtree(str(out_folder/d), ignore_errors=True)
    for (dirPath, _, _) in walk(str(in_folder)):
        folder_is_in_ignored = False
        for ignored in ignored_folders:
            if ignored in dirPath:
                folder_is_in_ignored = True
        for (_, _, files) in walk(dirPath):
            for file_name in files:
                file_path = format_path(Path(dirPath) / file_name)
                enc_file_path = file_path.replace(
                    format_path(in_folder), format_path(out_folder))
                encrypted_dir_path = format_path(dirPath).replace(
                    format_path(in_folder), format_path(out_folder))
                Path(encrypted_dir_path).mkdir(parents=True, exist_ok=True)
                _, file_extension = os.path.splitext(file_name)

                if file_extension == '.lua' and not do_not_obfuscate and not folder_is_in_ignored and not file_path.__contains__(collect_file_name):
                    fl_data = Path(file_path).read_text(encoding='utf-8-sig')
                    if fl_data.__contains__(ignored_files_start):
                        Path(enc_file_path).write_text(fl_data.replace(
                            ignored_files_start+'\n', ''), encoding='utf-8-sig')
                    else:
                        commands += 'echo ---------- OBF [' + file_path + \
                            '] TO LVL ' + \
                            str(obf_level) + '\n'
                        commands += PYTHON_CMD+' ' + '__main__.py' + ' --input ' + file_path \
                            + ' --output ' + enc_file_path + ' --level ' + str(obf_level) \
                            + ' --dontcopy --debug\n'
                else:
                    if '.git' not in file_path:
                        shutil.copy(file_path, enc_file_path)
            break

    # ЗАПУСКАЕМ ФАЙЛИК
    cmd_file = Path(cmd_file_path)
    # if drm_debug:
    #     commands += '\n sleep 1h'
    commands += '\n echo ------- All scripts is finished!'
    # commands += '\n sleep 1h'
    cmd_file.write_text(commands)
    output = run_file(cmd_file, 40)

    # УБИРАЕМ ЗА СОБОЙ
    if Path(cmd_file_path).exists() and not drm_debug:
        Path(cmd_file_path).unlink()
    return output
