from Assignment import *

def test_register(monkeypatch):
    responses = iter(['Sahiru','12345678'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses)) 
    assert create() == 'You already have an account!'