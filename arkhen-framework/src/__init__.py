"""
Framework Arkhen v2.0: Sistemas de Informação Interdimensionais

Este é o framework principal que integra todos os vetores:
1. NMSI (New Subquantum Informational Mechanics)
2. Blockchain Quântico com PoQC
3. Simulação Oscilatória do Universo
4. Sincronicidade Quântica
5. Protocolo SETI
6. Economias Autoevolutivas
7. Sistemas Autônomos

Desenvolvido por Rafael Oliveira - 2025
"""

from .nmsi import (
    NMSISimulator,
    SubquantumField,
    InformationalOscillator,
    NMSIParameters
)

from .quantum_blockchain import (
    QuantumBlockchain,
    PoQCConsensus,
    QuantumNode
)

from .universe_simulation import (
    OscillatoryUniverse,
    UniverseSimulator,
    CosmologicalParameters
)

from .quantum_synchronicity import (
    QuantumSynchronizer,
    EntanglementNetwork,
    SyncParameter
)

from .seti_protocol import (
    SETIAnalyzer,
    QuantumTelescope,
    SignalDetector
)

from .core import (
    ArkhenFramework,
    FrameworkConfig,
    SimulationEngine
)

__version__ = "2.0.0"
__author__ = "Rafael Oliveira"
__email__ = "rafael@arkhen.dev"

__all__ = [
    # Core Framework
    "ArkhenFramework",
    "FrameworkConfig", 
    "SimulationEngine",
    
    # NMSI
    "NMSISimulator",
    "SubquantumField",
    "InformationalOscillator",
    "NMSIParameters",
    
    # Quantum Blockchain
    "QuantumBlockchain",
    "PoQCConsensus",
    "QuantumNode",
    
    # Universe Simulation
    "OscillatoryUniverse",
    "UniverseSimulator",
    "CosmologicalParameters",
    
    # Quantum Synchronicity
    "QuantumSynchronizer",
    "EntanglementNetwork", 
    "SyncParameter",
    
    # SETI Protocol
    "SETIAnalyzer",
    "QuantumTelescope",
    "SignalDetector"
]

# Framework metadata
FRAMEWORK_INFO = {
    "name": "Framework Arkhen v2.0",
    "description": "Sistemas de Informação Interdimensionais",
    "version": __version__,
    "author": __author__,
    "year": 2025,
    "license": "MIT",
    "components": [
        "NMSI - New Subquantum Informational Mechanics",
        "Quantum Blockchain with PoQC Consensus",
        "Oscillatory Universe Simulation",
        "Quantum Synchronicity Networks",
        "SETI Interdimensional Communication Protocol",
        "Self-Evolving Agent Economies",
        "Autonomous Self-Regulating Systems"
    ],
    "technologies": [
        "Quantum Computing (Qiskit, Cirq, PennyLane)",
        "Tensor Networks",
        "Distributed Systems",
        "Machine Learning",
        "Cryptography",
        "Scientific Computing"
    ]
}