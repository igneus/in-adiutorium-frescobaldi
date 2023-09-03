# Frescobaldi modules
import extensions
import extensions.actions

from PyQt5.QtWidgets import QAction

from .inadiutorium import score, contextmenu

class Actions(extensions.actions.ExtensionActionCollection):
    def createActions(self, parent):
        self.copy_score_action = QAction(parent)
        self.duplicate_score_action = QAction(parent)
        self.copy_fial_action = QAction(parent)
        self.goto_source_action = QAction(parent)
        self.goto_variations_action = QAction(parent)

    def translateUI(self):
        self.copy_score_action.setText(_('Copy score'))
        self.duplicate_score_action.setText(_('Duplicate score'))
        self.copy_fial_action.setText(_('Copy FIAL'))
        self.goto_source_action.setText(_('Go to source'))
        self.goto_variations_action.setText(_('Go to variations/main'))

    def configure_menu_actions(self):
        # context menu actions
        self.set_menu_action_list('editor', [
            self.copy_score_action,
            self.duplicate_score_action,
            self.copy_fial_action,
            self.goto_source_action,
            self.goto_variations_action,
        ])

class Extension(extensions.Extension):
    _action_collection_class = Actions

    def __init__(self, parent, name):
        super(Extension, self).__init__(parent, name)

        ac = self.action_collection()
        ac.copy_score_action.triggered.connect(self.do_copy_score)
        ac.duplicate_score_action.triggered.connect(self.do_duplicate_score)
        ac.copy_fial_action.triggered.connect(self.do_copy_fial)
        ac.goto_source_action.triggered.connect(self.do_goto_source)
        ac.goto_variations_action.triggered.connect(self.do_goto_variations)

        # TODO: enable/disable actions depending on availability
        # of a score under cursor

        # TODO:
        # - goto_source only active for score with fial
        # - goto_variations only active for score with id and should have appropriate text variant

    def current_score(self):
        return score.score_under_cursor(self.text_cursor())

    def current_document_path(self):
        return self.current_document().url().path()

    def do_copy_score(self):
        contextmenu.copy_score(self.current_score(), self.current_document())

    def do_duplicate_score(self):
        contextmenu.duplicate_score(self.current_score(), self.current_document(), self.mainwindow())

    def do_copy_fial(self):
        contextmenu.copy_fial(self.current_score(), self.current_document_path())

    def do_goto_source(self):
        contextmenu.goto_source(self.current_score(), self.current_document_path(), self.mainwindow())

    def do_goto_variations(self):
        contextmenu.goto_variations(self.current_score(), self.current_document_path(), self.mainwindow())
