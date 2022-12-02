from Assignment import *

def test_loan(monkeypatch):
    responses = iter([100000,'36'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses)) 
    assert loan() == 'Monthly Repayment: Rs. 3226.72'