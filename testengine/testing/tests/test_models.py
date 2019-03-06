from mixer.backend.django import mixer
import pytest


@pytest.fixture
@pytest.mark.django_db
def test():
    return mixer.blend('testing.Test', title='mytest')

@pytest.mark.django_db
def test_test_is_assigned_slug(test):
     assert test.slug == 'mytest'
