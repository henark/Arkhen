"""
Quantum Consensus Mechanisms

Implementa o protocolo PoQC (Proof-of-Quantum-Coherence) conforme descrito no framework:
C = (1/N) ∑ᵢ₌₁ᴺ ∏ⱼ₌₁ᴺ σᵢⱼ
P_fraud = 1 - e^(-λΔC)
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import hashlib
import time
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import random_statevector, Statevector
from qiskit.quantum_info.operators import Pauli
import asyncio


@dataclass
class QuantumProof:
    """Prova quântica para o protocolo PoQC"""
    node_id: str
    timestamp: float
    quantum_state: np.ndarray
    pauli_measurements: Dict[str, float]
    coherence_value: float
    signature: str
    
    def to_dict(self) -> dict:
        return {
            'node_id': self.node_id,
            'timestamp': self.timestamp,
            'quantum_state': self.quantum_state.tolist(),
            'pauli_measurements': self.pauli_measurements,
            'coherence_value': self.coherence_value,
            'signature': self.signature
        }


class QuantumStateManager:
    """Gerencia estados quânticos dos nós da rede"""
    
    def __init__(self, n_qubits: int = 4):
        self.n_qubits = n_qubits
        self.states = {}
        
    def create_random_state(self, node_id: str) -> np.ndarray:
        """Cria estado quântico aleatório para um nó"""
        state = random_statevector(2**self.n_qubits)
        self.states[node_id] = state.data
        return state.data
    
    def get_state(self, node_id: str) -> Optional[np.ndarray]:
        """Retorna estado quântico de um nó"""
        return self.states.get(node_id)
    
    def update_state(self, node_id: str, new_state: np.ndarray):
        """Atualiza estado quântico de um nó"""
        self.states[node_id] = new_state


def compute_pauli_measurement(state1: np.ndarray, state2: np.ndarray, 
                            pauli_op: str = 'Z') -> float:
    """
    Calcula medida de Pauli entre dois estados quânticos.
    
    Args:
        state1, state2: Estados quânticos
        pauli_op: Operador de Pauli ('X', 'Y', 'Z')
    
    Returns:
        Valor da medida σᵢⱼ
    """
    # Converte para objetos Statevector do Qiskit
    psi1 = Statevector(state1)
    psi2 = Statevector(state2)
    
    # Cria operador de Pauli
    n_qubits = int(np.log2(len(state1)))
    pauli = Pauli(pauli_op * n_qubits)
    
    # Calcula valor esperado
    expectation1 = psi1.expectation_value(pauli).real
    expectation2 = psi2.expectation_value(pauli).real
    
    # Retorna produto das medidas
    return expectation1 * expectation2


def compute_coherence_parameter(nodes_states: Dict[str, np.ndarray]) -> float:
    """
    Calcula parâmetro de coerência quântica:
    C = (1/N) ∑ᵢ₌₁ᴺ ∏ⱼ₌₁ᴺ σᵢⱼ
    
    Args:
        nodes_states: Dicionário {node_id: quantum_state}
    
    Returns:
        Parâmetro de coerência C
    """
    node_ids = list(nodes_states.keys())
    N = len(node_ids)
    
    if N < 2:
        return 1.0
    
    total_coherence = 0.0
    
    for i in range(N):
        node_product = 1.0
        state_i = nodes_states[node_ids[i]]
        
        for j in range(N):
            if i != j:
                state_j = nodes_states[node_ids[j]]
                sigma_ij = compute_pauli_measurement(state_i, state_j)
                node_product *= sigma_ij
                
        total_coherence += node_product
    
    return total_coherence / N


def compute_fraud_probability(coherence_current: float, 
                            coherence_baseline: float,
                            lambda_param: float = 1.0) -> float:
    """
    Calcula probabilidade de detecção de comportamento fraudulento:
    P_fraud = 1 - e^(-λΔC)
    
    Args:
        coherence_current: Coerência atual
        coherence_baseline: Coerência de referência
        lambda_param: Parâmetro de sensibilidade
    
    Returns:
        Probabilidade de fraude (0-1)
    """
    delta_C = abs(coherence_current - coherence_baseline)
    return 1.0 - np.exp(-lambda_param * delta_C)


class PoQCConsensus:
    """
    Protocolo de Consenso Proof-of-Quantum-Coherence
    
    Implementa validação baseada em coerência quântica entre nós da rede.
    """
    
    def __init__(self, lambda_param: float = 1.0, fraud_threshold: float = 0.7):
        self.lambda_param = lambda_param
        self.fraud_threshold = fraud_threshold
        self.state_manager = QuantumStateManager()
        self.baseline_coherence = None
        self.validators = []
        
    def register_validator(self, node_id: str) -> str:
        """Registra um nó como validador"""
        if node_id not in self.validators:
            self.validators.append(node_id)
            # Cria estado quântico inicial
            self.state_manager.create_random_state(node_id)
            return f"Validator {node_id} registered successfully"
        return f"Validator {node_id} already registered"
    
    def generate_quantum_proof(self, node_id: str) -> QuantumProof:
        """Gera prova quântica para um nó validador"""
        if node_id not in self.validators:
            raise ValueError(f"Node {node_id} is not a registered validator")
        
        # Obtém estado atual do nó
        quantum_state = self.state_manager.get_state(node_id)
        
        # Calcula medidas de Pauli com outros nós
        pauli_measurements = {}
        for other_node in self.validators:
            if other_node != node_id:
                other_state = self.state_manager.get_state(other_node)
                if other_state is not None:
                    sigma_val = compute_pauli_measurement(quantum_state, other_state)
                    pauli_measurements[other_node] = sigma_val
        
        # Calcula coerência atual
        all_states = {nid: self.state_manager.get_state(nid) 
                     for nid in self.validators 
                     if self.state_manager.get_state(nid) is not None}
        coherence_value = compute_coherence_parameter(all_states)
        
        # Gera assinatura
        proof_data = f"{node_id}{time.time()}{coherence_value}"
        signature = hashlib.sha256(proof_data.encode()).hexdigest()
        
        return QuantumProof(
            node_id=node_id,
            timestamp=time.time(),
            quantum_state=quantum_state,
            pauli_measurements=pauli_measurements,
            coherence_value=coherence_value,
            signature=signature
        )
    
    def validate_quantum_proof(self, proof: QuantumProof) -> Tuple[bool, str]:
        """Valida uma prova quântica"""
        try:
            # Verifica se o nó é validador registrado
            if proof.node_id not in self.validators:
                return False, "Node is not a registered validator"
            
            # Verifica timestamp (não pode ser muito antigo)
            current_time = time.time()
            if current_time - proof.timestamp > 300:  # 5 minutos
                return False, "Proof is too old"
            
            # Reconstrói estados para verificação
            all_states = {nid: self.state_manager.get_state(nid) 
                         for nid in self.validators 
                         if self.state_manager.get_state(nid) is not None}
            
            # Calcula coerência esperada
            expected_coherence = compute_coherence_parameter(all_states)
            
            # Verifica se coerência na prova está próxima da esperada
            coherence_diff = abs(proof.coherence_value - expected_coherence)
            if coherence_diff > 0.1:  # Tolerância
                return False, f"Coherence mismatch: {coherence_diff}"
            
            # Calcula probabilidade de fraude
            if self.baseline_coherence is not None:
                fraud_prob = compute_fraud_probability(
                    proof.coherence_value, 
                    self.baseline_coherence, 
                    self.lambda_param
                )
                
                if fraud_prob > self.fraud_threshold:
                    return False, f"High fraud probability: {fraud_prob:.3f}"
            
            return True, "Proof validated successfully"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def update_baseline_coherence(self):
        """Atualiza coerência de referência baseada nos validadores ativos"""
        all_states = {nid: self.state_manager.get_state(nid) 
                     for nid in self.validators 
                     if self.state_manager.get_state(nid) is not None}
        
        if len(all_states) >= 2:
            self.baseline_coherence = compute_coherence_parameter(all_states)
    
    async def run_consensus_round(self) -> Dict[str, any]:
        """Executa uma rodada completa de consenso"""
        results = {
            'timestamp': time.time(),
            'participating_validators': [],
            'proofs': [],
            'consensus_achieved': False,
            'average_coherence': 0.0,
            'fraud_detections': []
        }
        
        # Gera provas de todos os validadores
        valid_proofs = []
        for validator in self.validators:
            try:
                proof = self.generate_quantum_proof(validator)
                is_valid, message = self.validate_quantum_proof(proof)
                
                if is_valid:
                    valid_proofs.append(proof)
                    results['participating_validators'].append(validator)
                else:
                    results['fraud_detections'].append({
                        'validator': validator,
                        'reason': message
                    })
                    
                results['proofs'].append(proof.to_dict())
                
            except Exception as e:
                results['fraud_detections'].append({
                    'validator': validator,
                    'reason': f"Error generating proof: {str(e)}"
                })
        
        # Calcula estatísticas
        if valid_proofs:
            coherences = [proof.coherence_value for proof in valid_proofs]
            results['average_coherence'] = np.mean(coherences)
            
            # Consenso é alcançado se maioria dos validadores participou
            participation_rate = len(valid_proofs) / len(self.validators)
            results['consensus_achieved'] = participation_rate >= 0.51  # Maioria simples
            
            # Atualiza baseline se consenso foi alcançado
            if results['consensus_achieved']:
                self.update_baseline_coherence()
        
        return results


def validate_quantum_proof(proof_data: dict, consensus: PoQCConsensus) -> Tuple[bool, str]:
    """Função auxiliar para validar prova quântica a partir de dados serializados"""
    try:
        proof = QuantumProof(
            node_id=proof_data['node_id'],
            timestamp=proof_data['timestamp'],
            quantum_state=np.array(proof_data['quantum_state']),
            pauli_measurements=proof_data['pauli_measurements'],
            coherence_value=proof_data['coherence_value'],
            signature=proof_data['signature']
        )
        return consensus.validate_quantum_proof(proof)
    except Exception as e:
        return False, f"Invalid proof format: {str(e)}"