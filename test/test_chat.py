import pytest

from welkin.models.chat import Chat, Chats, ChatSearchResult, SearchChats


@pytest.mark.vcr()
def test_create_chat(client, vcr_cassette):
    patient_id = "17450e44-c2c8-46c4-9486-0d9bfa16d3aa"
    message = "Foo Baz."
    patient = client.Patient(id=patient_id)
    chat = patient.Chat(message=message).create()

    assert isinstance(chat, Chat)
    assert chat.message == message
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_read_chat(client, vcr_cassette):
    patient_id = "17450e44-c2c8-46c4-9486-0d9bfa16d3aa"
    patient = client.Patient(id=patient_id)
    chats = patient.Chats().get()

    assert isinstance(chats, Chats)
    if len(chats) > 0:
        assert isinstance(chats[0], Chat)
        assert chats[0].message
        assert str(chats[0]) == "PATIENT Foo Baz."
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_search_chat(client, vcr_cassette):
    patient_id = "17450e44-c2c8-46c4-9486-0d9bfa16d3aa"
    query = "Test"
    patient = client.Patient(id=patient_id)
    chats = patient.SearchChats().get(query=query)

    assert isinstance(chats, SearchChats)
    if len(chats) > 0:
        assert isinstance(chats[0], ChatSearchResult)
        assert query.lower() in chats[0].message["message"].lower()

    if len(chats) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"
