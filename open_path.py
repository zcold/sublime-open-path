import sys
import subprocess
import os

import sublime
import sublime_plugin


class OpenPathCommand(sublime_plugin.TextCommand):

    def _open(self, path):
        settings = sublime.load_settings('open_path.sublime-settings')
        win_text_editor = settings.get('win_text_editor', '')
        osx_text_editor = settings.get('osx_text_editor', '')
        posix_text_editor = settings.get('posix_text_editor', '')

        if sys.platform.startswith('darwin'):
            open_text = lambda: subprocess.call(('open', path))
            if os.path.exists(osx_text_editor):
                open_text = lambda: subprocess.call((osx_text_editor, path))
            explorer = lambda: subprocess.call(('open', path))
        elif os.name == 'nt':
            open_text = lambda: os.startfile(path)
            if os.path.exists(win_text_editor):
                open_text = lambda: subprocess.call((win_text_editor, path))
            explorer = lambda: os.startfile(path)
        elif os.name == 'posix':
            open_text = lambda: subprocess.call(('xdg-open', path))
            if os.path.exists(posix_text_editor):
                open_text = lambda: subprocess.call((posix_text_editor, path))
            explorer = lambda: subprocess.call(('xdg-open', path))

        if os.path.isfile(path):
            open_text()
        else:
            explorer()

    def run(self, edit):
        current_file_name = self.view.file_name()
        print('current file name', current_file_name)

        project_path_var = sublime.load_settings('open_path.sublime-settings').get('project_path_var', '')
        print('project path var', project_path_var)

        selections = []
        for region in self.view.sel():
            if region.empty():
                region = self.view.line(region)
            selections.extend(self.view.substr(region).split('\n'))

        for line in selections:
            line = line.strip()
            print('line', line)
            if project_path_var in os.environ and not current_file_name.startswith(os.environ[project_path_var]):
                print('project var', os.environ[project_path_var])
                for e in os.environ:
                    if current_file_name.startswith(os.environ[e]):
                        line = line.replace('$'+project_path_var, '$'+e)
                        break
            for e in os.environ:
                if '$'+e+'/' in line:
                    line = line.replace('$'+e+'/', os.environ[e]+'/')
                    break
            if line.endswith(','):
                line = line[-1]
            print('modified', line)

            if os.path.exists(line):
                sublime.status_message('Opening `'+line+'`')
                self._open(line)
                print('Opened', line)
            else:
                sublime.status_message('Cannot find `'+line+'`')
