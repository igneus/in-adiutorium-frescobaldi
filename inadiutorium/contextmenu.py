import os.path

from PyQt5.QtWidgets import QApplication, QAction, QMessageBox
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import QUrl

import app

from . import is_in_adiutorium_file
from .variations import is_variations_file, main_file, variations_file
from . import score


def copy_score(score, document):
    # copy score
    copy_cursor = QTextCursor(document)
    score_end = score.end()
    # it isn't easily possible to get score start index
    # from the DOM ...
    start_token = '\\score'
    score_start_cur = document.find(start_token, score_end, QTextDocument.FindBackward)
    score_start = score_start_cur.position() - len(start_token)
    copy_cursor.setPosition(score_start, QTextCursor.MoveAnchor)
    copy_cursor.setPosition(score_end, QTextCursor.KeepAnchor)

    # copy to clipboard
    fragment = copy_cursor.selection()
    QApplication.clipboard().setText(fragment.toPlainText())

def duplicate_score(score, document, mainwindow):
    # add newline after the score
    cursor = QTextCursor(document)
    cursor.setPosition(score.end(), QTextCursor.MoveAnchor)
    cursor.insertText('\n\n')

    # copy score
    copy_cursor = QTextCursor(document)
    score_end = score.end()
    # it isn't easily possible to get score start index
    # from the DOM ...
    start_token = '\\score'
    score_start_cur = document.find(start_token, score_end, QTextDocument.FindBackward)
    score_start = score_start_cur.position() - len(start_token)
    while document.characterAt(score_start - 1) == ' ':
        score_start -= 1
    copy_cursor.setPosition(score_start, QTextCursor.MoveAnchor)
    copy_cursor.setPosition(score_end, QTextCursor.KeepAnchor)

    # insert copy
    fragment = copy_cursor.selection()
    cursor.insertFragment(fragment)

    # make it selected
    fragment_len = len(fragment.toPlainText())
    score_beginning = cursor.position() - fragment_len
    cursor.setPosition(score_beginning, QTextCursor.KeepAnchor)
    mainwindow.setTextCursor(cursor)

def copy_fial(score, path):
    fial = '{0}#{1}'.format(
        project_path(path).replace('variationes/', ''),
        score.headers['id']
    )
    QApplication.clipboard().setText(fial)

def goto_source(score, path, mainwindow):
    open_fial(score.fial(), path, mainwindow)

def goto_variations(score, path, mainwindow):
    if is_variations_file(path):
        path_to_open = main_file(path)
    else:
        path_to_open = variations_file(path)

    open_score(path_to_open, score.headers['id'], mainwindow)

def goto_variations_file(path, mainwindow):
    if is_variations_file(path):
        path_to_open = main_file(path)
    else:
        path_to_open = variations_file(path)

    open_file(path_to_open, mainwindow)

""" Helper functions """

def open_fial(fial, project_path, mainwindow):
    open_score(fial.expand_path(project_path), fial.id, mainwindow)

def open_file(path, mainwindow):
    url = QUrl.fromLocalFile(path)
    try:
        doc = app.openUrl(url)
    except IOError as e:
        msg = 'Failed to read referenced file {0}.'.format(path)
        QMessageBox.critical(mainwindow, app.caption(_("Error")), msg)
        return None
    else:
        mainwindow.setCurrentDocument(doc)
        return doc

def open_score(path, score_id, mainwindow):
    doc = open_file(path, mainwindow)
    if doc is not None:
        mainwindow.setCurrentDocument(doc)
        id_str = 'id = "{0}"'.format(score_id)
        cursor = doc.find(id_str)
        if cursor.isNull():
            msg = "Score with id '{0}' not found.".format(score_id)
            QMessageBox.information(mainwindow, app.caption(_("Error")), msg)
        else:
            mainwindow.setTextCursor(cursor)

def project_path(path):
    """
    Path relative to the project root.
    Directory containing the .git directory is considered project root.
    """
    return path.replace(git_root_dir(path) + '/', '')

def git_root_dir(path):
    while not (path == '' or path == '/'):
        if os.path.isdir(path) and os.path.isdir(os.path.join(path, '.git')):
            break
        path = os.path.dirname(path)
    return path
