import audio

def test_getBitNumber():
  a = Audio()
  assert a.getBitNumber() == 16
  
def test_setBitNumber():
  a = Audio()
  a.setBitNumber(8)
  assert a.getBitNumber() == 8
  

