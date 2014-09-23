import sublime
import sublime_plugin

import re

from ..settings import get_setting

class ImplementInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit, interface):

