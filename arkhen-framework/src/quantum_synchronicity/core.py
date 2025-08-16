"""
Core Quantum Synchronicity Implementation

Implementa o formalismo matemático baseado em:
Sᵢⱼ = ⟨ψᵢ|ψⱼ⟩/(|ψᵢ||ψⱼ|)

Baseado em "Navigating the Open Oceans of Quantum Synchronicity" (OU Physics, 2025)
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass
import networkx as nx
from qiskit.quantum_info import Statevector, partial_trace, entropy
from qiskit import QuantumCircuit
import time


@dataclass
class SyncParameter:
    """Parâmetros de sincronicidade quântica"""
    coupling_strength: float = 1.0
    coherence_time: float = 100.0  # microsegundos
    entanglement_threshold: float = 0.5
    sync_frequency: float = 1.0  # Hz
    temperature: float = 0.001  # Kelvin (para átomos ultrafrios)


class SynchronicityMeasure:
    """
    Calcula medidas de sincronicidade entre sistemas quânticos.
    
    Implementa: Sᵢⱼ = ⟨ψᵢ|ψⱼ⟩/(|ψᵢ||ψⱼ|)
    """
    
    @staticmethod
    def compute_overlap(psi_i: np.ndarray, psi_j: np.ndarray) -> complex:
        """
        Calcula o produto interno ⟨ψᵢ|ψⱼ⟩
        
        Args:
            psi_i, psi_j: Estados quânticos (arrays complexos)
            
        Returns:
            Produto interno complexo
        """
        return np.vdot(psi_i, psi_j)
    
    @staticmethod
    def compute_norm(psi: np.ndarray) -> float:
        """Calcula a norma |ψ| de um estado quântico"""
        return np.linalg.norm(psi)
    
    @classmethod
    def compute_synchronicity(cls, psi_i: np.ndarray, psi_j: np.ndarray) -> float:
        """
        Calcula o grau de sincronicidade Sᵢⱼ entre dois sistemas.
        
        Args:
            psi_i, psi_j: Estados quânticos
            
        Returns:
            Grau de sincronicidade (real, 0-1)
        """
        overlap = cls.compute_overlap(psi_i, psi_j)
        norm_i = cls.compute_norm(psi_i)
        norm_j = cls.compute_norm(psi_j)
        
        if norm_i == 0 or norm_j == 0:
            return 0.0
            
        sync_value = abs(overlap) / (norm_i * norm_j)
        return min(sync_value, 1.0)  # Limita a 1.0
    
    @classmethod
    def compute_phase_synchronicity(cls, psi_i: np.ndarray, psi_j: np.ndarray) -> Tuple[float, float]:
        """
        Calcula sincronicidade de amplitude e fase separadamente.
        
        Returns:
            (amplitude_sync, phase_sync)
        """
        overlap = cls.compute_overlap(psi_i, psi_j)
        norm_i = cls.compute_norm(psi_i)
        norm_j = cls.compute_norm(psi_j)
        
        if norm_i == 0 or norm_j == 0:
            return 0.0, 0.0
        
        normalized_overlap = overlap / (norm_i * norm_j)
        
        amplitude_sync = abs(normalized_overlap)
        phase_sync = np.cos(np.angle(normalized_overlap))
        
        return amplitude_sync, phase_sync


class EntanglementNetwork:
    """
    Rede de entrelaçamento quântico para sincronicidade em larga escala.
    """
    
    def __init__(self, n_nodes: int, parameters: SyncParameter):
        self.n_nodes = n_nodes
        self.params = parameters
        self.nodes = {}
        self.graph = nx.Graph()
        self.entanglement_matrix = np.zeros((n_nodes, n_nodes))
        self.sync_history = []
        
        # Inicializa nós
        for i in range(n_nodes):
            node_id = f"node_{i}"
            self.add_node(node_id)
    
    def add_node(self, node_id: str, initial_state: Optional[np.ndarray] = None):
        """Adiciona um nó à rede"""
        if initial_state is None:
            # Estado inicial aleatório
            dim = 4  # Sistema de 2 qubits
            initial_state = np.random.complex128(dim) + 1j * np.random.random(dim)
            initial_state = initial_state / np.linalg.norm(initial_state)
        
        self.nodes[node_id] = {
            'state': initial_state,
            'last_update': time.time(),
            'sync_partners': set()
        }
        self.graph.add_node(node_id)
    
    def create_entanglement(self, node_i: str, node_j: str, strength: float = 1.0):
        """Cria entrelaçamento entre dois nós"""
        if node_i not in self.nodes or node_j not in self.nodes:
            raise ValueError("Both nodes must exist in the network")
        
        # Adiciona aresta no grafo
        self.graph.add_edge(node_i, node_j, weight=strength)
        
        # Atualiza matriz de entrelaçamento
        i_idx = list(self.nodes.keys()).index(node_i)
        j_idx = list(self.nodes.keys()).index(node_j)
        self.entanglement_matrix[i_idx, j_idx] = strength
        self.entanglement_matrix[j_idx, i_idx] = strength
        
        # Marca como parceiros sincronizados
        self.nodes[node_i]['sync_partners'].add(node_j)
        self.nodes[node_j]['sync_partners'].add(node_i)
    
    def evolve_network(self, dt: float):
        """Evolui a rede por um passo de tempo dt"""
        current_time = time.time()
        
        # Calcula sincronicidades atuais
        sync_matrix = self.compute_synchronicity_matrix()
        
        # Evolui cada nó baseado nas interações
        for node_id, node_data in self.nodes.items():
            new_state = self._evolve_node_state(
                node_id, node_data['state'], sync_matrix, dt
            )
            self.nodes[node_id]['state'] = new_state
            self.nodes[node_id]['last_update'] = current_time
        
        # Salva histórico
        self.sync_history.append({
            'time': current_time,
            'avg_sync': np.mean(sync_matrix[sync_matrix > 0]),
            'max_sync': np.max(sync_matrix),
            'network_coherence': self.compute_network_coherence()
        })
    
    def _evolve_node_state(self, node_id: str, state: np.ndarray, 
                          sync_matrix: np.ndarray, dt: float) -> np.ndarray:
        """Evolui o estado de um nó baseado nas sincronicidades"""
        node_idx = list(self.nodes.keys()).index(node_id)
        
        # Hamiltoniano de interação baseado em sincronicidades
        interaction_term = np.zeros_like(state)
        
        for partner_id in self.nodes[node_id]['sync_partners']:
            partner_idx = list(self.nodes.keys()).index(partner_id)
            partner_state = self.nodes[partner_id]['state']
            
            sync_value = sync_matrix[node_idx, partner_idx]
            coupling = self.params.coupling_strength * sync_value
            
            # Termo de acoplamento (simplificado)
            interaction_term += coupling * partner_state
        
        # Evolução unitária simples
        phase_factor = np.exp(-1j * self.params.sync_frequency * dt)
        evolved_state = phase_factor * state + dt * interaction_term
        
        # Renormaliza
        return evolved_state / np.linalg.norm(evolved_state)
    
    def compute_synchronicity_matrix(self) -> np.ndarray:
        """Calcula matriz de sincronicidades entre todos os nós"""
        n = len(self.nodes)
        sync_matrix = np.zeros((n, n))
        
        node_ids = list(self.nodes.keys())
        
        for i in range(n):
            for j in range(i + 1, n):
                state_i = self.nodes[node_ids[i]]['state']
                state_j = self.nodes[node_ids[j]]['state']
                
                sync_value = SynchronicityMeasure.compute_synchronicity(state_i, state_j)
                sync_matrix[i, j] = sync_value
                sync_matrix[j, i] = sync_value
        
        return sync_matrix
    
    def compute_network_coherence(self) -> float:
        """Calcula coerência global da rede"""
        sync_matrix = self.compute_synchronicity_matrix()
        return np.mean(sync_matrix[sync_matrix > 0])
    
    def detect_sync_clusters(self, threshold: float = 0.7) -> List[List[str]]:
        """Detecta clusters de nós altamente sincronizados"""
        sync_matrix = self.compute_synchronicity_matrix()
        node_ids = list(self.nodes.keys())
        
        # Cria grafo de sincronicidade
        sync_graph = nx.Graph()
        sync_graph.add_nodes_from(node_ids)
        
        n = len(node_ids)
        for i in range(n):
            for j in range(i + 1, n):
                if sync_matrix[i, j] > threshold:
                    sync_graph.add_edge(node_ids[i], node_ids[j], 
                                      weight=sync_matrix[i, j])
        
        # Encontra componentes conectados
        clusters = list(nx.connected_components(sync_graph))
        return [list(cluster) for cluster in clusters]


class QuantumSynchronizer:
    """
    Sistema principal de sincronização quântica.
    Orquestra redes de entrelaçamento e análises de sincronicidade.
    """
    
    def __init__(self, parameters: SyncParameter):
        self.params = parameters
        self.networks = {}
        self.experiments = []
        self.global_sync_data = []
    
    def create_network(self, network_id: str, n_nodes: int) -> EntanglementNetwork:
        """Cria uma nova rede de entrelaçamento"""
        network = EntanglementNetwork(n_nodes, self.params)
        self.networks[network_id] = network
        return network
    
    def run_synchronization_experiment(self, network_id: str, 
                                     duration: float, dt: float = 0.01) -> Dict:
        """
        Executa experimento de sincronização em uma rede.
        
        Args:
            network_id: ID da rede
            duration: Duração do experimento em segundos
            dt: Passo de tempo
            
        Returns:
            Dados do experimento
        """
        if network_id not in self.networks:
            raise ValueError(f"Network {network_id} not found")
        
        network = self.networks[network_id]
        start_time = time.time()
        
        # Estado inicial
        initial_coherence = network.compute_network_coherence()
        
        # Executa evolução
        steps = int(duration / dt)
        for step in range(steps):
            network.evolve_network(dt)
        
        # Estado final
        final_coherence = network.compute_network_coherence()
        sync_clusters = network.detect_sync_clusters()
        
        experiment_data = {
            'network_id': network_id,
            'start_time': start_time,
            'duration': duration,
            'steps': steps,
            'initial_coherence': initial_coherence,
            'final_coherence': final_coherence,
            'coherence_change': final_coherence - initial_coherence,
            'sync_clusters': sync_clusters,
            'history': network.sync_history[-steps:],
            'final_sync_matrix': network.compute_synchronicity_matrix().tolist()
        }
        
        self.experiments.append(experiment_data)
        return experiment_data
    
    def analyze_global_synchronicity(self) -> Dict:
        """Analisa sincronicidade global entre todas as redes"""
        if not self.networks:
            return {'error': 'No networks available'}
        
        # Calcula sincronicidade entre redes
        network_ids = list(self.networks.keys())
        inter_network_sync = {}
        
        for i, net_i in enumerate(network_ids):
            for j, net_j in enumerate(network_ids[i+1:], i+1):
                # Sincronicidade média entre nós de diferentes redes
                sync_values = []
                
                for node_i in self.networks[net_i].nodes:
                    for node_j in self.networks[net_j].nodes:
                        state_i = self.networks[net_i].nodes[node_i]['state']
                        state_j = self.networks[net_j].nodes[node_j]['state']
                        
                        sync = SynchronicityMeasure.compute_synchronicity(state_i, state_j)
                        sync_values.append(sync)
                
                inter_network_sync[f"{net_i}_{net_j}"] = {
                    'mean_sync': np.mean(sync_values),
                    'max_sync': np.max(sync_values),
                    'std_sync': np.std(sync_values)
                }
        
        # Coerência global
        all_coherences = [net.compute_network_coherence() 
                         for net in self.networks.values()]
        
        global_analysis = {
            'timestamp': time.time(),
            'num_networks': len(self.networks),
            'inter_network_sync': inter_network_sync,
            'global_coherence': np.mean(all_coherences),
            'coherence_variance': np.var(all_coherences),
            'networks_status': {
                net_id: {
                    'num_nodes': len(net.nodes),
                    'coherence': net.compute_network_coherence(),
                    'num_entangled_pairs': net.graph.number_of_edges()
                }
                for net_id, net in self.networks.items()
            }
        }
        
        self.global_sync_data.append(global_analysis)
        return global_analysis