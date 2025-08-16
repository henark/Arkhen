import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { BlockchainService } from './services/blockchainService';
import { BlockchainConfig } from './types';
import { logger } from './utils/logger';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Basic Middleware
app.use(cors());
app.use(helmet());
app.use(express.json());

// Placeholder for Blockchain Configuration
// In a real app, this would come from a more secure and robust config system
const blockchainConfig: BlockchainConfig = {
  rpcUrl: process.env.RPC_URL || 'http://localhost:8545',
  contractAddress: process.env.CONTRACT_ADDRESS || '0x5FbDB2315678afecb367f032d93F642f64180aa3', // Example address
  maxGasPrice: '50' // in gwei
};

// Instantiate Blockchain Service
let blockchainService: BlockchainService;
try {
  blockchainService = new BlockchainService(blockchainConfig);
  logger.info('Blockchain Service instantiated.');
} catch (error) {
  logger.error('Failed to instantiate Blockchain Service.', { error: error instanceof Error ? error.message : 'Unknown error' });
  // We can choose to exit if the blockchain connection is critical
  // process.exit(1);
}


// --- API Routes ---

// Root health check endpoint
app.get('/', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'ok',
    message: 'Eudaimonic IoT Backend is running.',
    blockchainHealthy: blockchainService ? blockchainService.isHealthy() : false
  });
});

// Endpoint to get system stats from the blockchain
app.get('/stats', async (req: Request, res: Response) => {
  if (!blockchainService) {
    return res.status(503).json({ error: 'Blockchain service is not available.' });
  }

  try {
    const stats = await blockchainService.getSystemStats();
    // Convert BigInts to strings for JSON serialization
    const serializedStats = {
      totalProduced: stats.totalProduced.toString(),
      totalCredits: stats.totalCredits.toString(),
      totalMembers: stats.totalMembers.toString(),
      currentFeeRate: stats.currentFeeRate.toString()
    };
    res.status(200).json(serializedStats);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    logger.error('Failed to retrieve system stats', { error: errorMessage });
    res.status(500).json({ error: 'Failed to retrieve system stats', details: errorMessage });
  }
});


// --- Server Initialization ---

app.listen(PORT, async () => {
  logger.info(`Server is running on port ${PORT}`);
  if (blockchainService) {
    const isHealthy = await blockchainService.healthCheck();
    logger.info(`Initial blockchain health check: ${isHealthy ? 'OK' : 'Failed'}`);
  }
});

export default app;
