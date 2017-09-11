import sys
import subprocess
import os

import sublime
import sublime_plugin

def exec_cmd(cmd):
    popen_arg_list = {
        "shell": False,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE
    }

    subprocess.Popen(cmd, **popen_arg_list)

class OpenPathCommand(sublime_plugin.TextCommand):

    def description(self):
        tip = []
        for path, valid in self.paths:
            if not valid:
                tip += ['Cannot find '+path]
            else:
                tip += ['Open '+path]

        return '\n'.join(tip)

    def _open(self, path):

        sublime_text = self.settings.get('sublime_text', '')

        try:
            exec_cmd((sublime_text, path))
        except:
            if sys.platform.startswith('darwin'):
                exec_cmd(('open', path))
            elif os.name == 'nt':
                os.startfile(path)
            elif os.name == 'posix':
                exec_cmd(('xdg-open', path))

    def _get_path(self):

        current_file_name = self.view.file_name()
        print('current file name', current_file_name)

        project_path_var = self.settings.get('project_path_var', '')
        print('project path var', project_path_var)
        selection_limit = self.settings.get('selection_limit', 1)
        selections = []
        for region in self.view.sel():
            if region.empty():
                region = self.view.line(region)
            selections.extend(self.view.substr(region).split('\n'))
            if len(selections) >= selection_limit:
                break
        self.paths = []
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
                line = line[:-1]
            print('modified', line)

            self.paths.append((str(line), os.path.exists(line)))

    def is_enabled(self):
        self.settings = sublime.load_settings('sublime-open-path.sublime-settings')
        self._get_path()
        return any(map(lambda p: p[1], self.paths))

    def run(self, edit):
        for path, _ in self.paths:
            sublime.status_message('Opening '+path+'')
            self._open(path)
            print('Opened', path)
