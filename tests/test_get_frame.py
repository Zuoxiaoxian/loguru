import sys
import loguru

def test_with_sys_getframe(monkeypatch):
    patched = lambda: None
    monkeypatch.setattr(sys, '_getframe', patched)
    assert loguru._get_frame.get_get_frame_function() == patched

def test_without_sys_getframe(monkeypatch):
    monkeypatch.delattr(sys, '_getframe')
    assert loguru._get_frame.get_get_frame_function() == loguru._get_frame.get_frame_fallback

def test_get_frame_fallback():
    frame_root = frame_a = frame_b = None

    def a():
        nonlocal frame_a
        frame_a = loguru._get_frame.get_frame_fallback(1)
        b()

    def b():
        nonlocal frame_b
        frame_b = loguru._get_frame.get_frame_fallback(2)

    frame_root = loguru._get_frame.get_frame_fallback(0)
    a()

    assert frame_a == frame_b == frame_root

