# __init__.py
from .bridge_base import BridgeBase
from .amatsuki import AmatsukiBridge
from .majsoul import MajsoulBridge
from .riichi_city import RiichiCityBridge
from .tenhou import TenhouBridge
from .unified import UnifiedBridge
from .jp_mahjong import JpMahjongBridge

__all__ = ['BridgeBase', 'AmatsukiBridge', 'RiichiCityBridge', 'MajsoulBridge', 'TenhouBridge', 'UnifiedBridge','JpMahjongBridge']