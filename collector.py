from os import walk
from pathlib import Path

from files import format_path
from LuaObfuscator.stringstripper import strip_comments, strip_multiline_comments
from settings import sh_common_file, sv_common_file, cl_common_file, get_common_file, drm_debug, collect_file_name

output = ''


def is_collectable_file(file_path):
    file_path = Path(str(file_path))
    return file_path.suffix == '.lua' and file_path.name not in [cl_common_file, sv_common_file, sh_common_file, collect_file_name]


# Собирает содержимое папки в три файлика
def collect_into_three_files(folder_path):
    global output
    for (_, _, files) in walk(str(folder_path)):
        for f in sorted(files):
            f_path = Path(folder_path) / f
            if not is_collectable_file(f_path):
                continue
            data = f_path.read_text(encoding='utf-8-sig')  # Новые данные
            # Заменяем все ентеры на пробелы
            data, _ = strip_comments(data)
            data, _ = strip_multiline_comments(data)
            data = data.replace('\n', ' ')
            # Старые данные
            old_data = ''
            common_file_path = Path(folder_path) / get_common_file(f_path.name)
            if common_file_path.exists():
                old_data = common_file_path.read_text(encoding='utf-8-sig')
            common_file_path.write_text(
                old_data + ' ' + data, encoding='utf-8-sig')
            if drm_debug:
                output += 'Перемещён файл ' + \
                    format_path(f_path) + ' --> ' + \
                    format_path(common_file_path) + '\n'
            Path(f_path).unlink()
        break


# Собирает все файлы в папке в один, возвращает его
def collect_folder(path, force=False):
    global output
    path = Path(path)
    collect_file_path = Path(path) / collect_file_name
    cl_common_path = Path(path) / cl_common_file
    sv_common_path = Path(path) / sv_common_file
    sh_common_path = Path(path) / sh_common_file
    b_collect = collect_file_path.exists()
    # Удаляем сообщающий файлик
    if b_collect:
        collect_file_path.unlink()
        # Замещаем файлики
        cl_common_path.write_text('', encoding='utf-8-sig')
        sv_common_path.write_text('', encoding='utf-8-sig')
        sh_common_path.write_text('', encoding='utf-8-sig')
    for (_, dirs, files) in walk(str(path)):
        if b_collect or force:
            collect_into_three_files(path)
        for d in dirs:
            if d == '.git':
                continue
            d_path = Path(path)/d
            cl_common_in_path, sv_common_in_path, sh_common_in_path = collect_folder(
                str(d_path), b_collect or force)

            def proceed_common_file(fl, fl_in):
                global output
                if fl_in.exists():
                    if fl.exists():
                        old_content = fl.read_text(encoding='utf-8-sig')
                        content = fl_in.read_text(encoding='utf-8-sig')
                        fl.write_text(old_content + ' ' +
                                      content, encoding='utf-8-sig')
                        if drm_debug:
                            output += 'Перемещён главный файл ' + \
                                format_path(fl_in) + ' --> ' + \
                                format_path(fl) + '\n'
                        fl_in.unlink()
                        if not any(Path(d_path).iterdir()):
                            d_path.rmdir()
            proceed_common_file(cl_common_path, cl_common_in_path)
            proceed_common_file(sv_common_path, sv_common_in_path)
            proceed_common_file(sh_common_path, sh_common_in_path)
        return cl_common_path, sv_common_path, sh_common_path


def collect_addon(addon_name):
    global output
    output = ''
    addon_path = ADDONS_FOLDER_ENC / addon_name
    collect_folder(addon_path)
    return output+'ALL FILES ARE COLLECTED!'
