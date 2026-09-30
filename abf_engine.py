"""
ABF core engine (v2).

The previous module invented ABF-CTL-01…05 and treated PII / agentic systems as
EU high-risk. That logic is withdrawn.

Use:
  from abf.classify import classify, obligation_applies
  from abf.library import build_library
  python3 tools/abf_cli.py --answers answers.json
"""

from abf.classify import ScreeningResult, classify, obligation_applies
from abf.library import build_library

__all__ = [
    "ScreeningResult",
    "build_library",
    "classify",
    "obligation_applies",
]
