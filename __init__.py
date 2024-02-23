# Frescobaldi modules
import app
import extensions
import extensions.actions

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QColor

from .inadiutorium import score, contextmenu, variations

class Actions(extensions.actions.ExtensionActionCollection):
    GOTO_VARIATIONS = 'Go to variations'
    GOTO_MAIN = 'Go to main'
    GOTO_UNCERTAIN = 'Go to variations/main'

    def createActions(self, parent):
        self.copy_score_action = QAction(parent)
        self.duplicate_score_action = QAction(parent)
        self.copy_fial_action = QAction(parent)
        self.goto_source_action = QAction(parent)
        self.goto_source_variations_action = QAction(parent)
        self.goto_variations_action = QAction(parent)

        self.goto_variations_file_action = QAction(parent)

    def translateUI(self):
        self.copy_score_action.setText(_('Copy score'))
        self.duplicate_score_action.setText(_('Duplicate score'))
        self.copy_fial_action.setText(_('Copy FIAL'))
        self.goto_source_action.setText(_('Go to source'))
        self.goto_source_variations_action.setText(_('Go to variations (source)'))
        self.goto_variations_action.setText(_(self.GOTO_UNCERTAIN))

        self.goto_variations_file_action.setText(_(self.GOTO_UNCERTAIN))

    def configure_menu_actions(self):
        actions = [
            self.copy_score_action,
            self.duplicate_score_action,
            self.copy_fial_action,
            self.goto_source_action,
            self.goto_source_variations_action,
            self.goto_variations_action,
        ]

        # editor context menu
        self.set_menu_action_list('editor', actions)
        # Tools menu
        self.set_menu_action_list('tools', actions)

class Extension(extensions.Extension):
    _action_collection_class = Actions

    def __init__(self, parent, name):
        super(Extension, self).__init__(parent, name)

        ac = self.action_collection()
        ac.copy_score_action.triggered.connect(self.do_copy_score)
        ac.duplicate_score_action.triggered.connect(self.do_duplicate_score)
        ac.copy_fial_action.triggered.connect(self.do_copy_fial)
        ac.goto_source_action.triggered.connect(self.do_goto_source)
        ac.goto_source_variations_action.triggered.connect(self.do_goto_source_variations)
        ac.goto_variations_action.triggered.connect(self.do_goto_variations)

        ac.goto_variations_file_action.triggered.connect(self.do_goto_variations_file)

        self.menu('editor').aboutToShow.connect(self.do_update_actions)
        self.menu('tools').aboutToShow.connect(self.do_update_actions)

        # code below hooks into the editor's internal APIs,
        # beyond the Extensions API, and is more probable to break
        # in future

        app.documentLoaded.connect(self.do_update_document_tab)
        app.documentUrlChanged.connect(self.do_update_document_tab)

        tab_menu = self.mainwindow().tabBar.contextMenu()
        tab_menu.addSeparator()
        tab_menu.addAction(ac.goto_variations_file_action)
        tab_menu.aboutToShow.connect(self.set_goto_variations_text)

    def current_score(self):
        return score.score_under_cursor(self.text_cursor())

    def current_document_path(self):
        return self.current_document().url().path()

    def set_goto_variations_text(self):
        ac = self.action_collection()
        text = Actions.GOTO_MAIN if variations.is_variations_file(self.current_document_path()) else Actions.GOTO_VARIATIONS
        ac.goto_variations_action.setText(_(text))
        ac.goto_variations_file_action.setText(_(text))

    def do_copy_score(self):
        contextmenu.copy_score(self.current_score(), self.current_document())

    def do_duplicate_score(self):
        contextmenu.duplicate_score(self.current_score(), self.current_document(), self.mainwindow())

    def do_copy_fial(self):
        contextmenu.copy_fial(self.current_score(), self.current_document_path())

    def do_goto_source(self):
        contextmenu.goto_source(self.current_score(), self.current_document_path(), self.mainwindow())

    def do_goto_source_variations(self):
        contextmenu.goto_source_variations(self.current_score(), self.current_document_path(), self.mainwindow())

    def do_goto_variations(self):
        contextmenu.goto_variations(self.current_score(), self.current_document_path(), self.mainwindow())

    def do_goto_variations_file(self):
        contextmenu.goto_variations_file(self.current_document_path(), self.mainwindow())

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
            ac.goto_source_variations_action.setEnabled(score.has_fial())
            self.set_goto_variations_text()

    def do_update_document_tab(self, document):
        tabbar = self.mainwindow().tabBar
        if variations.is_variations_file(document.url().toLocalFile()) and document in tabbar.docs:
            index = tabbar.docs.index(document)
            color = QColor('indigo')
            tabbar.setTabTextColor(index, color)
        # TODO: reset color if never more appropriate due to path change
        # (but this rarely ever happens in practice, so we can just
        # ignore it)
