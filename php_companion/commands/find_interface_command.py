import sublime
import sublime_plugin

import re

from ..settings import get_setting
from ..utils import find_symbol

class FindInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view   = self.view
        region = view.find(r"implements[^\{]+\{", 0)
        if region.empty():
            return sublime.status_message('No class definition found')

        interfaces = view.substr(region).replace("implements", "").replace("{", "")
        interfaces = interfaces.split(",")

        # Hack hack hacky
        # Find the end of the class by expanding the selection to the matching
        # bracket. Store and restore the current selection while we're at it!
        stored = [[item.a, item.b] for item in view.sel()]
        view.sel().clear()
        view.sel().add(region)
        view.run_command('expand_selection', { "to": "brackets" })
        region = view.sel()[0]
        view.sel().clear()

        for item in stored:
            view.sel().add(sublime.Region(item[0], item[1]))

        for interface in interfaces:
            interface = interface.strip()
            print('interface is ' + interface)
            files = find_symbol(interface, view.window())
            if -1 < interface.find('Interface'):
                print('munging interface name a little from ' + interface + ' to ' + interface.replace('Interface', ''))
                files = files + find_symbol(interface.replace('Interface', ''), view.window())

            if len(files) == 0:
                print('no files found for symbol ' + interface)
                continue

            print('found ' + str(len(files)) + ' for symbol ' + interface)
            view.run_command("generate_interface", { "insert_point": region.end() - 1, "interface": interface, "files": files })
