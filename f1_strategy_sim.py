import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Compound:
    name: str
    pace_delta: float       # Tempo relativo ao Medium (segundos)
    deg_per_lap: float      # Perda de tempo por volta (segundos)
    max_useful_laps: int    # Vida útil ideal da borracha

class F1StrategySimulator:
    def __init__(self, total_laps: int, pit_loss_seconds: float):
        self.total_laps = total_laps
        self.pit_loss = pit_loss_seconds
        
        # Performance base dos compostos Pirelli
        self.compounds = {
            "SOFT": Compound("SOFT", pace_delta=-0.6, deg_per_lap=0.12, max_useful_laps=15),
            "MEDIUM": Compound("MEDIUM", pace_delta=0.0, deg_per_lap=0.07, max_useful_laps=28),
            "HARD": Compound("HARD", pace_delta=0.5, deg_per_lap=0.03, max_useful_laps=45)
        }

    def simulate_stint(self, compound_key: str, laps: int, base_pace: float = 80.0) -> List[float]:
        comp = self.compounds[compound_key]
        lap_times = []
        
        for lap in range(1, laps + 1):
            # Degradação exponencial quando o pneu passa a vida útil
            wear_factor = 1.0 if lap <= comp.max_useful_laps else 1.8
            deg = (lap * comp.deg_per_lap) * wear_factor
            lap_time = base_pace + comp.pace_delta + deg
            lap_times.append(round(lap_time, 3))
            
        return lap_times

    def evaluate_strategy(self, strategy_name: str, sequence: List[tuple]) -> Dict:
        """
        sequence ex: [("SOFT", 15), ("HARD", 42)]
        """
        total_time = 0.0
        all_laps = []
        pit_stops = len(sequence) - 1

        for idx, (compound, laps) in enumerate(sequence):
            stint_times = self.simulate_stint(compound, laps)
            all_laps.extend(stint_times)
            total_time += sum(stint_times)
            
            # Adiciona tempo de perda na box (exceto no final da corrida)
            if idx < pit_stops:
                total_time += self.pit_loss

        return {
            "strategy": strategy_name,
            "total_time_seconds": round(total_time, 2),
            "pit_stops": pit_stops,
            "avg_lap": round(sum(all_laps) / len(all_laps), 3)
        }

def format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    rem_seconds = seconds % 60
    return f"{minutes}m {rem_seconds:.2f}s"

if __name__ == "__main__":
    print("🏎️  F1 RACE STRATEGY SIMULATOR — MONZA (53 LAPS)")
    print("=" * 55)
    
    sim = F1StrategySimulator(total_laps=53, pit_loss_seconds=22.5)
    
    strategies = [
        ("1-Stop: Soft -> Hard", [("SOFT", 15), ("HARD", 38)]),
        ("1-Stop: Medium -> Hard", [("MEDIUM", 22), ("HARD", 31)]),
        ("2-Stop: Soft -> Medium -> Soft", [("SOFT", 12), ("MEDIUM", 26), ("SOFT", 15)]),
    ]
    
    results = []
    for name, seq in strategies:
        res = sim.evaluate_strategy(name, seq)
        results.append(res)
    
    # Ordenar por tempo total mais rápido
    results.sort(key=lambda x: x["total_time_seconds"])
    
    for rank, res in enumerate(results, 1):
        print(f"#{rank} | {res['strategy']}")
        print(f"     Tempo Total : {format_time(res['total_time_seconds'])}")
        print(f"     Média/Volta : {res['avg_lap']}s | Paragens: {res['pit_stops']}")
        print("-" * 55)
