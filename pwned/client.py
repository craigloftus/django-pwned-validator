from hashlib import sha1
import logging
import requests

from .settings import get_config


logger = logging.getLogger(__name__)


session = requests.Session()
session.headers.update({'User-Agent': get_config()['USER_AGENT'], 'Add-Padding': 'true'})


class PwnedClient:

    def fetch_range(self, prefix):
        try:
            url = ''.join([get_config()['ENDPOINT'], prefix])
            resp = session.get(url, timeout=get_config()['TIMEOUT'])
            return resp.text
        except requests.exceptions.RequestException as e:
            logger.exception("Request to Pwned Password API failed. Validation skipped.")
            return ""

    def parse_range(self, raw_range):
        """
        The range of hashes are returned as suffixes only, followed
        by the number of occurrences, separated by a colon.

            <hash suffix>:<count>
            0018A45C4D1DEF81644B54AB7F969B88D65:1
            00D4F6E8FA6EECAD2A3AA415EEC418D38EC:2
            011053FD0102E94D6AE2F8B83D76FAF94F6:1
            012A7CA357541F0AC487871FEEC1891C49C:2
        """
        split_lines = [line.split(":") for line in raw_range.split('\n') if line.strip()]
        return dict((suffix.strip(), int(count)) for suffix, count in split_lines)

    def join_hash(self, prefix, suffix):
        return ''.join([prefix, suffix])

    def make_hash(self, password):
        # uppercased to match responses
        return sha1(password.encode()).hexdigest().upper()

    def split_hash(self, hashed_password):
        length = get_config()['PREFIX_LENGTH']
        return hashed_password[:length], hashed_password[length:]

    def count_occurrences(self, password):
        hashed_password = self.make_hash(password)
        prefix, suffix = self.split_hash(hashed_password)
        raw_range = self.fetch_range(prefix)
        suffixes = self.parse_range(raw_range)
        return suffixes.get(suffix, 0)
