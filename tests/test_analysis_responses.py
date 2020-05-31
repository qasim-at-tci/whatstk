import math
import pytest
from whatstk.objects import WhatsAppChat
from whatstk.analysis.responses import response_matrix


filename = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_response_matrix_1():
    chat = WhatsAppChat.from_txt(filename)
    df_resp = response_matrix(chat=chat, zero_own=True)

    # Check shape and colnames of returned dataframe
    n_users = len(chat.users)
    assert(df_resp.shape == (n_users, n_users))
    assert(set(chat.users) == set(df_resp.columns))

    # Check diagonal of returned dataframe is zero
    assert(all([df_resp.loc[user, user] == 0 for user in df_resp.columns]))


def test_response_matrix_2():
    chat = WhatsAppChat.from_txt(filename)
    df_resp = response_matrix(chat=chat, zero_own=False)

    # Check shape and colnames of returned dataframe
    n_users = len(chat.users)
    assert(df_resp.shape == (n_users, n_users))
    assert(set(chat.users) == set(df_resp.columns))


def test_response_matrix_3():
    chat = WhatsAppChat.from_txt(filename)
    df_resp = response_matrix(chat=chat, norm='joint')

    # Check shape and colnames of returned dataframe
    n_users = len(chat.users)
    assert(df_resp.shape == (n_users, n_users))
    assert(set(chat.users) == set(df_resp.columns))

    # Check scaling has been done correct
    assert(math.isclose(df_resp.sum().sum(), 1))


def test_response_matrix_4():
    chat = WhatsAppChat.from_txt(filename)
    df_resp = response_matrix(chat=chat, norm='sender')

    # Check shape and colnames of returned dataframe
    n_users = len(chat.users)
    assert(df_resp.shape == (n_users, n_users))
    assert(set(chat.users) == set(df_resp.columns))

    # Check scaling has been done correct
    assert(all([math.isclose(x, 1) for x in df_resp.sum(axis=1)]))


def test_response_matrix_5():
    chat = WhatsAppChat.from_txt(filename)
    df_resp = response_matrix(chat=chat, norm='receiver')

    # Check shape and colnames of returned dataframe
    n_users = len(chat.users)
    assert(df_resp.shape == (n_users, n_users))
    assert(set(chat.users) == set(df_resp.columns))

    # Check scaling has been done correct
    assert(all([math.isclose(x, 1) for x in df_resp.sum(axis=0)]))


def test_response_matrix_error():
    chat = WhatsAppChat.from_txt(filename)
    with pytest.raises(ValueError):
        _ = response_matrix(chat=chat, norm='error')
