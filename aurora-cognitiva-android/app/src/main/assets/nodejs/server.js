#!/usr/bin/env node

/**
 * Aurora Cognitiva Local Server
 * Embedded Node.js server for Android app
 * Implements blockchain, AI, and manufacturing convergence
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const crypto = require('crypto-js');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3001;
const HOST = process.env.HOST || '127.0.0.1';
const DATA_DIR = process.env.AURORA_DATA_DIR || './aurora_data';

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Aurora Components
const AuroraBlockchain = require('./modules/blockchain');
const AuroraAI = require('./modules/ai');
const AuroraManufacturing = require('./modules/manufacturing');
const AuroraNoir = require('./modules/noir');
const AuroraGovernance = require('./modules/governance');

class AuroraLocalServer {
    constructor() {
        this.blockchain = new AuroraBlockchain(DATA_DIR);
        this.ai = new AuroraAI(DATA_DIR);
        this.manufacturing = new AuroraManufacturing(DATA_DIR);
        this.noir = new AuroraNoir(DATA_DIR);
        this.governance = new AuroraGovernance(DATA_DIR);
        
        this.convergenceMetrics = {
            technical: 0.67,
            ai: 0.68,
            manufacturing: 0.71,
            integration: 0.62,
            lastUpdated: Date.now()
        };
        
        this.isInitialized = false;
    }

    async initialize() {
        console.log('🌅 Initializing Aurora Cognitiva Local Server...');
        
        try {
            // Initialize components
            await this.blockchain.initialize();
            await this.ai.initialize();
            await this.manufacturing.initialize();
            await this.noir.initialize();
            await this.governance.initialize();
            
            // Load saved state
            this.loadState();
            
            this.isInitialized = true;
            console.log('✅ Aurora Local Server initialized successfully');
        } catch (error) {
            console.error('❌ Failed to initialize Aurora Local Server:', error);
            throw error;
        }
    }

    loadState() {
        try {
            const statePath = path.join(DATA_DIR, 'aurora_state.json');
            if (fs.existsSync(statePath)) {
                const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
                this.convergenceMetrics = { ...this.convergenceMetrics, ...state.convergenceMetrics };
                console.log('📋 Loaded saved state');
            }
        } catch (error) {
            console.warn('⚠️  Failed to load state:', error.message);
        }
    }

    saveState() {
        try {
            const state = {
                convergenceMetrics: this.convergenceMetrics,
                timestamp: Date.now()
            };
            const statePath = path.join(DATA_DIR, 'aurora_state.json');
            fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
        } catch (error) {
            console.warn('⚠️  Failed to save state:', error.message);
        }
    }

    calculateTSI() {
        const { technical, ai, manufacturing, integration } = this.convergenceMetrics;
        
        // Weighted average: blockchain=40%, ai=40%, manufacturing=20%
        const weightedScore = (technical * 0.4 + ai * 0.4 + manufacturing * 0.2);
        
        // Apply integration multiplier
        const tsi = weightedScore * integration;
        
        return Math.round(tsi * 1000) / 1000; // Round to 3 decimal places
    }

    async simulateEvolution() {
        // Simulate natural evolution of the system
        const evolutionRate = 0.001; // 0.1% per minute
        
        setInterval(() => {
            // Simulate gradual improvement with some noise
            this.convergenceMetrics.technical = Math.min(1.0, 
                this.convergenceMetrics.technical + (Math.random() - 0.4) * evolutionRate);
            this.convergenceMetrics.ai = Math.min(1.0, 
                this.convergenceMetrics.ai + (Math.random() - 0.3) * evolutionRate);
            this.convergenceMetrics.manufacturing = Math.min(1.0, 
                this.convergenceMetrics.manufacturing + (Math.random() - 0.4) * evolutionRate);
            this.convergenceMetrics.integration = Math.min(1.0, 
                this.convergenceMetrics.integration + (Math.random() - 0.2) * evolutionRate);
            
            this.convergenceMetrics.lastUpdated = Date.now();
            this.saveState();
        }, 60000); // Update every minute
    }
}

// Create Aurora instance
const aurora = new AuroraLocalServer();

// Routes

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        initialized: aurora.isInitialized,
        timestamp: Date.now(),
        version: '1.0.0',
        components: {
            blockchain: aurora.blockchain.isReady(),
            ai: aurora.ai.isReady(),
            manufacturing: aurora.manufacturing.isReady(),
            noir: aurora.noir.isReady(),
            governance: aurora.governance.isReady()
        }
    });
});

// Convergence API
app.get('/api/convergence/tsi', (req, res) => {
    const tsi = aurora.calculateTSI();
    res.json({
        tsi: tsi,
        metrics: aurora.convergenceMetrics,
        phase: tsi >= 0.9 ? 'Meta' : tsi >= 0.75 ? 'Macro' : 'Micro'
    });
});

app.post('/api/convergence/update', (req, res) => {
    try {
        const { technical, ai, manufacturing, integration } = req.body;
        
        // Validate inputs
        if (technical < 0 || technical > 1 || ai < 0 || ai > 1 || 
            manufacturing < 0 || manufacturing > 1 || integration < 0 || integration > 1) {
            return res.status(400).json({ error: 'Metrics must be between 0 and 1' });
        }
        
        aurora.convergenceMetrics = {
            technical: parseFloat(technical),
            ai: parseFloat(ai),
            manufacturing: parseFloat(manufacturing),
            integration: parseFloat(integration),
            lastUpdated: Date.now()
        };
        
        aurora.saveState();
        
        res.json({
            success: true,
            tsi: aurora.calculateTSI(),
            metrics: aurora.convergenceMetrics
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Governance API
app.get('/api/governance/proposals', async (req, res) => {
    try {
        const proposals = await aurora.governance.getProposals();
        res.json({ proposals });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/governance/vote', async (req, res) => {
    try {
        const { proposalId, technical, cultural, cosmic, temporal, stake } = req.body;
        
        const voteResult = await aurora.governance.castVote({
            proposalId,
            technical: parseFloat(technical),
            cultural: parseFloat(cultural),
            cosmic: parseFloat(cosmic),
            temporal: parseFloat(temporal),
            stake: parseFloat(stake)
        });
        
        res.json({ success: true, voteResult });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/governance/proposal', async (req, res) => {
    try {
        const { title, description, category } = req.body;
        
        const proposal = await aurora.governance.createProposal({
            title,
            description,
            category,
            createdAt: Date.now()
        });
        
        res.json({ success: true, proposal });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Manufacturing API
app.get('/api/manufacturing/jobs', async (req, res) => {
    try {
        const jobs = await aurora.manufacturing.getJobs();
        res.json({ jobs });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/manufacturing/optimize', async (req, res) => {
    try {
        const { designData, constraints } = req.body;
        
        const optimizedDesign = await aurora.ai.optimizeDesign(designData, constraints);
        const job = await aurora.manufacturing.createJob({
            originalDesign: designData,
            optimizedDesign,
            status: 'optimized',
            createdAt: Date.now()
        });
        
        res.json({ success: true, job, optimizedDesign });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/manufacturing/job', async (req, res) => {
    try {
        const { designHash, parameters } = req.body;
        
        const job = await aurora.manufacturing.createJob({
            designHash,
            parameters,
            status: 'pending',
            createdAt: Date.now()
        });
        
        res.json({ success: true, job });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// AI API
app.post('/api/ai/predict', async (req, res) => {
    try {
        const { input, modelType } = req.body;
        
        const prediction = await aurora.ai.predict(input, modelType);
        
        res.json({ success: true, prediction });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/ai/models', async (req, res) => {
    try {
        const models = await aurora.ai.getAvailableModels();
        res.json({ models });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Noir Verification API
app.post('/api/verification/generate', async (req, res) => {
    try {
        const { circuitType, inputs } = req.body;
        
        const proof = await aurora.noir.generateProof(circuitType, inputs);
        
        res.json({ success: true, proof });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/verification/verify', async (req, res) => {
    try {
        const { proof, publicInputs } = req.body;
        
        const isValid = await aurora.noir.verifyProof(proof, publicInputs);
        
        res.json({ success: true, valid: isValid });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/verification/circuits', async (req, res) => {
    try {
        const circuits = await aurora.noir.getAvailableCircuits();
        res.json({ circuits });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Blockchain API
app.get('/api/blockchain/status', async (req, res) => {
    try {
        const status = await aurora.blockchain.getStatus();
        res.json({ status });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/blockchain/transaction', async (req, res) => {
    try {
        const { to, value, data } = req.body;
        
        const txHash = await aurora.blockchain.sendTransaction({ to, value, data });
        
        res.json({ success: true, txHash });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Sync API (for internet connectivity)
app.post('/api/sync/upload', async (req, res) => {
    try {
        const { data, type } = req.body;
        
        // Store data for later upload to global network
        const syncData = {
            data,
            type,
            timestamp: Date.now(),
            synced: false
        };
        
        const syncPath = path.join(DATA_DIR, 'sync_queue.json');
        let syncQueue = [];
        
        if (fs.existsSync(syncPath)) {
            syncQueue = JSON.parse(fs.readFileSync(syncPath, 'utf8'));
        }
        
        syncQueue.push(syncData);
        fs.writeFileSync(syncPath, JSON.stringify(syncQueue, null, 2));
        
        res.json({ success: true, queued: true });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/sync/status', (req, res) => {
    try {
        const syncPath = path.join(DATA_DIR, 'sync_queue.json');
        let pendingSync = 0;
        
        if (fs.existsSync(syncPath)) {
            const syncQueue = JSON.parse(fs.readFileSync(syncPath, 'utf8'));
            pendingSync = syncQueue.filter(item => !item.synced).length;
        }
        
        res.json({
            pendingSync,
            lastSync: aurora.convergenceMetrics.lastUpdated,
            isOnline: false // Will be updated by Android app
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// WebSocket for real-time updates
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('📱 Client connected');
    
    // Send current state
    ws.send(JSON.stringify({
        type: 'state',
        data: {
            tsi: aurora.calculateTSI(),
            metrics: aurora.convergenceMetrics,
            initialized: aurora.isInitialized
        }
    }));
    
    ws.on('close', () => {
        console.log('📱 Client disconnected');
    });
});

// Error handling
app.use((err, req, res, next) => {
    console.error('Server Error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
async function startServer() {
    try {
        await aurora.initialize();
        aurora.simulateEvolution();
        
        server.listen(PORT, HOST, () => {
            console.log(`🌅 Aurora Cognitiva Local Server running on http://${HOST}:${PORT}`);
            console.log(`📊 Initial TSI: ${aurora.calculateTSI()}`);
            console.log(`🔗 WebSocket server ready for real-time updates`);
        });
    } catch (error) {
        console.error('❌ Failed to start server:', error);
        process.exit(1);
    }
}

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('🛑 Shutting down Aurora Local Server...');
    aurora.saveState();
    server.close(() => {
        console.log('✅ Server shut down gracefully');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('🛑 Shutting down Aurora Local Server...');
    aurora.saveState();
    server.close(() => {
        console.log('✅ Server shut down gracefully');
        process.exit(0);
    });
});

// Start the server
startServer();