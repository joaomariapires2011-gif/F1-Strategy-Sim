from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from f1_strategy_sim import F1StrategySimulator

app = FastAPI(
    title="ApexMetrics & F1 Strategy Engine API",
    description="Backend de telemetria e simulação de corrida",
    version="1.0.0"
)

# Permite que o frontend (React/Lovable) se ligue a esta API sem bloqueios de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StintInput(BaseModel):
    compound: str
    laps: int

class SimulationRequest(BaseModel):
    total_laps: int = 53
    pit_loss_seconds: float = 22.5
    stints: List[StintInput]

@app.get("/health")
def health_check():
    return {"status": "online", "engine": "FastAPI", "version": "1.0.0"}

@app.post("/api/v1/simulate")
def run_simulation(data: SimulationRequest):
    total_stint_laps = sum(s.laps for s in data.stints)
    if total_stint_laps != data.total_laps:
        raise HTTPException(
            status_code=400, 
            detail=f"A soma das voltas dos stints ({total_stint_laps}) não bate certo com o total da corrida ({data.total_laps})."
        )

    sim = F1StrategySimulator(total_laps=data.total_laps, pit_loss_seconds=data.pit_loss_seconds)
    sequence = [(s.compound.upper(), s.laps) for s in data.stints]
    
    return sim.evaluate_strategy("Custom Strategy", sequence)
