"""
SETI Protocol Module - Framework Arkhen v2.0

Implementa protocolo de comunicação interdimensional baseado em:
- Detecção quântica de sinais
- Análise informacional usando teoria da informação
- Telescópios quânticos para padrões não naturais
- Reanálise do sinal Wow! com técnicas quânticas
- Colaboração com SETI Forward
"""

from .core import (
    QuantumTelescope,
    SETIAnalyzer,
    SignalDetector,
    InformationDecoder
)

from .signal_analysis import (
    WowSignalAnalyzer,
    PatternRecognizer,
    QuantumSignalProcessor,
    EntropyCalculator
)

from .communication import (
    InterdimensionalTransmitter,
    QuantumReceiver,
    MessageEncoder,
    ProtocolHandler
)

__version__ = "2.0.0"
__all__ = [
    "QuantumTelescope",
    "SETIAnalyzer",
    "SignalDetector", 
    "InformationDecoder",
    "WowSignalAnalyzer",
    "PatternRecognizer",
    "QuantumSignalProcessor",
    "EntropyCalculator",
    "InterdimensionalTransmitter",
    "QuantumReceiver",
    "MessageEncoder",
    "ProtocolHandler"
]