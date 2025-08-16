"""
Quantum Blockchain Module - Framework Arkhen v2.0

Implementa sistema de blockchain quântico com:
- Protocolo PoQC (Proof-of-Quantum-Coherence)
- Detecção de comportamento fraudulento
- Interfaces interdimensionais
- Consenso quântico distribuído
"""

from .core import (
    QuantumBlock,
    QuantumBlockchain,
    QuantumNode,
    QuantumConsensus
)

from .consensus import (
    PoQCConsensus,
    compute_coherence_parameter,
    compute_fraud_probability,
    validate_quantum_proof
)

from .interfaces import (
    DimensionalInterface,
    QuantumSingularity,
    InterdimensionalBridge
)

from .network import (
    QuantumNetwork,
    QuantumPeer,
    QuantumMessage
)

__version__ = "2.0.0"
__all__ = [
    "QuantumBlock",
    "QuantumBlockchain", 
    "QuantumNode",
    "QuantumConsensus",
    "PoQCConsensus",
    "compute_coherence_parameter",
    "compute_fraud_probability",
    "validate_quantum_proof",
    "DimensionalInterface",
    "QuantumSingularity",
    "InterdimensionalBridge",
    "QuantumNetwork",
    "QuantumPeer",
    "QuantumMessage"
]