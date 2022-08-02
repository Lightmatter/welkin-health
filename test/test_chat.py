import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.chat import Chat, Chats, ChatSearchResult, SearchChats


@pytest.mark.vcr()
def test_create_chat(client, vcr_cassette):
    patient_id = "17450e44-c2c8-46c4-9486-0d9bfa16d3aa"
    message = "Foo Baz."
    chat = client.Chat(message=message).create(patient_id=patient_id)

    assert isinstance(chat, Chat)
    assert chat.message == message
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_read_chat(client, vcr_cassette):
    patient_id = "17450e44-c2c8-46c4-9486-0d9bfa16d3aa"
    chats = client.Chats().get(patient_id=patient_id)

    assert isinstance(chats, Chats)
    if len(chats) > 0:
        assert isinstance(chats[0], Chat)
        assert chats[0].message
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_search_chat(client, vcr_cassette):
    patient_id = "17450e44-c2c8-46c4-9486-0d9bfa16d3aa"
    query = "Test"
    chats = client.SearchChats().get(patient_id=patient_id, query=query)

    assert isinstance(chats, SearchChats)
    if len(chats) > 0:
        assert isinstance(chats[0], ChatSearchResult)
        assert query.lower() in chats[0].message["message"].lower()

    if len(chats) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"
