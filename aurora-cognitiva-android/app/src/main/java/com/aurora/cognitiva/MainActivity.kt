package com.aurora.cognitiva

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.aurora.cognitiva.ui.theme.AuroraCognitivaTheme
import com.aurora.cognitiva.ui.dashboard.DashboardScreen
import com.aurora.cognitiva.ui.governance.GovernanceScreen
import com.aurora.cognitiva.ui.manufacturing.ManufacturingScreen
import com.aurora.cognitiva.ui.verification.NoirVerificationScreen
import com.aurora.cognitiva.server.LocalServerManager
import com.aurora.cognitiva.data.repository.AuroraRepository
import com.aurora.cognitiva.utils.NetworkMonitor
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    
    private lateinit var localServerManager: LocalServerManager
    private lateinit var auroraRepository: AuroraRepository
    private lateinit var networkMonitor: NetworkMonitor
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize core components
        initializeAuroraComponents()
        
        setContent {
            AuroraCognitivaTheme {
                AuroraApp(
                    localServerManager = localServerManager,
                    auroraRepository = auroraRepository,
                    networkMonitor = networkMonitor
                )
            }
        }
    }
    
    private fun initializeAuroraComponents() {
        localServerManager = LocalServerManager(this)
        networkMonitor = NetworkMonitor(this)
        auroraRepository = AuroraRepository(this, localServerManager, networkMonitor)
    }
    
    override fun onDestroy() {
        super.onDestroy()
        localServerManager.stop()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuroraApp(
    localServerManager: LocalServerManager,
    auroraRepository: AuroraRepository,
    networkMonitor: NetworkMonitor
) {
    val navController = rememberNavController()
    var isInitializing by remember { mutableStateOf(true) }
    var initializationProgress by remember { mutableStateOf(0f) }
    var currentStep by remember { mutableStateOf("Inicializando Aurora...") }
    
    // Initialize Aurora systems
    LaunchedEffect(Unit) {
        try {
            // Step 1: Start local server
            currentStep = "Iniciando servidor local..."
            initializationProgress = 0.2f
            localServerManager.start()
            delay(2000)
            
            // Step 2: Initialize blockchain
            currentStep = "Conectando blockchain..."
            initializationProgress = 0.4f
            auroraRepository.initializeBlockchain()
            delay(1500)
            
            // Step 3: Load AI models
            currentStep = "Carregando modelos de IA..."
            initializationProgress = 0.6f
            auroraRepository.loadAIModels()
            delay(2000)
            
            // Step 4: Initialize Noir circuits
            currentStep = "Preparando circuitos Noir..."
            initializationProgress = 0.8f
            auroraRepository.initializeNoirCircuits()
            delay(1000)
            
            // Step 5: Complete initialization
            currentStep = "Ativando Aurora Cognitiva..."
            initializationProgress = 1.0f
            delay(1000)
            
            isInitializing = false
        } catch (e: Exception) {
            currentStep = "Erro na inicialização: ${e.message}"
            // Handle initialization error
        }
    }
    
    if (isInitializing) {
        AuroraInitializationScreen(
            progress = initializationProgress,
            currentStep = currentStep
        )
    } else {
        Scaffold(
            bottomBar = {
                AuroraBottomNavigation(
                    navController = navController
                )
            }
        ) { innerPadding ->
            NavHost(
                navController = navController,
                startDestination = "dashboard",
                modifier = Modifier.padding(innerPadding)
            ) {
                composable("dashboard") {
                    DashboardScreen(
                        auroraRepository = auroraRepository,
                        networkMonitor = networkMonitor
                    )
                }
                composable("governance") {
                    GovernanceScreen(
                        auroraRepository = auroraRepository
                    )
                }
                composable("manufacturing") {
                    ManufacturingScreen(
                        auroraRepository = auroraRepository
                    )
                }
                composable("verification") {
                    NoirVerificationScreen(
                        auroraRepository = auroraRepository
                    )
                }
            }
        }
    }
}

@Composable
fun AuroraInitializationScreen(
    progress: Float,
    currentStep: String
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // Aurora logo animation
        AuroraLogo(
            modifier = Modifier.size(120.dp),
            isAnimating = true
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = "Aurora Cognitiva",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.primary
        )
        
        Text(
            text = "Convergência Holográfica",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
        )
        
        Spacer(modifier = Modifier.height(48.dp))
        
        LinearProgressIndicator(
            progress = progress,
            modifier = Modifier
                .fillMaxWidth()
                .height(8.dp),
            color = MaterialTheme.colorScheme.primary,
            trackColor = MaterialTheme.colorScheme.primaryContainer
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = currentStep,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = "${(progress * 100).toInt()}%",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
        )
    }
}

@Composable
fun AuroraBottomNavigation(
    navController: androidx.navigation.NavController
) {
    NavigationBar {
        val currentRoute = navController.currentBackStackEntry?.destination?.route
        
        NavigationBarItem(
            icon = { 
                Icon(
                    imageVector = Icons.Default.Dashboard,
                    contentDescription = "Dashboard"
                )
            },
            label = { Text("Dashboard") },
            selected = currentRoute == "dashboard",
            onClick = {
                navController.navigate("dashboard") {
                    popUpTo("dashboard") { inclusive = true }
                }
            }
        )
        
        NavigationBarItem(
            icon = { 
                Icon(
                    imageVector = Icons.Default.HowToVote,
                    contentDescription = "Governança"
                )
            },
            label = { Text("Governança") },
            selected = currentRoute == "governance",
            onClick = {
                navController.navigate("governance") {
                    popUpTo("dashboard")
                }
            }
        )
        
        NavigationBarItem(
            icon = { 
                Icon(
                    imageVector = Icons.Default.Precision3d,
                    contentDescription = "Manufatura"
                )
            },
            label = { Text("Manufatura") },
            selected = currentRoute == "manufacturing",
            onClick = {
                navController.navigate("manufacturing") {
                    popUpTo("dashboard")
                }
            }
        )
        
        NavigationBarItem(
            icon = { 
                Icon(
                    imageVector = Icons.Default.VerifiedUser,
                    contentDescription = "Verificação"
                )
            },
            label = { Text("Noir") },
            selected = currentRoute == "verification",
            onClick = {
                navController.navigate("verification") {
                    popUpTo("dashboard")
                }
            }
        )
    }
}

@Composable
fun AuroraLogo(
    modifier: Modifier = Modifier,
    isAnimating: Boolean = false
) {
    // Animated Aurora logo with holographic effect
    val infiniteTransition = rememberInfiniteTransition()
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = if (isAnimating) 360f else 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(3000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        )
    )
    
    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val center = Offset(size.width / 2, size.height / 2)
            val radius = minOf(size.width, size.height) / 3
            
            // Draw holographic aurora effect
            for (i in 0..3) {
                val alpha = (4 - i) * 0.2f
                val currentRadius = radius + (i * 10)
                
                drawCircle(
                    color = Color.Cyan.copy(alpha = alpha),
                    radius = currentRadius,
                    center = center,
                    style = Stroke(width = 2.dp.toPx())
                )
            }
            
            // Draw rotating triangles (representing tri-technology convergence)
            rotate(rotation, center) {
                val triangleRadius = radius * 0.6f
                for (i in 0..2) {
                    val angle = (i * 120f) + rotation
                    val triangleCenter = Offset(
                        center.x + cos(Math.toRadians(angle.toDouble())).toFloat() * triangleRadius * 0.5f,
                        center.y + sin(Math.toRadians(angle.toDouble())).toFloat() * triangleRadius * 0.5f
                    )
                    
                    val color = when(i) {
                        0 -> Color.Blue   // Blockchain
                        1 -> Color.Green  // AI
                        else -> Color.Red // Manufacturing
                    }
                    
                    drawCircle(
                        color = color.copy(alpha = 0.8f),
                        radius = 8.dp.toPx(),
                        center = triangleCenter
                    )
                }
            }
            
            // Central core
            drawCircle(
                color = Color.White,
                radius = 4.dp.toPx(),
                center = center
            )
        }
    }
}