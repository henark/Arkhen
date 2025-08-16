package com.aurora.cognitiva.server

import android.content.Context
import android.util.Log
import com.aurora.cognitiva.BuildConfig
import java.io.*
import java.net.HttpURLConnection
import java.net.URL
import kotlinx.coroutines.*
import org.json.JSONObject
import java.util.concurrent.atomic.AtomicBoolean

class LocalServerManager(private val context: Context) {
    
    companion object {
        private const val TAG = "LocalServerManager"
        private const val SERVER_PORT = 3001
        private const val SERVER_HOST = "127.0.0.1"
        private const val NODE_EXECUTABLE = "node"
        private const val SERVER_SCRIPT = "server.js"
        private const val HEALTH_CHECK_INTERVAL = 5000L
    }
    
    private var serverProcess: Process? = null
    private val isServerRunning = AtomicBoolean(false)
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private var healthCheckJob: Job? = null
    
    suspend fun start(): Boolean = withContext(Dispatchers.IO) {
        try {
            if (isServerRunning.get()) {
                Log.i(TAG, "Server already running")
                return@withContext true
            }
            
            // Extract Node.js assets if needed
            extractNodeAssets()
            
            // Start Node.js server
            startNodeServer()
            
            // Wait for server to be ready
            if (waitForServerReady()) {
                isServerRunning.set(true)
                startHealthCheck()
                Log.i(TAG, "Aurora Local Server started successfully")
                true
            } else {
                Log.e(TAG, "Failed to start Aurora Local Server")
                false
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error starting server", e)
            false
        }
    }
    
    fun stop() {
        try {
            healthCheckJob?.cancel()
            serverProcess?.destroyForcibly()
            serverProcess = null
            isServerRunning.set(false)
            Log.i(TAG, "Aurora Local Server stopped")
        } catch (e: Exception) {
            Log.e(TAG, "Error stopping server", e)
        }
    }
    
    fun isRunning(): Boolean = isServerRunning.get()
    
    fun getServerUrl(): String = "http://$SERVER_HOST:$SERVER_PORT"
    
    private suspend fun extractNodeAssets() = withContext(Dispatchers.IO) {
        val nodeDir = File(context.filesDir, "nodejs")
        if (!nodeDir.exists() || shouldUpdateAssets()) {
            Log.i(TAG, "Extracting Node.js assets...")
            
            nodeDir.mkdirs()
            
            // Extract server.js
            extractAsset("nodejs/server.js", File(nodeDir, "server.js"))
            
            // Extract package.json
            extractAsset("nodejs/package.json", File(nodeDir, "package.json"))
            
            // Extract node_modules (bundled)
            extractNodeModules(nodeDir)
            
            // Mark assets as current version
            val versionFile = File(nodeDir, "version.txt")
            versionFile.writeText(BuildConfig.VERSION_NAME)
        }
    }
    
    private fun extractAsset(assetPath: String, targetFile: File) {
        context.assets.open(assetPath).use { input ->
            targetFile.outputStream().use { output ->
                input.copyTo(output)
            }
        }
    }
    
    private fun extractNodeModules(nodeDir: File) {
        val nodeModulesDir = File(nodeDir, "node_modules")
        nodeModulesDir.mkdirs()
        
        // Extract essential modules for Aurora functionality
        val modules = listOf(
            "express", "web3", "tensorflow", "crypto-js", 
            "sqlite3", "cors", "body-parser", "ws"
        )
        
        modules.forEach { module ->
            try {
                val moduleDir = File(nodeModulesDir, module)
                moduleDir.mkdirs()
                extractModuleFiles("nodejs/node_modules/$module", moduleDir)
            } catch (e: Exception) {
                Log.w(TAG, "Failed to extract module $module", e)
            }
        }
    }
    
    private fun extractModuleFiles(assetPath: String, targetDir: File) {
        try {
            val files = context.assets.list(assetPath) ?: return
            for (file in files) {
                val assetFile = "$assetPath/$file"
                val targetFile = File(targetDir, file)
                
                if (context.assets.list(assetFile)?.isNotEmpty() == true) {
                    // It's a directory
                    targetFile.mkdirs()
                    extractModuleFiles(assetFile, targetFile)
                } else {
                    // It's a file
                    extractAsset(assetFile, targetFile)
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "Error extracting module files from $assetPath", e)
        }
    }
    
    private fun shouldUpdateAssets(): Boolean {
        val versionFile = File(context.filesDir, "nodejs/version.txt")
        return !versionFile.exists() || versionFile.readText() != BuildConfig.VERSION_NAME
    }
    
    private suspend fun startNodeServer() = withContext(Dispatchers.IO) {
        val nodeDir = File(context.filesDir, "nodejs")
        val serverScript = File(nodeDir, SERVER_SCRIPT)
        
        val processBuilder = ProcessBuilder()
            .directory(nodeDir)
            .command("sh", "-c", "cd ${nodeDir.absolutePath} && node $SERVER_SCRIPT")
            .redirectErrorStream(true)
        
        // Set environment variables
        val env = processBuilder.environment()
        env["PORT"] = SERVER_PORT.toString()
        env["HOST"] = SERVER_HOST
        env["NODE_ENV"] = if (BuildConfig.DEBUG) "development" else "production"
        env["AURORA_DATA_DIR"] = File(context.filesDir, "aurora_data").absolutePath
        
        serverProcess = processBuilder.start()
        
        // Monitor server output
        scope.launch {
            serverProcess?.inputStream?.bufferedReader()?.use { reader ->
                reader.forEachLine { line ->
                    Log.d(TAG, "Server: $line")
                }
            }
        }
    }
    
    private suspend fun waitForServerReady(timeoutMs: Long = 30000): Boolean = 
        withContext(Dispatchers.IO) {
            val startTime = System.currentTimeMillis()
            
            while (System.currentTimeMillis() - startTime < timeoutMs) {
                try {
                    val url = URL("$getServerUrl()/health")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 1000
                    connection.readTimeout = 1000
                    
                    if (connection.responseCode == 200) {
                        val response = connection.inputStream.bufferedReader().readText()
                        val json = JSONObject(response)
                        if (json.optString("status") == "ok") {
                            return@withContext true
                        }
                    }
                } catch (e: Exception) {
                    // Server not ready yet, continue waiting
                }
                
                delay(500)
            }
            
            false
        }
    
    private fun startHealthCheck() {
        healthCheckJob = scope.launch {
            while (isServerRunning.get()) {
                try {
                    val isHealthy = checkServerHealth()
                    if (!isHealthy) {
                        Log.w(TAG, "Server health check failed, attempting restart...")
                        restartServer()
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Health check error", e)
                }
                
                delay(HEALTH_CHECK_INTERVAL)
            }
        }
    }
    
    private suspend fun checkServerHealth(): Boolean = withContext(Dispatchers.IO) {
        try {
            val url = URL("$getServerUrl()/health")
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "GET"
            connection.connectTimeout = 3000
            connection.readTimeout = 3000
            
            connection.responseCode == 200
        } catch (e: Exception) {
            false
        }
    }
    
    private suspend fun restartServer() = withContext(Dispatchers.IO) {
        try {
            Log.i(TAG, "Restarting Aurora Local Server...")
            stop()
            delay(2000)
            start()
        } catch (e: Exception) {
            Log.e(TAG, "Failed to restart server", e)
        }
    }
    
    // API methods for interacting with the local server
    
    suspend fun getTSI(): Float = withContext(Dispatchers.IO) {
        try {
            val response = makeApiCall("/api/convergence/tsi", "GET")
            val json = JSONObject(response)
            json.optDouble("tsi", 0.0).toFloat()
        } catch (e: Exception) {
            Log.e(TAG, "Error getting TSI", e)
            0.0f
        }
    }
    
    suspend fun updateConvergenceMetrics(
        technical: Float,
        ai: Float,
        manufacturing: Float,
        integration: Float
    ): Boolean = withContext(Dispatchers.IO) {
        try {
            val payload = JSONObject().apply {
                put("technical", technical)
                put("ai", ai)
                put("manufacturing", manufacturing)
                put("integration", integration)
            }
            
            makeApiCall("/api/convergence/update", "POST", payload.toString())
            true
        } catch (e: Exception) {
            Log.e(TAG, "Error updating convergence metrics", e)
            false
        }
    }
    
    suspend fun getProposals(): List<Proposal> = withContext(Dispatchers.IO) {
        try {
            val response = makeApiCall("/api/governance/proposals", "GET")
            val json = JSONObject(response)
            val proposalsArray = json.getJSONArray("proposals")
            
            (0 until proposalsArray.length()).map { i ->
                val proposalJson = proposalsArray.getJSONObject(i)
                Proposal(
                    id = proposalJson.getString("id"),
                    title = proposalJson.getString("title"),
                    description = proposalJson.getString("description"),
                    status = proposalJson.getString("status"),
                    votingEnds = proposalJson.getLong("votingEnds")
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error getting proposals", e)
            emptyList()
        }
    }
    
    suspend fun castVote(
        proposalId: String,
        technical: Float,
        cultural: Float,
        cosmic: Float,
        temporal: Float,
        stake: Float
    ): Boolean = withContext(Dispatchers.IO) {
        try {
            val payload = JSONObject().apply {
                put("proposalId", proposalId)
                put("technical", technical)
                put("cultural", cultural)
                put("cosmic", cosmic)
                put("temporal", temporal)
                put("stake", stake)
            }
            
            makeApiCall("/api/governance/vote", "POST", payload.toString())
            true
        } catch (e: Exception) {
            Log.e(TAG, "Error casting vote", e)
            false
        }
    }
    
    suspend fun generateNoirProof(
        circuitType: String,
        inputs: Map<String, Any>
    ): String? = withContext(Dispatchers.IO) {
        try {
            val payload = JSONObject().apply {
                put("circuitType", circuitType)
                put("inputs", JSONObject(inputs))
            }
            
            val response = makeApiCall("/api/verification/generate", "POST", payload.toString())
            val json = JSONObject(response)
            json.optString("proof")
        } catch (e: Exception) {
            Log.e(TAG, "Error generating Noir proof", e)
            null
        }
    }
    
    suspend fun verifyNoirProof(
        proof: String,
        publicInputs: Map<String, Any>
    ): Boolean = withContext(Dispatchers.IO) {
        try {
            val payload = JSONObject().apply {
                put("proof", proof)
                put("publicInputs", JSONObject(publicInputs))
            }
            
            val response = makeApiCall("/api/verification/verify", "POST", payload.toString())
            val json = JSONObject(response)
            json.optBoolean("valid", false)
        } catch (e: Exception) {
            Log.e(TAG, "Error verifying Noir proof", e)
            false
        }
    }
    
    private suspend fun makeApiCall(
        endpoint: String,
        method: String,
        body: String? = null
    ): String = withContext(Dispatchers.IO) {
        val url = URL("$getServerUrl()$endpoint")
        val connection = url.openConnection() as HttpURLConnection
        
        connection.requestMethod = method
        connection.setRequestProperty("Content-Type", "application/json")
        connection.connectTimeout = 10000
        connection.readTimeout = 10000
        
        body?.let {
            connection.doOutput = true
            connection.outputStream.bufferedWriter().use { writer ->
                writer.write(it)
            }
        }
        
        if (connection.responseCode in 200..299) {
            connection.inputStream.bufferedReader().readText()
        } else {
            throw Exception("HTTP ${connection.responseCode}: ${connection.responseMessage}")
        }
    }
}

// Data classes for API responses
data class Proposal(
    val id: String,
    val title: String,
    val description: String,
    val status: String,
    val votingEnds: Long
)