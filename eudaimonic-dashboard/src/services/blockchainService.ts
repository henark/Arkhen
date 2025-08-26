// SERVIÇO DE BLOCKCHAIN - PONTE ENTRE O MUNDO DIGITAL E FÍSICO
// Este serviço implementa os princípios Eudaimónicos na interação com a blockchain
// Autopoiese: Gestão robusta de estados e erros
// Transparência Estrutural: Operações claras e auditáveis

import { createPublicClient, createWalletClient, custom, getContract } from 'viem';
import { localhost } from 'viem/chains';
import {
  Member,
  Proposal,
  SystemStats,
  VotingCreditsInfo,
  SystemHealth,
  EnergyGridEvent
} from '@/types/energyGrid';

// Declaração para window.ethereum (MetaMask)
declare global {
  interface Window {
    ethereum?: unknown;
  }
}

// ABI do contrato EnergyGridDAO (extraído do contrato Solidity)
const ENERGY_GRID_ABI = [
  // Eventos (Sistema Nervoso do Contrato)
  {
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "member", "type": "address" },
      { "indexed": false, "name": "timestamp", "type": "uint256" }
    ],
    "name": "MemberRegistered",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "member", "type": "address" },
      { "indexed": false, "name": "amount", "type": "uint256" },
      { "indexed": false, "name": "creditsEarned", "type": "uint256" }
    ],
    "name": "EnergyProduced",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "proposalId", "type": "uint256" },
      { "indexed": true, "name": "voter", "type": "address" },
      { "indexed": false, "name": "support", "type": "bool" },
      { "indexed": false, "name": "intensity", "type": "uint256" },
      { "indexed": false, "name": "cost", "type": "uint256" }
    ],
    "name": "QuadraticVoteCast",
    "type": "event"
  },
  // Funções de Leitura (View Functions)
  {
    "inputs": [{ "name": "member", "type": "address" }],
    "name": "getMemberInfo",
    "outputs": [
      { "name": "isRegistered", "type": "bool" },
      { "name": "energyCredits", "type": "uint256" },
      { "name": "invalidReportsCount", "type": "uint256" },
      { "name": "isTemporarilySuspended", "type": "bool" }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getSystemStats",
    "outputs": [
      { "name": "totalProduced", "type": "uint256" },
      { "name": "totalCredits", "type": "uint256" },
      { "name": "totalMembers", "type": "uint256" },
      { "name": "currentFeeRate", "type": "uint256" }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [{ "name": "proposalId", "type": "uint256" }],
    "name": "getProposal",
    "outputs": [
      { "name": "proposer", "type": "address" },
      { "name": "description", "type": "string" },
      { "name": "yesVotes", "type": "uint256" },
      { "name": "noVotes", "type": "uint256" },
      { "name": "endTime", "type": "uint256" },
      { "name": "executed", "type": "bool" }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [{ "name": "member", "type": "address" }],
    "name": "getVotingCreditsInfo",
    "outputs": [
      { "name": "currentCredits", "type": "uint256" },
      { "name": "maxCredits", "type": "uint256" },
      { "name": "monthsUntilNext", "type": "uint256" }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  // Funções de Escrita (State-Changing Functions)
  {
    "inputs": [],
    "name": "registerMember",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [{ "name": "energyAmount", "type": "uint256" }],
    "name": "reportEnergyProduction",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "name": "to", "type": "address" },
      { "name": "amount", "type": "uint256" }
    ],
    "name": "transferCredits",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [{ "name": "description", "type": "string" }],
    "name": "createProposal",
    "outputs": [{ "name": "proposalId", "type": "uint256" }],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "name": "proposalId", "type": "uint256" },
      { "name": "support", "type": "bool" },
      { "name": "intensity", "type": "uint256" }
    ],
    "name": "voteQuadratic",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "name": "to", "type": "address" },
      { "name": "amount", "type": "uint256" }
    ],
    "name": "donateVotingCredits",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
] as const;

// Configuração do contrato (em produção, vem de variáveis de ambiente)
const CONTRACT_ADDRESS = (typeof window !== 'undefined' && (window as { [key: string]: unknown }).CONTRACT_ADDRESS as `0x${string}`) || '0x0000000000000000000000000000000000000000' as `0x${string}`;
const CHAIN = localhost; // ou mainnet para produção

export class EnergyGridService {
  private publicClient: ReturnType<typeof createPublicClient> | null;
  private walletClient: ReturnType<typeof createWalletClient> | null;
  private contract: ReturnType<typeof getContract> | null;

  constructor() {
    // Verificação de ambiente para window.ethereum
    if (typeof window === 'undefined' || !window.ethereum) {
      // No ambiente servidor (SSR) ou sem wallet, não inicializamos
      this.publicClient = null;
      this.walletClient = null;
      this.contract = null;
      return;
    }

    // Cliente público para leituras (sem wallet necessário)
    this.publicClient = createPublicClient({
      chain: CHAIN,
      transport: custom(window.ethereum!)
    });

    // Cliente wallet para escritas (requer MetaMask/wallet conectada)
    this.walletClient = createWalletClient({
      chain: CHAIN,
      transport: custom(window.ethereum!)
    });

    // Instância do contrato
    this.contract = getContract({
      address: CONTRACT_ADDRESS,
      abi: ENERGY_GRID_ABI,
      client: { public: this.publicClient, wallet: this.walletClient }
    });
  }

  // ==========================================
  // FUNÇÕES DE LEITURA (Consciência Sistémica)
  // ==========================================

  /**
   * Obtém informações completas de um membro
   * Implementa o princípio da Transparência Estrutural
   */
  async getMemberInfo(address: string): Promise<Member | null> {
    debugLog('getMemberInfo called for address:', address);
    try {
      const result = await this.contract.read.getMemberInfo([address as `0x${string}`]);
      debugLog('getMemberInfo result:', result);
      
      // Se não está registrado, retorna null
      if (!result[0]) return null;

      // Simula os dados completos de membro (em produção, seria múltiplas chamadas)
      const memberInfo = {
        address,
        isRegistered: result[0],
        energyCredits: result[1],
        invalidReportsCount: result[2],
        isTemporarilySuspended: result[3],
        lastReportTimestamp: BigInt(0), // Requer chamada adicional
        votingCredits: BigInt(100), // Requer chamada adicional  
        lastVotingCreditsUpdate: BigInt(Date.now() / 1000)
      };
      debugLog('getMemberInfo processed info:', memberInfo);
      return memberInfo;
    } catch (error) {
      console.error('Erro ao obter informações do membro:', error);
      debugLog('Error in getMemberInfo:', error);
      return null;
    }
  }

  /**
   * Obtém estatísticas sistémicas globais
   * Base para o Medidor de Resiliência (Autopoiese)
   */
  async getSystemStats(): Promise<SystemStats> {
    debugLog('getSystemStats called');
    try {
      const result = await this.contract.read.getSystemStats();
      debugLog('getSystemStats result:', result);
      
      const stats = {
        totalProduced: result[0],
        totalCredits: result[1], 
        totalMembers: result[2],
        currentFeeRate: result[3]
      };
      debugLog('getSystemStats processed stats:', stats);
      return stats;
    } catch (error) {
      console.error('Erro ao obter estatísticas do sistema:', error);
      debugLog('Error in getSystemStats:', error);
      throw new Error('Falha na comunicação com a rede');
    }
  }

  /**
   * Obtém informações de uma proposta específica
   * Componente da Metacognição (Governança)
   */
  async getProposal(proposalId: bigint): Promise<Proposal | null> {
    debugLog('getProposal called for ID:', proposalId);
    try {
      const result = await this.contract.read.getProposal([proposalId]);
      debugLog('getProposal result:', result);
      
      const proposal = {
        id: proposalId,
        proposer: result[0],
        description: result[1],
        yesVotes: result[2],
        noVotes: result[3],
        endTime: result[4],
        executed: result[5]
      };
      debugLog('getProposal processed proposal:', proposal);
      return proposal;
    } catch (error) {
      console.error('Erro ao obter proposta:', error);
      debugLog('Error in getProposal:', error);
      return null;
    }
  }

  /**
   * Obtém créditos de votação de um membro
   * Suporte para Votação Quadrática (Ressonância Semântica)
   */
  async getVotingCreditsInfo(address: string): Promise<VotingCreditsInfo> {
    debugLog('getVotingCreditsInfo called for address:', address);
    try {
      const result = await this.contract.read.getVotingCreditsInfo([address as `0x${string}`]);
      debugLog('getVotingCreditsInfo result:', result);
      
      const creditsInfo = {
        currentCredits: result[0],
        maxCredits: result[1],
        monthsUntilNext: result[2]
      };
      debugLog('getVotingCreditsInfo processed info:', creditsInfo);
      return creditsInfo;
    } catch (error) {
      console.error('Erro ao obter créditos de votação:', error);
      debugLog('Error in getVotingCreditsInfo:', error);
      throw new Error('Falha ao consultar créditos de votação');
    }
  }

  /**
   * Calcula a Saúde Sistémica completa
   * Coração do Dashboard Eudaimónico
   */
  async calculateSystemHealth(): Promise<SystemHealth> {
    debugLog('calculateSystemHealth called');
    try {
      const stats = await this.getSystemStats();
      debugLog('calculateSystemHealth stats:', stats);
      
      // Cálculos para Medidor de Resiliência (Autopoiese)
      const activeMembers = Number(stats.totalMembers); // Conversão explícita de bigint para number
      const suspendedMembers = 0; // Requer iteração sobre membros
      const contractUptime = 99.5; // Seria calculado com base em eventos históricos
      
      // Cálculos para Índice de Equidade (Simbiose)
      const avgBalance = stats.totalCredits / (stats.totalMembers || BigInt(1));
      const giniCoefficient = 0.3; // Requer cálculo complexo sobre todos os saldos
      
      // Métricas de Governança (Metacognição)
      const activeProposals = 0; // Requer contagem de propostas não executadas
      const participationRate = 75; // Histórico de participação em votações
      
      // Indicadores de Ressonância Semântica
      const communityEngagement = Math.min(100, (participationRate + 25));
      
      const health = {
        resilience: {
          activeMembers,
          suspendedMembers,
          contractUptime,
          networkStability: contractUptime > 95 ? 'high' : contractUptime > 85 ? 'medium' : 'low'
        },
        equity: {
          giniCoefficient,
          averageBalance: avgBalance,
          medianBalance: avgBalance, // Aproximação
          distributionHealth: giniCoefficient < 0.4 ? 'balanced' : giniCoefficient < 0.7 ? 'concentrated' : 'critical'
        },
        governance: {
          activeProposals,
          recentProposals: [], // Requer consulta de eventos recentes
          participationRate,
          consensusLevel: participationRate > 70 ? 'high' : participationRate > 40 ? 'medium' : 'low'
        },
        resonance: {
          communityEngagement,
          votingCreditsDistribution: 'healthy', // Baseado na distribuição de créditos
          collaborationIndex: 65 // Baseado em transferências e doações
        }
      };
      debugLog('calculateSystemHealth processed health:', health);
      return health;
    } catch (error) {
      console.error('Erro ao calcular saúde sistémica:', error);
      debugLog('Error in calculateSystemHealth:', error);
      throw new Error('Falha no cálculo da saúde sistémica');
    }
  }

  // ==========================================
  // FUNÇÕES DE ESCRITA (Ações Transformadoras)
  // ==========================================

  /**
   * Registra um novo membro na DAO
   * Primeira manifestação da Autopoiese
   */
  async registerMember(): Promise<string> {
    debugLog('registerMember called');
    try {
      const [account] = await this.walletClient.getAddresses();
      debugLog('Account for registerMember:', account);
      
      const hash = await this.contract.write.registerMember({
        account
      });
      debugLog('registerMember transaction hash:', hash);
      
      return hash;
    } catch (error) {
      console.error('Erro ao registrar membro:', error);
      debugLog('Error in registerMember:', error);
      throw new Error('Falha no registro como membro');
    }
  }

  /**
   * Reporta produção de energia
   * Conecta o mundo físico ao digital
   */
  async reportEnergyProduction(amount: bigint): Promise<string> {
    debugLog('reportEnergyProduction called with amount:', amount);
    try {
      const [account] = await this.walletClient.getAddresses();
      debugLog('Account for reportEnergyProduction:', account);
      
      const hash = await this.contract.write.reportEnergyProduction([amount], {
        account
      });
      debugLog('reportEnergyProduction transaction hash:', hash);
      
      return hash;
    } catch (error) {
      console.error('Erro ao reportar produção de energia:', error);
      debugLog('Error in reportEnergyProduction:', error);
      throw new Error('Falha no reporte de energia');
    }
  }

  /**
   * Transfere créditos entre membros
   * Implementa Simbiose económica
   */
  async transferCredits(to: string, amount: bigint): Promise<string> {
    debugLog('transferCredits called to:', to, 'amount:', amount);
    try {
      const [account] = await this.walletClient.getAddresses();
      debugLog('Account for transferCredits:', account);
      
      const hash = await this.contract.write.transferCredits([to as `0x${string}`, amount], {
        account
      });
      debugLog('transferCredits transaction hash:', hash);
      
      return hash;
    } catch (error) {
      console.error('Erro ao transferir créditos:', error);
      debugLog('Error in transferCredits:', error);
      throw new Error('Falha na transferência de créditos');
    }
  }

  /**
   * Cria uma nova proposta
   * Manifestação da Metacognição coletiva
   */
  async createProposal(description: string): Promise<string> {
    debugLog('createProposal called with description:', description);
    try {
      const [account] = await this.walletClient.getAddresses();
      debugLog('Account for createProposal:', account);
      
      const hash = await this.contract.write.createProposal([description], {
        account
      });
      debugLog('createProposal transaction hash:', hash);
      
      return hash;
    } catch (error) {
      console.error('Erro ao criar proposta:', error);
      debugLog('Error in createProposal:', error);
      throw new Error('Falha na criação da proposta');
    }
  }

  /**
   * Voto quadrático com intensidade
   * Ressonância Semântica em ação
   */
  async voteQuadratic(proposalId: bigint, support: boolean, intensity: number): Promise<string> {
    debugLog('voteQuadratic called for proposalId:', proposalId, 'support:', support, 'intensity:', intensity);
    try {
      const [account] = await this.walletClient.getAddresses();
      debugLog('Account for voteQuadratic:', account);
      
      const hash = await this.contract.write.voteQuadratic([proposalId, support, BigInt(intensity)], {
        account
      });
      debugLog('voteQuadratic transaction hash:', hash);
      
      return hash;
    } catch (error) {
      console.error('Erro no voto quadrático:', error);
      debugLog('Error in voteQuadratic:', error);
      throw new Error('Falha no voto quadrático');
    }
  }

  /**
   * Doa créditos de votação
   * Solidariedade cívica (Ressonância Semântica)
   */
  async donateVotingCredits(to: string, amount: bigint): Promise<string> {
    debugLog('donateVotingCredits called to:', to, 'amount:', amount);
    try {
      const [account] = await this.walletClient.getAddresses();
      debugLog('Account for donateVotingCredits:', account);
      
      const hash = await this.contract.write.donateVotingCredits([to as `0x${string}`, amount], {
        account
      });
      debugLog('donateVotingCredits transaction hash:', hash);
      
      return hash;
    } catch (error) {
      console.error('Erro ao doar créditos de votação:', error);
      debugLog('Error in donateVotingCredits:', error);
      throw new Error('Falha na doação de créditos');
    }
  }

  // ==========================================
  // MONITORIZAÇÃO EM TEMPO REAL
  // ==========================================

  /**
   * Subscreve eventos da blockchain
   * Sistema nervoso do Dashboard
   */
  subscribeToEvents(callback: (event: EnergyGridEvent) => void) {
    // Em produção, implementaria WebSocket ou polling de eventos
    console.log('Subscrevendo eventos da blockchain...');
    
    // Simulação de eventos para desenvolvimento
    setInterval(() => {
      const mockEvent: EnergyGridEvent = {
        type: 'EnergyProduced',
        timestamp: new Date(),
        data: { member: '0x...', amount: '1000' },
        impact: 'positive'
      };
      callback(mockEvent);
    }, 30000); // Evento a cada 30 segundos
  }
}

// Helper para logging em modo debug
const debugLog = (message: string, ...args: any[]) => {
  if (process.env.NEXT_PUBLIC_DEBUG_MODE === 'true') {
    console.log(`[DEBUG] ${message}`, ...args);
  }
};

// Instância singleton do serviço
export const energyGridService = new EnergyGridService();