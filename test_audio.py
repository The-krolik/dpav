import audio as aud

def test_getBitNumber():
  a = aud.Audio()
  assert a.getBitNumber() == 16
  
def test_setBitNumber():
  a = aud.Audio()
  a.setBitNumber(8)
  assert a.getBitNumber() == 8
