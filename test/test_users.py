import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.user import User, Users


@pytest.mark.vcr()
def test_user_create(client, vcr_cassette):
    user = client.User(username="bar", email="bar@foo.com").create()

    assert isinstance(user, User)
    assert hasattr(user, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_user_read(client, vcr_cassette):
    user = client.User(id="658f3b36-a12a-4bce-aad6-1e4930948b7d")

    assert isinstance(user, User)
    assert len(user) == 1

    user.get()

    assert len(user) > 1
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_user_read_all(client, vcr_cassette):
    users = client.Users().get()

    assert isinstance(users, Users)
    assert isinstance(users[0], User)

    if len(users) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_user_search(client, vcr_cassette):
    users = client.Users().search("lightmatter")

    assert isinstance(users, Users)
    assert isinstance(users[0], User)

    if len(users) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_user_update(client, vcr_cassette):
    user = client.User(id="92cc5811-ff71-4101-915d-a419383db168").get()
    name = user.firstName

    user.update(firstName="Baz")

    assert user.firstName != name
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_user_delete(client, vcr_cassette):
    user = client.User(id="658f3b36-a12a-4bce-aad6-1e4930948b7d")

    with pytest.raises(WelkinHTTPError) as excinfo:
        user.delete()

    assert excinfo.value.response.status_code == 403

    assert len(vcr_cassette) == 1
