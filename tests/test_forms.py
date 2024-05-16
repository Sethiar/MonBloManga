"""
Tests pour les formulaires du blog
"""

import sys
import os

# Chemin absolu du répertoire courant
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path
sys.path.append(parent_dir)

import pytest

from Models.forms import AdminConnection, UserSaving, NewAuthor, UserConnection, NewCategorieForm, \
    NewSubjectForumForm, ArticleForm, CommentForm


def test_admin_connection_form():
    form = AdminConnection()
    assert form.validate()


def test_user_saving_form():
    form = UserSaving()
    assert form.validate()


def test_new_author_form():
    form = NewAuthor()
    assert form.validate()


def test_user_connection_form():
    form = UserConnection()
    assert form.validate()


def test_new_categorie_form():
    form = NewCategorieForm()
    assert form.validate()


def test_new_subject_forum_form():
    form = NewSubjectForumForm()
    assert form.validate()


def test_article_form():
    form = ArticleForm()
    assert form.validate()


def test_comment_form():
    form = CommentForm()
    assert form.validate()
