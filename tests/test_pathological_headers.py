import pytest

import eml_parser.parser


class TestPathologicalHeaders:
    @pytest.mark.parametrize('header,count', [('cc', 500), ('From', 500), ('resent-sender', 500), ('Sender', 500)])
    def test_many_open_parentheses(self, header: str, count: int) -> None:
        parens = b'(' * count
        sample = header.encode() + b': ' + parens + b', c@c' + b', Foo Bar <d@d> ' + parens
        ep = eml_parser.EmlParser()
        data = ep.decode_email_bytes(sample)
        header_name = header.lower()
        assert data['header']['header'][header_name] == ['c@c, d@d']
        if header_name in ('to', 'cc'):
            assert data['header'][header_name] == ['c@c', 'd@d']
