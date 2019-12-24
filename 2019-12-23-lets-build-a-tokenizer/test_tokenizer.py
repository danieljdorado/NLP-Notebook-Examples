from grammar import rules
from tokenizer import Tokenizer

tokenizer_rules = rules
tokenizer = Tokenizer()

# Test rule regexes.
def test_inital_punctuation_regex():
    tokenizer_rules['initial_punctuation_token'].pattern == """^([\'"])([A-Z]+[\',!?":.]*)$"""

def test_final_punctuation_regex():
    assert tokenizer_rules['final_punctuation_token'].pattern == """^([A-Z]+)([',!?":.]+)$"""

def test_all_punctuation_regex():
    assert tokenizer_rules['all_punctuation_token'].pattern == """^([',!?":.])([',!?":.]+)$"""

def test_currency_amount_regex():
    assert tokenizer_rules['currency_amount_token'].pattern == r"""^([$£¥€])([0-9]+\.?[0-9]{,2})([',!?":.]*)$"""


# Test rules.

def test_inital_punctuation_rule():
    inital_punctuation_testdata = {
        '"Hi' : ['"', 'Hi'],
        '\'Hi' : ['\'', 'Hi'],
        '-Hi' : ['-Hi'],
        '""hi' : ['""hi'],
    }

    for test, answer in inital_punctuation_testdata.items():
        assert tokenizer.tokenize(test) == answer

def test_final_punctuation_rule():
    final_punctuation_testdata = {
        'Say,' : ["Say", ','],
        'Hi...' : ['Hi', '.', '.', '.'],
        'Like this:' : ['Like', 'this', ':'],
        'E.T.' : ['E.T.'],
        'etc.' : ['etc', '.'],
    }

    for test, answer in final_punctuation_testdata.items():
        assert tokenizer.tokenize(test) == answer


def test_all_punctuation_rule():
    all_punctuation_testdata = {
        '",' : ["\"", ','],
        '\',' : ["\'", ','],
    }

    for test, answer in all_punctuation_testdata.items():
        assert tokenizer.tokenize(test) == answer


def test_currency_amount_rule():
    currency_amount_testdata = {
        '$5.00' : ['$', '5.00'],
        '¥32' : ['¥', '32'],
        '¥35.00' : ['¥', '35.00'],
        '€23.00' : ['€', '23.00'],
        '€1.23,' : ['€', '1.23', ','],
    }

    for test, answer in currency_amount_testdata.items():
        assert tokenizer.tokenize(test) == answer

def test_exceptions():
    exceptions_testdata = {
        "don't" : ["do", "n't"],
        "isn't" : ["is", "n't"],
        "What's" : ["What", "'s"],
        "what's" : ["what's"],
        "I'm" : ["I", "'m"],
    }
    for test, answer in exceptions_testdata.items():
        assert tokenizer.tokenize(test) == answer