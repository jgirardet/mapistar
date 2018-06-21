import pytest
from mapistar.first_run import create_directory_tree


def test_create_directory_tree(tmpdir):
    create_directory_tree(tmpdir)
    choices = "0123456789abcdef"
    a = {str(e)[-3:] for e in tmpdir.visit() if len(str(e)) > len(str(tmpdir)) + 2}
    assert a == {i + "/" + j for i in choices for j in choices}
