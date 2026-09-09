import unittest
from f1_strategy_sim import F1StrategySimulator

class TestF1StrategySimulator(unittest.TestCase):

    def setUp(self):
        self.sim = F1StrategySimulator(total_laps=53, pit_loss_seconds=22.5)

    def test_compound_degradation_delta(self):
        """Valida se o pneu Soft tem maior taxa de degradação que o Hard."""
        soft_deg = self.sim.compounds["SOFT"].deg_per_lap
        hard_deg = self.sim.compounds["HARD"].deg_per_lap
        self.assertGreater(soft_deg, hard_deg)

    def test_stint_simulation_length(self):
        """Garante que a simulação devolve o número exato de voltas do stint."""
        stint_laps = 15
        lap_times = self.sim.simulate_stint("SOFT", stint_laps)
        self.assertEqual(len(lap_times), stint_laps)

    def test_strategy_evaluation_pit_count(self):
        """Verifica a contagem correta de paragens nas boxes."""
        res = self.sim.evaluate_strategy("1-Stop", [("SOFT", 15), ("HARD", 38)])
        self.assertEqual(res["pit_stops"], 1)

if __name__ == '__main__':
    unittest.main()
