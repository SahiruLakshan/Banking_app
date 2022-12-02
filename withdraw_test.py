from Assignment import *

def test_withdraw(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 2000)
    assert withdraw() == 'Cash Withdraw Success.Your Current Account Balance is Rs:2000.00'