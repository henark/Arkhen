"""
Universe Simulation Module - Framework Arkhen v2.0

Implementa simulação de universo oscilatório baseado em:
- Modelo alternativo ao Big Bang
- Tensor Networks Quânticas
- Wheeler-DeWitt Equation solver
- Métodos VQE (Variational Quantum Eigensolver)
"""

from .core import (
    OscillatoryUniverse,
    UniverseSimulator,
    CosmologicalParameters,
    WaveFunction
)

from .wheeler_dewitt import (
    WheelerDeWittSolver,
    QuantumGravitySimulator,
    HamiltonianConstraint
)

from .tensor_networks import (
    QuantumTensorNetwork,
    TensorNetworkSimulator,
    VariationalQuantumEigensolver
)

from .cosmology import (
    DarkMatterAnalyzer,
    DarkEnergyCalculator,
    CosmicInflationModel
)

__version__ = "2.0.0"
__all__ = [
    "OscillatoryUniverse",
    "UniverseSimulator", 
    "CosmologicalParameters",
    "WaveFunction",
    "WheelerDeWittSolver",
    "QuantumGravitySimulator",
    "HamiltonianConstraint",
    "QuantumTensorNetwork",
    "TensorNetworkSimulator", 
    "VariationalQuantumEigensolver",
    "DarkMatterAnalyzer",
    "DarkEnergyCalculator",
    "CosmicInflationModel"
]