import sublime
import sublime_plugin

import re

from ..settings import get_setting

class GenerateInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit, insert_point, files):
        self.edit         = edit
        self.insert_point = insert_point
        self.files        = files
        if len(files) == 1:
            self.interface = self.files[index][0][0]
            self.insert_interface(files[0][1])

        elif len(files) > 1:
            self.view.window().show_quick_panel(self.files, self.on_done)

    def on_done(self, index):
        if index > -1:
            self.interface = self.files[index][0]
            self.insert_interface(self.files[index][1])

    def insert_interface(self, file):

        with open(file, "r") as interface_file:
            content = interface_file.read()

        methods = self.extract_methods_from_string(content)
        if len(methods) == 0:
            print('no methods found in interface ' + self.interface)
            return

        content = ""
        indent      = get_setting('line_indent', "    ")
        author      = get_setting('author', None)
        for method in methods:
            if self.class_has_method(method[0]):
                continue

            method_content = ""
            method_content += indent + "/**\n"
            method_content += indent + " * @see " + self.interface + "::" + method[0] + "()\n"
            if author:
                method_content += indent + " * @author " + author + "\n"
            method_content += indent + " */\n"
            method_content += indent + method[1].strip() + "\n" + indent + "{\n" + indent + "}\n"
            content    += method_content + "\n"

        content = content.strip()
        if len(content) == 0:
            return

        self.view.run_command('insert_content', { "insert_point": self.insert_point, "content": "\n\n" + indent + content });

    def extract_methods_from_string(self, str):
        methods = []
        raw = re.findall(r"\s?public function[^;]+", str)

        if len(raw) == 0:
            return methods

        for line in raw:
            name = re.findall(r"function\s+([^\(]+)", line)
            methods.append((name[0], line))

        return methods

    def class_has_method(self, method):
        region = self.view.find(r"" + method + "\(", 0)
        if not region.empty():
            return True

        return False
