# -*- coding: utf-8 -*-
"""Fixtures and util for tests."""

import pytest

pytest_plugins = ['aiida.manage.tests.pytest_fixtures']


@pytest.fixture(scope='function', autouse=True)
def clear_database_plugin(clear_database):  # pylint: disable=unused-argument
    """Clear the database before each test.
    We autouse clear_database of aiida-core
    """
    #aiida_profile.reset_db()
    #yield
    #aiida_profile.reset_db()
