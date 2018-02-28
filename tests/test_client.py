import pytest

from pwned.client import PwnedClient

def test_parse_range_valid():
    client = PwnedClient()
    raw_range = """
    0018A45C4D1DEF81644B54AB7F969B88D65:1
    00D4F6E8FA6EECAD2A3AA415EEC418D38EC:2
    011053FD0102E94D6AE2F8B83D76FAF94F6:1
    012A7CA357541F0AC487871FEEC1891C49C:2
    """
    expected = {
        '0018A45C4D1DEF81644B54AB7F969B88D65': 1,
        '00D4F6E8FA6EECAD2A3AA415EEC418D38EC': 2,
        '011053FD0102E94D6AE2F8B83D76FAF94F6': 1,
        '012A7CA357541F0AC487871FEEC1891C49C': 2,
    }
    assert client.parse_range(raw_range) == expected


def test_join_hash():
    client = PwnedClient()
    prefix = '00D4F'
    suffix = '6E8FA6EECAD2A3AA415EEC418D38EC'
    expected = '00D4F6E8FA6EECAD2A3AA415EEC418D38EC'
    assert client.join_hash(prefix, suffix) == expected


def test_make_hash():
    client = PwnedClient()
    password = 'My1E37pwd'
    expected = '8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A'
    assert client.make_hash(password) == expected


def test_split_hash():
    client = PwnedClient()
    hashed_password = '8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A'
    assert client.split_hash(hashed_password) == ('8CEF1', 'E00B20F463C1E48B589B03660D4E3B9EF7A')


def test_split_hash_prefix_length(monkeypatch):
    monkeypatch.setattr('pwned.app_settings.PWNED', {'PREFIX_LENGTH': 10})
    client = PwnedClient()
    hashed_password = '8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A'
    prefix, suffix = client.split_hash(hashed_password)
    assert len(prefix) == 10


@pytest.mark.vcr
def test_count_occurrences_found():
    client = PwnedClient()
    count = client.count_occurrences('password')
    assert count == 3303003


@pytest.mark.vcr
def test_count_occurrences_none():
    client = PwnedClient()
    count = client.count_occurrences('8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A')
    assert count == 0
