"""
Core Framework Module - Framework Arkhen v2.0

Integra todos os vetores em um sistema unificado.
"""

from .framework import (
    ArkhenFramework,
    FrameworkConfig,
    SimulationEngine
)

from .parallax import (
    ParallaxCore,
    InferenceOrchestrator,
    DistributedLLM
)

from .lattica import (
    LatticaTransport,
    PeerToPeerNetwork,
    TensorStreamCompression
)

__version__ = "2.0.0"
__all__ = [
    "ArkhenFramework",
    "FrameworkConfig",
    "SimulationEngine",
    "ParallaxCore",
    "InferenceOrchestrator", 
    "DistributedLLM",
    "LatticaTransport",
    "PeerToPeerNetwork",
    "TensorStreamCompression"
]