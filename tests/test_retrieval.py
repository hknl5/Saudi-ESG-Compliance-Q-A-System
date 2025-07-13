import importlib
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import types
# Patch heavy/missing dependencies before importing the module
sys.modules['faiss'] = types.SimpleNamespace(read_index=lambda *a, **kw: None)

sentence_stub = types.ModuleType('sentence_transformers')
class DummyModel:
    def __init__(self, *a, **kw):
        pass
sentence_stub.SentenceTransformer = DummyModel
sys.modules['sentence_transformers'] = sentence_stub

sys.modules['openai'] = types.ModuleType('openai')

# Stub packages that may not be installed
sys.modules['numpy'] = types.ModuleType('numpy')
dotenv_stub = types.ModuleType('dotenv')
dotenv_stub.load_dotenv = lambda *a, **k: None
sys.modules['dotenv'] = dotenv_stub

# Import the module after stubbing
ar = importlib.import_module('advanced_retrieval')


def setup_function(function):
    ar.seen_texts.clear()


def test_short_text_rejected():
    assert not ar.is_valid_chunk("too short")


def test_repeated_text_ignored():
    text = "this is a valid chunk with enough words for this simple test"
    assert ar.is_valid_chunk(text)
    assert not ar.is_valid_chunk(text)


def test_valid_text_passes():
    text = "another valid chunk that easily surpasses the minimum word count"
    assert ar.is_valid_chunk(text)
