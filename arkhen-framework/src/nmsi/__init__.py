"""
NMSI - New Subquantum Informational Mechanics

Implementação da mecânica informacional subquântica conforme descrita por Lazarev (2025).
Este módulo fornece as fundações teóricas e computacionais para o Framework Arkhen v2.0.
"""

from .core import (
    SubquantumField,
    InformationalOscillator,
    CoherenceFunction,
    NMSISimulator
)

from .equations import (
    compute_field_function,
    compute_coherence,
    compute_phase_difference,
    compute_information_density
)

from .visualization import (
    plot_field_evolution,
    plot_coherence_map,
    plot_oscillatory_universe
)

__version__ = "2.0.0"
__all__ = [
    "SubquantumField",
    "InformationalOscillator", 
    "CoherenceFunction",
    "NMSISimulator",
    "compute_field_function",
    "compute_coherence",
    "compute_phase_difference",
    "compute_information_density",
    "plot_field_evolution",
    "plot_coherence_map", 
    "plot_oscillatory_universe"
]