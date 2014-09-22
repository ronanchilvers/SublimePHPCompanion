import sublime
import sublime_plugin

import re

from ..settings import get_setting

class ImplementInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit, leading_separator=False):
        view = self.view
        region = view.find(r"implements[^\{]+\{", 0)

        if region.empty():
            return sublime.status_message('No class definition found')

        interfaces = view.substr(region).replace("implements", "").replace("{", "")
        interfaces = interfaces.split(",")

        new_content = "\n"
        indent = get_setting('line_indent', "    ")
        author = get_setting('author', None)
        for interface in interfaces:
            interface = interface.strip()
            print('working on interface ' + interface)
            files = view.window().lookup_symbol_in_index(interface)

            if len(files) > 1:
                print('more than one file found for interface ' + interface)
                print(files)
                print('not handling multiple files yet!')
                continue

            with open(files[0][0], "r") as interface_file:
                content = interface_file.read()

            methods = self.extract_methods_from_string(content)
            if len(methods) == 0:
                print('no methods found in interface ' + interface)
                continue;

            method_content = ""
            for method in methods:
                if self.class_has_method(method[0]):
                    continue
                method_content += indent + "/**\n"
                method_content += indent + " * @see " + interface + "::" + method[0] + "()\n"
                if author:
                    method_content += indent + " * @author " + author + "\n"
                method_content += indent + " */\n"
                method_content += indent + method[1].strip() + "\n" + indent + "{\n" + indent + "}\n"
                method_content += "\n"
            if len(method_content) > 0:
                new_content += "\n" + indent + "/** Start implementation for " + interface + " **/\n"
                new_content += "\n" + method_content
                new_content += indent + "/** End implementation for " + interface + " **/\n"

        if len(new_content.strip()) == 0:
            return

        line = self.view.line(region)
        self.view.insert(edit, line.end(), new_content)

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


        # line = view.line(region)
        # view.insert(edit, line.end(), text)

        # self.edit = edit
        # view = self.view
        # self.region = view.word(view.sel()[0])
        # symbol = view.substr(self.region)

        # if len(symbol) == 0:
        #     print('No symbol found')
        #     return

        # print('symbol is ' + symbol)
        # self.files = view.window().lookup_symbol_in_index(symbol)

        # if len(self.files) == 0:
        #     print('symbol not found')
        #     return

        # if len(self.files) == 1:
        #     self.insert_interface(self.files[0])
        #     return;

        # view.window().show_quick_panel(self.files, self.on_done)

    # def on_done(self, index):
    #     self.insert_interface(self.files[index])
    #     return

    # def insert_interface(self, file):
    #     #implements\s+[\w,\s]+{
    #     region = self.view.find(r"implements[^{]+{", 0)
    #     print(region)

    #     if region.empty():
    #         return sublime.status_message('No class definition found')

    #     contents = "\n// Testing insert\n"

    #     line = self.view.line(region)
    #     self.view.insert(self.edit, line.end(), contents)



