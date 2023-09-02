# Frescobaldi modules
import extensions
import extensions.actions

from PyQt5.QtWidgets import QAction

from .inadiutorium import score, contextmenu

class Actions(extensions.actions.ExtensionActionCollection):
    def createActions(self, parent):
        self.copy_score_action = QAction(parent)

    def translateUI(self):
        self.copy_score_action.setText(_('Copy score'))

    def configure_menu_actions(self):
        self.set_menu_action_list('editor', [self.copy_score_action])

class Extension(extensions.Extension):
    _action_collection_class = Actions

    def __init__(self, parent, name):
        super(Extension, self).__init__(parent, name)

        ac = self.action_collection()
        ac.copy_score_action.triggered.connect(self.do_copy_score)

        # TODO: enable/disable actions depending on availability
        # of a score under cursor

    def current_score(self):
        return score.score_under_cursor(self.text_cursor())

    def do_copy_score(self):
        contextmenu.copy_score(self.current_score(), self.current_document())
