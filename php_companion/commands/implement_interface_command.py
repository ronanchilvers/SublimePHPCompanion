import sublime
import sublime_plugin

import re

from ..settings import get_setting

class ImplementInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit, interface, file):
        insert_point = self.view.sel()[0].begin()

        with open(file, "r") as interface_file:
            content = interface_file.read()

        methods = self.extract_methods_from_string(content)
        if len(methods) == 0:
            print('no methods found in interface ' + interface)
            return

        new_content = ""
        indent      = get_setting('line_indent', "    ")
        author      = get_setting('author', None)
        for method in methods:
            if self.class_has_method(method[0]):
                continue

            method_content = ""
            method_content += indent + "/**\n"
            method_content += indent + " * @see " + interface + "::" + method[0] + "()\n"
            if author:
                method_content += indent + " * @author " + author + "\n"
            method_content += indent + " */\n"
            method_content += indent + method[1].strip() + "\n" + indent + "{\n" + indent + "}\n"
            print(method_content)

            new_content += method_content + "\n"

        new_content = new_content.strip()
        if len(new_content) == 0:
            return

        if len(new_content) > 0:
            new_content = "/** Start implementation for " + interface + " **/\n\n" + indent + new_content + "\n"
            new_content += "\n" + indent + "/** End implementation for " + interface + " **/\n"

        self.view.insert(edit, insert_point, new_content)

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
