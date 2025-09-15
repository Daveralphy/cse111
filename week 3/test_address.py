from address import extract_city, extract_state, extract_zipcode
import pytest

def test_extract_city():
    assert extract_city("123 Main St, Rexburg, ID 83440") == "Rexburg"

def test_extract_state():
    assert extract_state("123 Main St, Rexburg, ID 83440") == "ID"

def test_extract_zipcode():
    assert extract_zipcode("123 Main St, Rexburg, ID 83440") == "83440"

pytest.main(["-v", "--tb=line", "-rN", __file__])