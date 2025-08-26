import asyncio
import json
import time
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
from dotenv import load_dotenv

# Import from the real zai-sdk
try:
    from zai import ZaiClient
    from zai.errors import APIStatusError
    ZAI_AVAILABLE = True
except ImportError:
    ZAI_AVAILABLE = False
    ZaiClient = None
    APIStatusError = None
    print("⚠️  ZAI SDK não disponível. Usando modo simulado.")

def get_zai_client() -> ZaiClient:
    """
    Initializes and returns a ZaiClient.
    """
    # Assuming the .env file is in the root of the arkhen-framework directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        raise ValueError("ZAI_API_KEY not found in environment variables.")

    return ZaiClient(api_key=api_key)

@dataclass
class ZAIAnalysisResult:
    anomaly_detected: bool
    anomaly_type: Optional[str]
    urgency_level: int
    recommended_action: str
    confidence: float
    reasoning: str
    processing_time: float
    model_used: str

class ZAIIntegration:
    """
    Integrates ZAI SDK capabilities into the spatial controlled anarchy system.
    """
    def __init__(self, mesh_network, consensus, ledger):
        self.mesh = mesh_network
        self.consensus = consensus
        self.ledger = ledger

        if ZAI_AVAILABLE:
            try:
                self.zai = get_zai_client()
                self.model_info = self._get_model_info()
                print(f"✅ ZAI SDK inicializado: {self.model_info}")
            except Exception as e:
                print(f"❌ Erro ao inicializar ZAI SDK: {e}")
                self.zai = None
        else:
            self.zai = None
            print("⚠️  Operando em modo simulado sem ZAI SDK")

        self.response_cache = {}
        self.cache_ttl = 300

        self.usage_metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "average_response_time": 0.0,
            "model_accuracy": 0.0
        }

    def _get_model_info(self):
        if self.zai:
            try:
                test_response = self.zai.chat.completions.create(
                    model="glm-4.5",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10
                )
                return f"Model: {test_response.model}, Tokens: {test_response.usage.total_tokens}"
            except APIStatusError as e:
                return f"API Error ao obter informações: {e.status_code} - {e.message}"
            except Exception as e:
                return f"Erro ao obter informações: {e}"
        return "Modelo não disponível"

    async def analyze_telemetry_with_zai(self, satellite_id: str, telemetry_data: Dict) -> ZAIAnalysisResult:
        start_time = time.time()
        self.usage_metrics["total_requests"] += 1

        cache_key = f"telemetry_{satellite_id}_{hash(str(telemetry_data))}"
        cached_result = self._get_from_cache(cache_key)

        if cached_result:
            self.usage_metrics["cache_hits"] += 1
            return cached_result

        prompt = self._build_telemetry_prompt(satellite_id, telemetry_data)

        try:
            if self.zai:
                response = self.zai.chat.completions.create(
                    model="glm-4.5",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500,
                    top_p=0.9,
                    frequency_penalty=0.1,
                    presence_penalty=0.1
                )
                result = self._parse_zai_response(response, satellite_id)
            else:
                result = self._simulate_zai_response(prompt, satellite_id)

            processing_time = time.time() - start_time
            result.processing_time = processing_time
            self._update_metrics(processing_time)

            self._store_in_cache(cache_key, result)

            return result

        except APIStatusError as e:
            print(f"❌ Erro na API ZAI para {satellite_id}: {e.status_code} - {e.message}")
            return self._create_fallback_result(satellite_id, telemetry_data)
        except Exception as e:
            print(f"❌ Erro na análise ZAI para {satellite_id}: {e}")
            return self._create_fallback_result(satellite_id, telemetry_data)

    def _build_telemetry_prompt(self, satellite_id: str, telemetry_data: Dict) -> str:
        """Constrói prompt otimizado para análise de telemetria"""
        return f"""
        Você é um sistema especialista em análise de telemetria de satélites.
        Analise os seguintes dados do satélite {satellite_id}:

        Dados de Telemetria:
        - Nível de Bateria: {telemetry_data.get('battery_level', 'N/A')}%
        - Temperatura: {telemetry_data.get('temperature', 'N/A')}°C
        - Eficiência Painel Solar: {telemetry_data.get('solar_panel_efficiency', 'N/A')}
        - Posição: {telemetry_data.get('position', 'N/A')}
        - Velocidade: {telemetry_data.get('velocity', 'N/A')}
        - Timestamp: {telemetry_data.get('timestamp', 'N/A')}

        Tarefas:
        1. Detecte anomalias nos sistemas
        2. Classifique o nível de urgência (1-10)
        3. Recomende ação específica
        4. Forneça confiança na análise (0-1)
        5. Explique seu raciocínio

        Formato de resposta JSON:
        {{
            "anomaly_detected": boolean,
            "anomaly_type": "string",
            "urgency_level": int,
            "recommended_action": "string",
            "confidence": float,
            "reasoning": "string"
        }}
        """

    def _parse_zai_response(self, response, satellite_id: str) -> ZAIAnalysisResult:
        try:
            content = response.choices[0].message.content
            result_data = json.loads(content)

            return ZAIAnalysisResult(
                anomaly_detected=result_data.get('anomaly_detected', False),
                anomaly_type=result_data.get('anomaly_type'),
                urgency_level=result_data.get('urgency_level', 0),
                recommended_action=result_data.get('recommended_action', 'normal_operation'),
                confidence=result_data.get('confidence', 0.0),
                reasoning=result_data.get('reasoning', ''),
                processing_time=0.0,
                model_used=response.model
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Erro ao processar resposta ZAI para {satellite_id}: {e}")
            return self._create_fallback_result(satellite_id, {})

    def _simulate_zai_response(self, prompt: str, satellite_id: str) -> ZAIAnalysisResult:
        return self._create_fallback_result(satellite_id, {})

    def _create_fallback_result(self, satellite_id: str, telemetry_data: Dict) -> ZAIAnalysisResult:
        """Cria resultado de fallback quando ZAI não está disponível ou falha"""
        battery = telemetry_data.get('battery_level', 100)
        temperature = telemetry_data.get('temperature', 20)

        anomaly_detected = battery < 30 or temperature > 80
        anomaly_type = "low_battery" if battery < 30 else "high_temperature" if temperature > 80 else None
        urgency_level = 8 if battery < 20 else (7 if temperature > 80 else 0)
        recommended_action = "conserve_power" if battery < 30 else "cool_down" if temperature > 80 else "normal_operation"
        confidence = 0.7 if anomaly_detected else 0.9
        reasoning = "Análise baseada em regras predefinidas (modo fallback)"

        return ZAIAnalysisResult(
            anomaly_detected=anomaly_detected,
            anomaly_type=anomaly_type,
            urgency_level=urgency_level,
            recommended_action=recommended_action,
            confidence=confidence,
            reasoning=reasoning,
            processing_time=0.1,
            model_used="fallback_model"
        )

    def _get_from_cache(self, key: str) -> Optional[ZAIAnalysisResult]:
        """Recupera um resultado do cache se for válido."""
        if key in self.response_cache:
            result, timestamp = self.response_cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return result
        return None

    def _store_in_cache(self, key: str, result: ZAIAnalysisResult):
        """Armazena um resultado no cache."""
        self.response_cache[key] = (result, time.time())

    def _update_metrics(self, response_time: float):
        """Atualiza as métricas de uso."""
        total_req = self.usage_metrics["total_requests"]
        current_avg_time = self.usage_metrics["average_response_time"]
        if total_req > 0:
            self.usage_metrics["average_response_time"] = ((current_avg_time * (total_req - 1)) + response_time) / total_req

    async def generate_mission_plan(self, mission_objective: Dict, constraints: Dict) -> Dict:
        """Gera plano de missão usando ZAI"""
        prompt = f"""
        Como especialista em missões espaciais, gere um plano detalhado para:

        Objetivo da Missão: {mission_objective}
        Restrições: {constraints}

        O plano deve incluir:
        1. Fases da missão
        2. Recursos necessários
        3. Timeline estimada
        4. Riscos e mitigação
        5. Critérios de sucesso

        Formato: JSON estruturado
        """

        try:
            if self.zai:
                response = self.zai.chat.completions.create(
                    model="glm-4.5",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=1000
                )
                return json.loads(response.choices[0].message.content)
            else:
                return self._generate_fallback_mission_plan(mission_objective, constraints)
        except Exception as e:
            print(f"❌ Erro ao gerar plano de missão: {e}")
            return self._generate_fallback_mission_plan(mission_objective, constraints)

    def _generate_fallback_mission_plan(self, mission_objective: Dict, constraints: Dict) -> Dict:
        """Gera um plano de missão de fallback."""
        print("Gerando plano de missão de fallback...")
        return {
            "mission_name": f"Fallback Plan for {mission_objective.get('name', 'Unnamed Mission')}",
            "phases": [
                {"phase_name": "Launch", "duration_days": 1, "description": "Launch and initial orbit insertion."},
                {"phase_name": "Cruise", "duration_days": 10, "description": "Cruise to target destination."},
                {"phase_name": "Operation", "duration_days": 30, "description": "Execute primary mission objectives."},
                {"phase_name": "Decommission", "duration_days": 2, "description": "Safe decommissioning of the spacecraft."}
            ],
            "required_resources": ["Launch Vehicle", "Ground Station Support", "Mission Control Team"],
            "estimated_timeline_days": 43,
            "risks_and_mitigation": [
                {"risk": "Launch failure", "mitigation": "Redundant systems and rigorous pre-flight checks."},
                {"risk": "Communication loss", "mitigation": "Multiple communication antennas and predefined autonomy protocols."}
            ],
            "success_criteria": ["Achieve 80% of primary mission objectives."],
            "model_used": "fallback_model"
        }
