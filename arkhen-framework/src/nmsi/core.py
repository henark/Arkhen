"""
Core classes for NMSI (New Subquantum Informational Mechanics)

Implementa as equações fundamentais:
Ψ(r,t) = Φ₀ exp[i(k·r - ωt + ϕ(r,t))] · Ω(r,t)
Ω(r,t) = tanh(⟨I(r,t)⟩/I_c)
"""

import numpy as np
from typing import Tuple, Optional, Callable
from dataclasses import dataclass
import scipy.sparse as sp
from scipy.integrate import odeint


@dataclass
class NMSIParameters:
    """Parâmetros fundamentais do NMSI"""
    phi_0: float = 1.0  # Amplitude da oscilação informacional
    k_vector: np.ndarray = None  # Vetor de onda
    omega: float = 1.0  # Frequência angular
    I_c: float = 1.0  # Limite crítico para manifestação física
    planck_scale: float = 1e-35  # Escala de Planck (metros)
    
    def __post_init__(self):
        if self.k_vector is None:
            self.k_vector = np.array([1.0, 0.0, 0.0])


class SubquantumField:
    """
    Campo informacional subquântico que forma a base da realidade física.
    
    Implementa a função de campo fundamental:
    Ψ(r,t) = Φ₀ exp[i(k·r - ωt + ϕ(r,t))] · Ω(r,t)
    """
    
    def __init__(self, parameters: NMSIParameters):
        self.params = parameters
        self.coherence_func = CoherenceFunction(parameters)
        
    def compute_field(self, r: np.ndarray, t: float, 
                     phase_func: Optional[Callable] = None) -> complex:
        """
        Calcula a função de campo em posição r e tempo t
        
        Args:
            r: Posição (vetor 3D)
            t: Tempo
            phase_func: Função de fase opcional ϕ(r,t)
        
        Returns:
            Valor complexo do campo Ψ(r,t)
        """
        # Produto escalar k·r
        k_dot_r = np.dot(self.params.k_vector, r)
        
        # Fase adicional (se fornecida)
        additional_phase = phase_func(r, t) if phase_func else 0.0
        
        # Fase total
        total_phase = k_dot_r - self.params.omega * t + additional_phase
        
        # Função de coerência
        coherence = self.coherence_func.compute(r, t)
        
        # Campo completo
        field = (self.params.phi_0 * 
                np.exp(1j * total_phase) * 
                coherence)
        
        return field
    
    def compute_field_grid(self, x_range: Tuple[float, float], 
                          y_range: Tuple[float, float],
                          t: float, grid_size: int = 100) -> np.ndarray:
        """Calcula o campo em uma grade 2D"""
        x = np.linspace(x_range[0], x_range[1], grid_size)
        y = np.linspace(y_range[0], y_range[1], grid_size)
        X, Y = np.meshgrid(x, y)
        
        field_grid = np.zeros((grid_size, grid_size), dtype=complex)
        
        for i in range(grid_size):
            for j in range(grid_size):
                r = np.array([X[i, j], Y[i, j], 0.0])
                field_grid[i, j] = self.compute_field(r, t)
                
        return field_grid


class InformationalOscillator:
    """
    Oscilador informacional que modela as flutuações subquânticas.
    Representa um modo fundamental de oscilação do substrato informacional.
    """
    
    def __init__(self, frequency: float, amplitude: float = 1.0):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = 0.0
        
    def evolve(self, dt: float):
        """Evolui o oscilador por um passo de tempo dt"""
        self.phase += 2 * np.pi * self.frequency * dt
        self.phase = self.phase % (2 * np.pi)
        
    def get_value(self, t: float) -> complex:
        """Retorna o valor do oscilador no tempo t"""
        return self.amplitude * np.exp(1j * (2 * np.pi * self.frequency * t + self.phase))
    
    def get_information_content(self) -> float:
        """Calcula o conteúdo informacional do oscilador"""
        return np.log2(self.amplitude + 1e-10)  # Evita log(0)


class CoherenceFunction:
    """
    Função de coerência que determina a transição informação → realidade física.
    
    Implementa: Ω(r,t) = tanh(⟨I(r,t)⟩/I_c)
    """
    
    def __init__(self, parameters: NMSIParameters):
        self.params = parameters
        self.information_field = None
        
    def compute_information_density(self, r: np.ndarray, t: float,
                                  oscillators: list = None) -> float:
        """
        Calcula a densidade informacional ⟨I(r,t)⟩ em uma posição e tempo.
        
        Args:
            r: Posição
            t: Tempo  
            oscillators: Lista de osciladores informacionais
        
        Returns:
            Densidade informacional
        """
        if oscillators is None:
            # Modelo simples: densidade baseada na distância
            distance = np.linalg.norm(r)
            return np.exp(-distance / self.params.planck_scale)
        
        # Soma das contribuições de todos os osciladores
        total_info = 0.0
        for osc in oscillators:
            value = osc.get_value(t)
            # Peso espacial (decaimento com distância)
            spatial_weight = np.exp(-np.linalg.norm(r) / self.params.planck_scale)
            total_info += abs(value)**2 * spatial_weight
            
        return total_info
    
    def compute(self, r: np.ndarray, t: float, 
               oscillators: list = None) -> float:
        """
        Calcula a função de coerência Ω(r,t).
        
        Returns:
            Valor da função de coerência (real, entre 0 e 1)
        """
        info_density = self.compute_information_density(r, t, oscillators)
        coherence = np.tanh(info_density / self.params.I_c)
        return coherence


class NMSISimulator:
    """
    Simulador completo do NMSI integrando todos os componentes.
    Permite simulações de evolução temporal e análise de propriedades emergentes.
    """
    
    def __init__(self, parameters: NMSIParameters):
        self.params = parameters
        self.field = SubquantumField(parameters)
        self.oscillators = []
        self.time = 0.0
        self.history = []
        
    def add_oscillator(self, frequency: float, amplitude: float = 1.0):
        """Adiciona um oscilador informacional ao sistema"""
        osc = InformationalOscillator(frequency, amplitude)
        self.oscillators.append(osc)
        
    def step(self, dt: float):
        """Executa um passo de simulação"""
        # Evolui todos os osciladores
        for osc in self.oscillators:
            osc.evolve(dt)
            
        # Atualiza tempo
        self.time += dt
        
        # Salva estado atual
        self.history.append({
            'time': self.time,
            'total_information': self.compute_total_information(),
            'avg_coherence': self.compute_average_coherence()
        })
        
    def run_simulation(self, duration: float, dt: float = 0.01):
        """Executa simulação por uma duração especificada"""
        steps = int(duration / dt)
        
        for _ in range(steps):
            self.step(dt)
            
    def compute_total_information(self) -> float:
        """Calcula o conteúdo informacional total do sistema"""
        total = 0.0
        for osc in self.oscillators:
            total += osc.get_information_content()
        return total
    
    def compute_average_coherence(self, n_samples: int = 100) -> float:
        """Calcula a coerência média em pontos aleatórios do espaço"""
        coherence_sum = 0.0
        
        for _ in range(n_samples):
            # Ponto aleatório no espaço
            r = np.random.randn(3) * self.params.planck_scale
            coherence = self.field.coherence_func.compute(r, self.time, self.oscillators)
            coherence_sum += coherence
            
        return coherence_sum / n_samples
    
    def get_phase_difference_map(self, grid_size: int = 50) -> np.ndarray:
        """
        Calcula mapa de diferenças de fase para identificar domínios de matéria/energia escura.
        Δϕ ≈ π indica transição entre domínios.
        """
        x = np.linspace(-10*self.params.planck_scale, 10*self.params.planck_scale, grid_size)
        y = np.linspace(-10*self.params.planck_scale, 10*self.params.planck_scale, grid_size)
        
        phase_map = np.zeros((grid_size, grid_size))
        
        for i in range(grid_size):
            for j in range(grid_size):
                r = np.array([x[i], y[j], 0.0])
                field_value = self.field.compute_field(r, self.time)
                phase_map[i, j] = np.angle(field_value)
                
        return phase_map
    
    def analyze_dark_matter_signature(self) -> dict:
        """
        Analisa assinaturas de matéria escura baseada em diferenças de fase.
        Retorna estatísticas dos domínios encontrados.
        """
        phase_map = self.get_phase_difference_map()
        
        # Identifica regiões com diferença de fase próxima a π
        dark_matter_mask = np.abs(phase_map - np.pi) < 0.1
        dark_energy_mask = np.abs(phase_map) < 0.1
        
        return {
            'dark_matter_fraction': np.sum(dark_matter_mask) / phase_map.size,
            'dark_energy_fraction': np.sum(dark_energy_mask) / phase_map.size,
            'total_domains': np.sum(dark_matter_mask) + np.sum(dark_energy_mask),
            'phase_variance': np.var(phase_map)
        }