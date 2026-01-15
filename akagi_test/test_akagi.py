import unittest

from akagi.akagi import mjai_bot
from akagi.libriichi_helper import meta_to_recommend


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # mjai_msg={'type': 'dahai', 'actor': 0, 'pai': 'S', 'tsumogiri': True, 'meta': {'q_values': [-0.5136862, -8.322889, -9.114153, -6.595241, -4.5522585, -7.936266, -7.127452, -3.761138, -5.181018, -4.005292, -2.730616, 0.30888462, -9.339581], 'mask_bits': 17587528089, 'is_greedy': True, 'batch_size': 1, 'eval_time_ns': 46771917, 'shanten': 3, 'at_furiten': False}}
        mjai_msg={'type': 'pon', 'actor': 0, 'target': 2, 'pai': 'P', 'consumed': ['P', 'P'], 'meta': {'q_values': [-0.13100247, -0.50856453], 'mask_bits': 37383395344384, 'is_greedy': True, 'batch_size': 1, 'eval_time_ns': 2289833, 'shanten': 4, 'at_furiten': False}}
        meta = mjai_msg["meta"]
        recommends: list[tuple[str, float]] = meta_to_recommend(meta, False)
        print(f"recommends <- {recommends[:3]}")


if __name__ == '__main__':
    unittest.main()
