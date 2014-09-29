import sublime
import sublime_plugin

class InsertContentCommand(sublime_plugin.TextCommand):

    def run(self, edit, insert_point, content):
        self.view.insert(edit, insert_point, content)
