from unittest import TestCase
from unittest.mock import mock_open, patch, MagicMock

from tools.skipfish.parsers import SkipfishResultsParser, SkipfishOutputParser
from tools.skipfish.structs import SkipfishIssuesDesc, SkipfishRisk


class SkipfishResultsParserTest(TestCase):
    ISSUES_DESC = r'''<script src="samples.js"></script>

<script>

var c_count      = 0;
var ignore_click = false;
var max_samples  = 100;
var diff_mode    = false;

/* Descriptions for issues reported by the scanner. */

var issue_desc= {

  "10101": "SSL certificate issuer information",
  "10201": "New HTTP cookie added",
  "10202": "New 'Server' header value seen",
  "10203": "New 'Via' header value seen",
  "10204": "New 'X-*' header value seen",
  "10205": "New 404 signature seen"
  };

/* Simple HTML escaping routine. */

function H(str) { return str.replace(/</g,'&lt;').replace(/"/g,'&quot;'); }


/* Simple truncation routine. */'''

    MIME_SAMPLES = r'''some additional text
    var mime_samples = [
    { 'mime': 'application/javascript', 'samples': [
    { 'url': 'http://192.168.56.102/doc/libssl-dev/demos/asn1/README.ASN1', 'dir': '_m0/0', 'linked': 2, 'len': 206 },
    { 'url': 'http://192.168.56.102/doc/libssl-dev/demos/bio/Makefile', 'dir': '_m0/1', 'linked': 2, 'len': 274 },
    { 'url': 'http://192.168.56.102/doc/libssl-dev/demos/bio/README', 'dir': '_m0/2', 'linked': 2, 'len': 98 },
    { 'url': 'http://192.168.56.102/doc/libssl-dev/demos/bio/server.pem', 'dir': '_m0/3', 'linked': 2, 'len': 1370 } ]
    },
    { 'mime': 'application/pdf', 'samples': [
    { 'url': 'http://192.168.56.102/dvwa/docs/DVWA-Documentation.pdf', 'dir': '_m1/0', 'linked': 2, 'len': 400000 } ]
    },
    { 'mime': 'application/x-gzip', 'samples': [
    { 'url': 'http://192.168.56.102/doc/libsnmp15/AGENT.txt.gz', 'dir': '_m2/0', 'linked': 2, 'len': 19292 },
    { 'url': 'http://192.168.56.102/doc/libsnmp15/changelog.Debian.gz', 'dir': '_m2/1', 'linked': 2, 'len': 11777 },
    { 'url': 'http://192.168.56.102/doc/libsnmp15/FAQ.gz', 'dir': '_m2/2', 'linked': 2, 'len': 49324 },
    { 'url': 'http://192.168.56.102/doc/libsnmp15/NEWS.Debian.gz', 'dir': '_m2/3', 'linked': 2, 'len': 378 },
    { 'url': 'http://192.168.56.102/doc/libsnmp15/README.gz', 'dir': '_m2/4', 'linked': 2, 'len': 5851 }]}];
    some additional text'''

    ISSUE_SAMPLES = '''some additional text
    var issue_samples = [
    { 'severity': 3, 'type': 40909, 'samples': [
    { 'url': 'http://192.168.56.102/doc/libssl-dev/demos/maurice/privkey.pem', 'extra': 'RSA private key', 'sid': '31002', 'dir': '_i0/0' } ]
    },
    { 'severity': 2, 'type': 40402, 'samples': [
    { 'url': 'http://192.168.56.102/dvwa/dvwa/includes/dvwaPage.inc.php', 'extra': 'PHP warning (HTML)', 'sid': '22018', 'dir': '_i1/0' },
    { 'url': 'http://192.168.56.102/dvwa/vulnerabilities/fi/include', 'extra': 'PHP error (HTML)', 'sid': '22008', 'dir': '_i1/1' } ]
    }];
    some additional text'''

    ISSUE_SAMPLES_OCTAL_ESCAPED = r'''var issue_samples = [{'severity': 1, 'type': 40909, 'samples': [
    {'url': 'http://10.12.1.253/sfi9876', 'extra': 'during 404 response checks', 'sid': '0', 'dir': '_i3/0' },
    {'url': 'http://10.12.1.253/sfish\x3e\x27\x3e\x22\x3e\x3c%2Fsfish\x3e\x3csfish\x3e', 'extra': 'XML injection', 'sid': '0', 'dir': '_i3/1' },
    {'url': 'http://10.12.1.253/dav/?C=git;O=D', 'extra': 'during parameter brute-force tests', 'sid': '0', 'dir': '_i3/2' }]
}];'''

    def setUp(self):
        self.parser = SkipfishResultsParser(directory='test_dir')

    def test_parse_issues_desc(self):
        expected = {
            "10101": "SSL certificate issuer information",
            "10201": "New HTTP cookie added",
            "10202": "New 'Server' header value seen",
            "10203": "New 'Via' header value seen",
            "10204": "New 'X-*' header value seen",
            "10205": "New 404 signature seen"
        }
        result = self.parser._parse_issues_desc(self.ISSUES_DESC)._issues

        self.assertDictEqual(result, expected)

    def test_parse_index(self):
        with patch('builtins.open', mock_open(read_data=self.ISSUES_DESC)) as mock_index:
            self.parser._parse_index()

    def test_parse_samples(self):
        with patch('builtins.open', mock_open(read_data=self.ISSUE_SAMPLES)) as mock_sample:
            self.parser._parse_samples()

    def test_issue_samples(self):
        severities_data = {
            "40909": "severity_40909",
            "40402": "severity_40402"
        }
        severities = SkipfishIssuesDesc()
        severities.add(severities_data)

        self.parser.severities = severities
        result = self.parser._parse_issues(self.ISSUE_SAMPLES)

        self.assertEqual(result._issues[0].severity, SkipfishRisk.MEDIUM_RISK)
        self.assertEqual(result._issues[0].type, severities_data["40909"])

    def test_issue_samples_octal_escaped(self):
        severities_data = {
            "40909": "severity_40909",
            "40402": "severity_40402"
        }
        severities = SkipfishIssuesDesc()
        severities.add(severities_data)

        self.parser.severities = severities
        result = self.parser._parse_issues(self.ISSUE_SAMPLES_OCTAL_ESCAPED)

        self.assertEqual(result._issues[1].severity, SkipfishRisk.WARNING)
        self.assertEqual(result._issues[1].type, severities_data["40909"])

    @patch('tools.skipfish.parsers.rmtree')
    def test_parse(self, rmtree_mock):
        self.parser._parse_index = MagicMock()
        self.parser._parse_samples = MagicMock(return_value='test')

        result = self.parser.parse()

        self.assertEqual(result, 'test')
        self.parser._parse_index.assert_called_once_with()
        self.parser._parse_samples.assert_called_once_with()

        rmtree_mock.assert_called_once_with('test_dir')



class SkipfishOutputParserTest(TestCase):
    OUTPUT = '''[*] Scan in progress, please stay tuned...

[!] Scan aborted by user, bailing out!
[+] Copying static resources...
[+] Sorting and annotating crawl nodes: 16
[+] Looking for duplicate entries: 16
[+] Counting unique nodes: 15
[+] Saving pivot data for third-party tools...
[+] Writing scan description...
[+] Writing crawl tree: 16
[+] Generating summary views...
[+] Report saved to 'tmp/skipfish_Tue Aug 30 14:17:33 CEST 2016/index.html' [0x7951b064].
[+] This was a great day for science!'''

    OUTPUT_FETCHED = '''skipfish web application scanner - version 2.10b
[1;32m[*] [1;37mScan in progress, please stay tuned...

[1;33m[!] [1;37mScan aborted by user, bailing out![0;37m
[1;32m[+] [0;37mCopying static resources...
[1;32m
[+] [0;37mSorting and annotating crawl nodes: 1[1;32m
[+] [0;37mSorting and annotating crawl nodes: 51[1;32m
[+] [0;37mSorting and annotating crawl nodes: 101[1;32m
[+] [0;37mSorting and annotating crawl nodes: 151[1;32m
[+] [0;37mSorting and annotating crawl nodes: 201[1;32m
[+] [0;37mSorting and annotating crawl nodes: 251[1;32m
[+] [0;37mSorting and annotating crawl nodes: 301[1;32m
[+] [0;37mSorting and annotating crawl nodes: 351[1;32m
[+] [0;37mSorting and annotating crawl nodes: 401[1;32m
[+] [0;37mSorting and annotating crawl nodes: 451[1;32m
[+] [0;37mSorting and annotating crawl nodes: 501[1;32m
[+] [0;37mSorting and annotating crawl nodes: 537
[1;32m
[+] [0;37mLooking for duplicate entries: 1[1;32m
[+] [0;37mLooking for duplicate entries: 51[1;32m
[+] [0;37mLooking for duplicate entries: 101[1;32m
[+] [0;37mLooking for duplicate entries: 151[1;32m
[+] [0;37mLooking for duplicate entries: 201[1;32m
[+] [0;37mLooking for duplicate entries: 251[1;32m
[+] [0;37mLooking for duplicate entries: 301[1;32m
[+] [0;37mLooking for duplicate entries: 351[1;32m
[+] [0;37mLooking for duplicate entries: 401[1;32m
[+] [0;37mLooking for duplicate entries: 451[1;32m
[+] [0;37mLooking for duplicate entries: 501[1;32m
[+] [0;37mLooking for duplicate entries: 537
[1;32m
[+] [0;37mCounting unique nodes: 1[1;32m
[+] [0;37mCounting unique nodes: 51[1;32m
[+] [0;37mCounting unique nodes: 101[1;32m
[+] [0;37mCounting unique nodes: 151[1;32m
[+] [0;37mCounting unique nodes: 201[1;32m
[+] [0;37mCounting unique nodes: 251[1;32m
[+] [0;37mCounting unique nodes: 301[1;32m
[+] [0;37mCounting unique nodes: 351[1;32m
[+] [0;37mCounting unique nodes: 401[1;32m
[+] [0;37mCounting unique nodes: 451[1;32m
[+] [0;37mCounting unique nodes: 501[1;32m
[+] [0;37mCounting unique nodes: 536
[1;32m[+] [0;37mSaving pivot data for third-party tools...
[1;32m[+] [0;37mWriting scan description...
[1;32m
[+] [0;37mWriting crawl tree: 1[1;32m
[+] [0;37mWriting crawl tree: 51[1;32m
[+] [0;37mWriting crawl tree: 101[1;32m
[+] [0;37mWriting crawl tree: 151[1;32m
[+] [0;37mWriting crawl tree: 201[1;32m
[+] [0;37mWriting crawl tree: 251[1;32m
[+] [0;37mWriting crawl tree: 301[1;32m
[+] [0;37mWriting crawl tree: 351[1;32m
[+] [0;37mWriting crawl tree: 401[1;32m
[+] [0;37mWriting crawl tree: 451[1;32m
[+] [0;37mWriting crawl tree: 501[1;32m
[+] [0;37mWriting crawl tree: 537
[1;32m[+] [0;37mGenerating summary views...
[1;32m[+] [0;37mReport saved to '[1;34m/tmp/skipfish_1472650914.8062923/index.html[0;37m' [[1;34m0xdeae3458[0;37m].
[1;32m[+] [1;37mThis was a great day for science![0m'''

    def setUp(self):
        self.parser = SkipfishOutputParser()

    def test_get_log_dir(self):

        expected = 'tmp/skipfish_Tue Aug 30 14:17:33 CEST 2016'
        result = self.parser._get_log_dir(output=self.OUTPUT, directory='tmp')

        self.assertEqual(result, expected)

    @patch('tools.skipfish.parsers.SkipfishResultsParser')
    @patch('tools.skipfish.parsers.SkipfishOutputParser._get_log_dir')
    @patch('tools.skipfish.parsers.cfg.get', MagicMock(return_value='tmp/'))
    def test_parse(self, get_dir_mock, parser_mock):
        get_dir_mock.return_value = 'test'
        self.parser.parse(self.OUTPUT)

        parser_mock.assert_called_once_with(directory='test')
        parser_mock.return_value.parse.assert_called_once_with()
        get_dir_mock.assert_called_once_with(output=self.OUTPUT, directory='tmp/')

    def test_get_log_dir_from_fetched_output(self):

        expected = '/tmp/skipfish_1472650914.8062923'
        result = self.parser._get_log_dir(output=self.OUTPUT_FETCHED, directory='/tmp')

        self.assertEqual(result, expected)

    @patch('tools.skipfish.parsers.SkipfishResultsParser')
    @patch('tools.skipfish.parsers.SkipfishOutputParser._get_log_dir')
    @patch('tools.skipfish.parsers.cfg.get', MagicMock(return_value='/tmp/'))
    def test_parse_fetched_output(self, get_dir_mock, parser_mock):
        get_dir_mock.return_value = 'test'
        self.parser.parse(self.OUTPUT_FETCHED)

        parser_mock.assert_called_once_with(directory='test')
        parser_mock.return_value.parse.assert_called_once_with()
        get_dir_mock.assert_called_once_with(output=self.OUTPUT_FETCHED, directory='/tmp/')