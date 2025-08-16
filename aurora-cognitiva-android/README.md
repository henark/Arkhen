# 🌅 Aurora Cognitiva Android App

## Visão Geral

Aplicativo Android nativo que implementa a Aurora Cognitiva com capacidades de servidor local e conectividade à internet, permitindo acesso completo ao ecossistema holográfico mesmo offline, com sincronização quando online.

## 🎯 Características Principais

- **🏠 Servidor Local**: Node.js embarcado rodando no dispositivo
- **🌐 Conectividade Híbrida**: Funciona offline e online
- **🔗 Blockchain Local**: Nó leve Ethereum/Polygon
- **🧠 IA Embarcada**: TensorFlow Lite para otimização local
- **📱 Interface Nativa**: Kotlin/Compose com UI holográfica
- **🔒 Verificação Noir**: Provas ZK processadas localmente
- **🗳️ Governança Móvel**: Votação holográfica touch-friendly

## 📁 Estrutura do Projeto

```
aurora-cognitiva-android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/aurora/cognitiva/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── ui/
│   │   │   │   │   ├── dashboard/DashboardScreen.kt
│   │   │   │   │   ├── governance/GovernanceScreen.kt
│   │   │   │   │   ├── manufacturing/ManufacturingScreen.kt
│   │   │   │   │   ├── verification/NoirVerificationScreen.kt
│   │   │   │   │   └── components/
│   │   │   │   │       ├── AuroraVisualization.kt
│   │   │   │   │       ├── TSIGauge.kt
│   │   │   │   │       ├── HolographicVotingCard.kt
│   │   │   │   │       └── ConvergenceMonitor.kt
│   │   │   │   ├── data/
│   │   │   │   │   ├── local/
│   │   │   │   │   │   ├── AuroraDatabase.kt
│   │   │   │   │   │   ├── dao/
│   │   │   │   │   │   └── entities/
│   │   │   │   │   ├── remote/
│   │   │   │   │   │   ├── AuroraApi.kt
│   │   │   │   │   │   └── dto/
│   │   │   │   │   └── repository/
│   │   │   │   │       ├── AuroraRepository.kt
│   │   │   │   │       └── SyncRepository.kt
│   │   │   │   ├── server/
│   │   │   │   │   ├── LocalServerManager.kt
│   │   │   │   │   ├── NodeJSExecutor.kt
│   │   │   │   │   └── BlockchainNode.kt
│   │   │   │   ├── blockchain/
│   │   │   │   │   ├── Web3Manager.kt
│   │   │   │   │   ├── SmartContractInterface.kt
│   │   │   │   │   └── TransactionManager.kt
│   │   │   │   ├── ai/
│   │   │   │   │   ├── TensorFlowLiteManager.kt
│   │   │   │   │   ├── OptimizationEngine.kt
│   │   │   │   │   └── PredictionService.kt
│   │   │   │   ├── noir/
│   │   │   │   │   ├── NoirProofGenerator.kt
│   │   │   │   │   ├── VerificationEngine.kt
│   │   │   │   │   └── CircuitManager.kt
│   │   │   │   └── utils/
│   │   │   │       ├── NetworkMonitor.kt
│   │   │   │       ├── EncryptionUtils.kt
│   │   │   │       └── HolographicMath.kt
│   │   │   ├── assets/
│   │   │   │   ├── nodejs/
│   │   │   │   │   ├── server.js
│   │   │   │   │   ├── package.json
│   │   │   │   │   └── node_modules/ (bundled)
│   │   │   │   ├── blockchain/
│   │   │   │   │   ├── contracts/
│   │   │   │   │   └── genesis.json
│   │   │   │   ├── ai_models/
│   │   │   │   │   ├── convergence_optimizer.tflite
│   │   │   │   │   ├── quality_predictor.tflite
│   │   │   │   │   └── cultural_analyzer.tflite
│   │   │   │   └── noir_circuits/
│   │   │   │       ├── convergence_verification.wasm
│   │   │   │       ├── governance_proof.wasm
│   │   │   │       └── manufacturing_integrity.wasm
│   │   │   └── res/
│   │   │       ├── layout/
│   │   │       ├── values/
│   │   │       ├── drawable/
│   │   │       └── raw/
│   │   └── androidTest/
│   │   └── test/
│   ├── build.gradle.kts
│   └── proguard-rules.pro
├── gradle/
├── build.gradle.kts
├── settings.gradle.kts
├── local.properties
└── README.md
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Android Studio Arctic Fox ou superior
- Android SDK 24+ (Android 7.0+)
- Gradle 7.0+
- Node.js 18+ (para desenvolvimento)
- Git LFS (para modelos de IA)

### Build do APK

```bash
# 1. Clone o repositório
git clone <repo-url>
cd aurora-cognitiva-android

# 2. Prepare assets embarcados
./scripts/prepare_assets.sh

# 3. Build do APK
./gradlew assembleRelease

# 4. APK gerado em:
# app/build/outputs/apk/release/aurora-cognitiva-release.apk
```

### Instalação

```bash
# Instalar via ADB
adb install app/build/outputs/apk/release/aurora-cognitiva-release.apk

# Ou transferir para dispositivo e instalar manualmente
```

## 📱 Funcionalidades do App

### Dashboard Principal

- **TSI Gauge**: Medidor em tempo real do Technology Synergy Index
- **Convergence Monitor**: Visualização da sinergia entre blockchain, IA e manufatura
- **Network Status**: Status de conectividade local/internet
- **Sync Indicator**: Estado de sincronização com rede global

### Governança Holográfica

- **Votação Multidimensional**: Interface touch para votos técnico/cultural/cósmico/temporal
- **Propostas Ativas**: Lista de propostas abertas para votação
- **Histórico de Decisões**: Visualização de decisões holográficas passadas
- **Poder de Voto**: Indicador do poder de voto quadrático do usuário

### Manufatura 3D

- **Design Browser**: Catálogo de designs 3D verificados
- **Optimization Engine**: IA local para otimização de designs
- **Quality Monitor**: Acompanhamento de jobs de impressão
- **IoT Integration**: Conexão com sensores de impressoras 3D

### Verificação Noir

- **Proof Generator**: Interface para gerar provas ZK
- **Verification History**: Histórico de verificações realizadas
- **Circuit Library**: Biblioteca de circuitos Noir disponíveis
- **Performance Monitor**: Métricas de performance das provas

## 🏠 Servidor Local Embarcado

### Arquitetura

O app inclui um servidor Node.js embarcado que executa:

```javascript
// server.js embarcado
const express = require('express');
const Web3 = require('web3');
const tf = require('@tensorflow/tfjs-node');

class AuroraLocalServer {
    constructor() {
        this.app = express();
        this.port = 3001;
        this.blockchain = new LocalBlockchainNode();
        this.ai = new LocalAIEngine();
        this.noir = new LocalNoirEngine();
    }

    async start() {
        // Inicializar blockchain local
        await this.blockchain.initialize();
        
        // Carregar modelos de IA
        await this.ai.loadModels();
        
        // Configurar rotas API
        this.setupRoutes();
        
        // Iniciar servidor
        this.app.listen(this.port, '127.0.0.1', () => {
            console.log(`Aurora Local Server running on port ${this.port}`);
        });
    }

    setupRoutes() {
        // API de convergência
        this.app.get('/api/convergence/tsi', this.getTSI.bind(this));
        this.app.post('/api/convergence/update', this.updateMetrics.bind(this));
        
        // API de governança
        this.app.get('/api/governance/proposals', this.getProposals.bind(this));
        this.app.post('/api/governance/vote', this.castVote.bind(this));
        
        // API de manufatura
        this.app.get('/api/manufacturing/jobs', this.getJobs.bind(this));
        this.app.post('/api/manufacturing/optimize', this.optimizeDesign.bind(this));
        
        // API de verificação
        this.app.post('/api/verification/generate', this.generateProof.bind(this));
        this.app.post('/api/verification/verify', this.verifyProof.bind(this));
        
        // API de sincronização
        this.app.post('/api/sync/upload', this.uploadToGlobal.bind(this));
        this.app.get('/api/sync/download', this.downloadFromGlobal.bind(this));
    }
}
```

### Capacidades Offline

- **Blockchain Local**: Nó Ethereum leve para transações offline
- **IA Embarcada**: Modelos TensorFlow Lite para otimização local
- **Banco de Dados Local**: SQLite com dados sincronizáveis
- **Noir Local**: Processamento de provas ZK sem internet

## 🌐 Conectividade Híbrida

### Modo Offline

Quando sem internet, o app:
- Opera completamente local via servidor embarcado
- Mantém blockchain local sincronizado
- Processa otimizações de IA localmente
- Gera e verifica provas Noir offline
- Armazena todas ações para sincronização posterior

### Modo Online

Quando com internet, o app:
- Sincroniza com blockchain global (Ethereum/Polygon)
- Atualiza modelos de IA com versões mais recentes
- Compartilha provas Noir com rede global
- Participa de governança global
- Baixa novos designs e atualizações

### Sincronização Inteligente

```kotlin
// SyncRepository.kt
class SyncRepository(
    private val localDb: AuroraDatabase,
    private val remoteApi: AuroraApi,
    private val networkMonitor: NetworkMonitor
) {
    suspend fun sync() {
        if (!networkMonitor.isConnected()) return
        
        try {
            // Sync convergence metrics
            val localMetrics = localDb.getUnsyncedMetrics()
            remoteApi.uploadMetrics(localMetrics)
            
            val remoteMetrics = remoteApi.getLatestMetrics()
            localDb.insertMetrics(remoteMetrics)
            
            // Sync governance data
            val localVotes = localDb.getUnsyncedVotes()
            remoteApi.uploadVotes(localVotes)
            
            val newProposals = remoteApi.getNewProposals()
            localDb.insertProposals(newProposals)
            
            // Sync manufacturing jobs
            val localJobs = localDb.getUnsyncedJobs()
            remoteApi.uploadJobs(localJobs)
            
            // Update AI models if needed
            val modelUpdates = remoteApi.checkModelUpdates()
            if (modelUpdates.isNotEmpty()) {
                downloadAndInstallModels(modelUpdates)
            }
            
            // Mark all as synced
            localDb.markAllAsSynced()
            
        } catch (e: Exception) {
            // Log sync error, will retry later
            Log.e("Sync", "Sync failed", e)
        }
    }
}
```

## 🔒 Segurança e Privacidade

### Criptografia Local

- **Chaves Privadas**: Armazenadas em Android Keystore
- **Dados Sensíveis**: Criptografados com AES-256
- **Comunicação**: TLS 1.3 para todas conexões
- **Provas ZK**: Processamento local preserva privacidade

### Permissions Mínimas

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" 
                 android:maxSdkVersion="28" />
<uses-permission android:name="android.permission.CAMERA" /> <!-- Para QR codes -->
<uses-permission android:name="android.permission.BLUETOOTH" /> <!-- Para IoT -->
```

## 📊 Interface Holográfica

### Componentes Visuais

```kotlin
// AuroraVisualization.kt
@Composable
fun AuroraVisualization(
    tsiValue: Float,
    convergenceData: ConvergenceData,
    modifier: Modifier = Modifier
) {
    Canvas(modifier = modifier.fillMaxSize()) {
        val center = Offset(size.width / 2, size.height / 2)
        val radius = minOf(size.width, size.height) / 3
        
        // Desenhar holograma da Aurora
        drawHolographicAura(center, radius, tsiValue)
        
        // Visualizar convergência tri-tecnológica
        drawTechnologyTriangle(center, radius * 0.8f, convergenceData)
        
        // Mostrar fluxo de informação
        drawInformationFlow(center, radius, convergenceData.flowIntensity)
        
        // Indicadores de fase
        drawPhaseIndicators(center, radius * 1.2f, convergenceData.currentPhase)
    }
}

@Composable
fun TSIGauge(
    value: Float,
    target: Float = 0.95f,
    modifier: Modifier = Modifier
) {
    Box(modifier = modifier) {
        CircularProgressIndicator(
            progress = value,
            modifier = Modifier.size(120.dp),
            strokeWidth = 8.dp,
            color = when {
                value >= 0.9f -> Color.Green
                value >= 0.7f -> Color.Yellow
                else -> Color.Red
            }
        )
        
        Column(
            modifier = Modifier.align(Alignment.Center),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "TSI",
                style = MaterialTheme.typography.caption
            )
            Text(
                text = String.format("%.3f", value),
                style = MaterialTheme.typography.h6,
                fontWeight = FontWeight.Bold
            )
        }
    }
}
```

### Votação Holográfica

```kotlin
// HolographicVotingCard.kt
@Composable
fun HolographicVotingCard(
    proposal: Proposal,
    onVote: (HolographicVote) -> Unit,
    modifier: Modifier = Modifier
) {
    var technicalScore by remember { mutableStateOf(0.5f) }
    var culturalScore by remember { mutableStateOf(0.5f) }
    var cosmicScore by remember { mutableStateOf(0.5f) }
    var temporalScore by remember { mutableStateOf(0.5f) }
    var stakeAmount by remember { mutableStateOf(100f) }
    
    Card(
        modifier = modifier.fillMaxWidth(),
        elevation = 8.dp
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = proposal.title,
                style = MaterialTheme.typography.h6
            )
            
            Text(
                text = proposal.description,
                style = MaterialTheme.typography.body2,
                modifier = Modifier.padding(vertical = 8.dp)
            )
            
            // Dimensões de votação
            VotingDimension(
                label = "Mérito Técnico",
                value = technicalScore,
                onValueChange = { technicalScore = it },
                color = Color.Blue
            )
            
            VotingDimension(
                label = "Alinhamento Cultural",
                value = culturalScore,
                onValueChange = { culturalScore = it },
                color = Color.Green
            )
            
            VotingDimension(
                label = "Sabedoria Cósmica",
                value = cosmicScore,
                onValueChange = { cosmicScore = it },
                color = Color.Purple
            )
            
            VotingDimension(
                label = "Impacto Temporal",
                value = temporalScore,
                onValueChange = { temporalScore = it },
                color = Color.Orange
            )
            
            // Stake commitment
            Text("Comprometimento de Stake")
            Slider(
                value = stakeAmount,
                onValueChange = { stakeAmount = it },
                valueRange = 1f..1000f,
                modifier = Modifier.padding(vertical = 8.dp)
            )
            
            // Poder de voto calculado
            val votingPower = calculateHolographicPower(
                technicalScore, culturalScore, cosmicScore, temporalScore, stakeAmount
            )
            
            Text(
                text = "Poder de Voto: ${String.format("%.2f", votingPower)}",
                style = MaterialTheme.typography.caption
            )
            
            Button(
                onClick = {
                    onVote(
                        HolographicVote(
                            technicalScore, culturalScore, cosmicScore, 
                            temporalScore, stakeAmount
                        )
                    )
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Votar Holograficamente")
            }
        }
    }
}
```

## 🔧 Build e Deploy

### Script de Build Automatizado

```bash
#!/bin/bash
# scripts/build_apk.sh

echo "🌅 Building Aurora Cognitiva APK..."

# 1. Preparar assets embarcados
echo "📦 Preparing embedded assets..."
./scripts/prepare_nodejs.sh
./scripts/prepare_blockchain.sh
./scripts/prepare_ai_models.sh
./scripts/prepare_noir_circuits.sh

# 2. Build do projeto
echo "🔨 Building project..."
./gradlew clean
./gradlew assembleRelease

# 3. Assinar APK
echo "🔑 Signing APK..."
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore aurora.keystore \
    app/build/outputs/apk/release/app-release-unsigned.apk \
    aurora_key

# 4. Zipalign
echo "📐 Optimizing APK..."
zipalign -v 4 \
    app/build/outputs/apk/release/app-release-unsigned.apk \
    app/build/outputs/apk/release/aurora-cognitiva-release.apk

# 5. Verificar assinatura
echo "✅ Verifying signature..."
jarsigner -verify -verbose -certs \
    app/build/outputs/apk/release/aurora-cognitiva-release.apk

echo "🎉 APK built successfully!"
echo "📱 Location: app/build/outputs/apk/release/aurora-cognitiva-release.apk"
echo "📊 Size: $(du -h app/build/outputs/apk/release/aurora-cognitiva-release.apk | cut -f1)"
```

### Configuração de Release

```kotlin
// build.gradle.kts (app)
android {
    compileSdk 34
    
    defaultConfig {
        applicationId "com.aurora.cognitiva"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }
    
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("release")
            
            // Configurações específicas para Aurora
            buildConfigField("String", "LOCAL_SERVER_PORT", "\"3001\"")
            buildConfigField("String", "ETHEREUM_NETWORK", "\"polygon\"")
            buildConfigField("Boolean", "ENABLE_CRASH_REPORTING", "true")
        }
    }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = "1.8"
    }
    
    buildFeatures {
        compose = true
    }
    
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.4"
    }
    
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // Core Android
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.1")
    
    // Compose
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    
    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.5")
    
    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    
    // Database
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    kapt("androidx.room:room-compiler:2.6.1")
    
    // Network
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    
    // Blockchain
    implementation("org.web3j:core:4.9.8")
    implementation("org.web3j:crypto:4.9.8")
    
    // AI
    implementation("org.tensorflow:tensorflow-lite:2.13.0")
    implementation("org.tensorflow:tensorflow-lite-support:0.4.4")
    
    // Cryptography
    implementation("org.bouncycastle:bcpkix-jdk15on:1.70")
    
    // Utilities
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("androidx.work:work-runtime-ktx:2.9.0")
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2023.10.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

## 📱 Download e Instalação

### APK Release

```
📱 Aurora Cognitiva v1.0.0
📊 Tamanho: ~85MB (inclui servidor Node.js, modelos IA, circuitos Noir)
🎯 Android: 7.0+ (API 24+)
🔒 Permissions: Internet, Storage, Camera, Bluetooth
```

### Links de Download

- **[Direct Download](releases/aurora-cognitiva-v1.0.0.apk)** - APK principal
- **[Lite Version](releases/aurora-cognitiva-lite-v1.0.0.apk)** - Versão sem IA embarcada (~25MB)
- **[Beta Channel](releases/aurora-cognitiva-beta-v1.1.0.apk)** - Versão com recursos experimentais

### Instalação Manual

1. **Baixe o APK** para seu dispositivo Android
2. **Enable Unknown Sources** em Configurações > Segurança
3. **Instale o APK** tocando no arquivo baixado
4. **Abra o app** e aguarde inicialização do servidor local (~30s primeira vez)
5. **Configure conectividade** (local/internet) nas configurações

## 🛠️ Desenvolvimento

Para desenvolvedores que querem contribuir:

```bash
# Setup desenvolvimento
git clone <repo>
cd aurora-cognitiva-android
./scripts/setup_dev_environment.sh

# Build debug
./gradlew assembleDebug

# Run tests
./gradlew test
./gradlew connectedAndroidTest

# Deploy para dispositivo
./gradlew installDebug
```

## 📞 Suporte

- **Documentação**: [docs/android/](docs/android/)
- **Issues**: [GitHub Issues](https://github.com/aurora-cognitiva/android/issues)
- **Discussões**: [Community Forum](https://forum.aurora-cognitiva.org)
- **Email**: support@aurora-cognitiva.org

---

**🌅 A Aurora Cognitiva na palma da sua mão - Convergência tecnológica, governança holográfica e evolução cósmica, onde quer que você esteja.**

*v1.0.0 - "Despertar Mobile" - Dezembro 2024*