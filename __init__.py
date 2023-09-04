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

        self.menu('editor').aboutToShow.connect(self.do_update_actions)
        self.menu('tools').aboutToShow.connect(self.do_update_actions)

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

    def do_update_actions(self):
        """
        Enables/disables actions based on what's under the cursor
        """
        score = self.current_score()
        ac = self.action_collection()

        def setAllEnabled(action_collection, enabled):
            for name, action in action_collection.actions().items():
                action.setEnabled(enabled)

        if score is None:
            setAllEnabled(ac, False)
        else:
            setAllEnabled(ac, True)
            ac.copy_fial_action.setEnabled(score.has_id())
            ac.goto_variations_action.setEnabled(score.has_id())
            ac.goto_source_action.setEnabled(score.has_fial())
            # TODO: goto_variations should have appropriate text
