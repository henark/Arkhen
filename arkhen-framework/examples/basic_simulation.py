#!/usr/bin/env python3
"""
Exemplo Básico do Framework Arkhen v2.0

Este exemplo demonstra como usar o framework para executar uma simulação
completa integrando todos os vetores:
- NMSI (Mecânica Informacional Subquântica)
- Blockchain Quântico com PoQC
- Sincronicidade Quântica
- Análise de propriedades emergentes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from arkhen import ArkhenFramework, FrameworkConfig, FRAMEWORK_INFO
import json


def main():
    """Função principal do exemplo"""
    
    print("=" * 60)
    print(f"🌌 {FRAMEWORK_INFO['name']}")
    print(f"📡 {FRAMEWORK_INFO['description']}")
    print(f"🔬 Version: {FRAMEWORK_INFO['version']}")
    print(f"👨‍💻 Author: {FRAMEWORK_INFO['author']}")
    print("=" * 60)
    
    # Configuração customizada para demonstração
    config = FrameworkConfig()
    config.simulation_duration = 5.0  # 5 segundos para demo rápida
    config.log_level = "INFO"
    config.max_nodes = 10
    
    print("\n🚀 Inicializando Framework Arkhen v2.0...")
    
    # Cria instância do framework
    arkhen = ArkhenFramework(config)
    
    # Exibe status inicial
    status = arkhen.get_status()
    print(f"✅ Framework inicializado com {len(status['components'])} componentes:")
    for component in status['components']:
        print(f"   • {component}")
    
    print(f"\n🔮 Executando simulação por {config.simulation_duration} segundos...")
    
    # Executa simulação
    results = arkhen.run_simulation()
    
    print("\n📊 Resultados da Simulação:")
    print("-" * 40)
    
    # Resultados NMSI
    nmsi_results = results['components_results']['nmsi']
    print(f"🌀 NMSI (Mecânica Informacional Subquântica):")
    print(f"   • Informação Total: {nmsi_results['total_information']:.4f}")
    print(f"   • Coerência Final: {nmsi_results['final_coherence']:.4f}")
    print(f"   • Osciladores: {nmsi_results['oscillator_count']}")
    
    dark_matter = nmsi_results['dark_matter_analysis']
    print(f"   • Fração Matéria Escura: {dark_matter['dark_matter_fraction']:.3f}")
    print(f"   • Fração Energia Escura: {dark_matter['dark_energy_fraction']:.3f}")
    
    # Resultados Blockchain
    blockchain_results = results['components_results']['blockchain']
    print(f"\n⛓️  Blockchain Quântico (PoQC):")
    print(f"   • Rodadas de Consenso: {blockchain_results['total_rounds']}")
    print(f"   • Taxa de Sucesso: {blockchain_results['success_rate']:.2%}")
    print(f"   • Coerência Média: {blockchain_results['average_coherence']:.4f}")
    print(f"   • Validadores: {blockchain_results['total_validators']}")
    print(f"   • Detecções de Fraude: {blockchain_results['fraud_detections']}")
    
    # Resultados Sincronicidade
    sync_results = results['components_results']['synchronicity']
    experiment = sync_results['experiment_result']
    print(f"\n🔗 Sincronicidade Quântica:")
    print(f"   • Coerência Inicial: {experiment['initial_coherence']:.4f}")
    print(f"   • Coerência Final: {experiment['final_coherence']:.4f}")
    print(f"   • Mudança: {experiment['coherence_change']:+.4f}")
    print(f"   • Clusters Sincronizados: {len(experiment['sync_clusters'])}")
    
    # Análise Global
    global_analysis = results['global_analysis']
    print(f"\n🌍 Análise Global do Framework:")
    print(f"   • Coerência do Framework: {global_analysis['framework_coherence']:.4f}")
    print(f"   • Propriedades Emergentes:")
    for prop in global_analysis['emergent_properties']:
        print(f"     ✨ {prop}")
    
    if not global_analysis['emergent_properties']:
        print("     • Nenhuma propriedade emergente detectada nesta simulação")
    
    # Salva resultados
    filename = arkhen.save_results("example_simulation_results.json")
    print(f"\n💾 Resultados salvos em: {filename}")
    
    print("\n" + "=" * 60)
    print("🎉 Simulação concluída com sucesso!")
    print("\n📖 Para mais exemplos e documentação:")
    print("   • README.md")
    print("   • examples/")
    print("   • https://github.com/henark/arkhen-framework")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulação interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")
        print("Verifique se todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)