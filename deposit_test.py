from Assignment import *


def test_deposit(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 3000)
    assert deposit() == 'Cash Deposit Success.Your Current Account Balance is Rs:4000.00' 