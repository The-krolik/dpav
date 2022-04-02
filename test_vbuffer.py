import vbuffer as vbuf

def test_vbuffer():
    vb = vbuf.VBuffer()
    x, y = vb.getDimensions()
    assert x > 0
    assert y > 0

    vb = vbuf.VBuffer([-100, -100])
    assert x > 0
    assert y > 0

    vb = vbuf.VBuffer([800, 600])
    x, y = vb.getDimensions()
    assert x == 800
    assert y == 600

    assert vb.getPixel([400, 300]) == hex(0)

    vb.writePixel([399, 299], hex(999999999))
    assert vb.getPixel([399, 299]) == hex(0)

    vb.writePixel([399, 299], 9)
    assert vb.getPixel([399, 299]) == hex(0)

    vb.writePixel([0, 0], '0xFFFFFF')
    assert vb.getPixel([0, 0]) == '0xFFFFFF'
    
    vb.clearBuffer()
    assert vb.getPixel([0,0]) == hex(0)
