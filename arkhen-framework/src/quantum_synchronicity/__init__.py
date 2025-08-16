"""
Quantum Synchronicity Module - Framework Arkhen v2.0

Implementa mecanismos físicos para sincronicidade quântica baseado em:
- Formalismo matemático Sᵢⱼ = ⟨ψᵢ|ψⱼ⟩/(|ψᵢ||ψⱼ|)
- Entrelaçamento em larga escala
- Experimentos com átomos ultrafrios
- Redes quânticas para validação experimental
"""

from .core import (
    QuantumSynchronizer,
    SynchronicityMeasure,
    EntanglementNetwork,
    SyncParameter
)

from .experiments import (
    UltracoldAtomExperiment,
    QuantumNetworkValidator,
    EntanglementDetector
)

from .analysis import (
    SynchronicityAnalyzer,
    CorrelationMapper,
    QuantumCoherenceTracker
)

__version__ = "2.0.0"
__all__ = [
    "QuantumSynchronizer",
    "SynchronicityMeasure", 
    "EntanglementNetwork",
    "SyncParameter",
    "UltracoldAtomExperiment",
    "QuantumNetworkValidator",
    "EntanglementDetector",
    "SynchronicityAnalyzer",
    "CorrelationMapper",
    "QuantumCoherenceTracker"
]