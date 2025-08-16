// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./governance/HolographicGovernor.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

/**
 * @title AuroraCognitivaCore
 * @notice Core contract implementing Aurora Cognitiva Phase 1 convergence of 
 *         blockchain, AI, and 3D manufacturing with holographic governance
 * @dev Extends eudaimonic engineering principles with cosmic-scale verification
 */
contract AuroraCognitivaCore is ReentrancyGuard, AccessControl {
    using SafeMath for uint256;

    // Role definitions
    bytes32 public constant AI_ORACLE_ROLE = keccak256("AI_ORACLE_ROLE");
    bytes32 public constant MANUFACTURING_ROLE = keccak256("MANUFACTURING_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

    // Core Aurora structures
    struct ConvergenceMetrics {
        uint256 technicalSynergy;     // [0, 1000] - blockchain performance
        uint256 aiOptimization;       // [0, 1000] - AI efficiency metrics  
        uint256 manufacturingQuality; // [0, 1000] - 3D print success rate
        uint256 integration;          // [0, 1000] - cross-system coherence
        uint256 timestamp;
        address reporter;
    }

    struct HolographicProposal {
        uint256 id;
        address proposer;
        string title;
        string description;
        bytes32 technicalHash;        // Hash of technical specification
        bytes32 culturalHash;         // Hash of cultural impact assessment
        bytes32 noirProofHash;        // Hash of verification proof
        uint256 createdAt;
        uint256 votingEnds;
        bool executed;
        mapping(address => HolographicVote) votes;
        uint256 totalVotingPower;
    }

    struct HolographicVote {
        uint256 technicalPreference;  // [0, 1000] technical merit
        uint256 culturalAlignment;    // [0, 1000] cultural resonance
        uint256 cosmicWisdom;         // [0, 1000] universal principles
        uint256 temporalImpact;       // [0, 1000] long-term effects
        uint256 stakeCommitment;      // Amount of tokens committed
        bool hasVoted;
    }

    struct ManufacturingJob {
        uint256 id;
        address requester;
        bytes32 designHash;
        bytes32 aiOptimizationHash;
        bytes32 qualityProofHash;
        uint256 createdAt;
        uint256 completedAt;
        ManufacturingStatus status;
        uint256 qualityScore;         // [0, 1000]
    }

    enum ManufacturingStatus {
        Pending,
        InProgress,
        Completed,
        Failed,
        Verified
    }

    // State variables
    mapping(uint256 => ConvergenceMetrics) public convergenceHistory;
    mapping(uint256 => HolographicProposal) public proposals;
    mapping(uint256 => ManufacturingJob) public manufacturingJobs;
    mapping(address => uint256) public stakeholderPower;
    mapping(bytes32 => bool) public verifiedProofs;

    uint256 public currentConvergenceIndex;
    uint256 public proposalCounter;
    uint256 public jobCounter;
    uint256 public constant VOTING_PERIOD = 7 days;
    uint256 public constant MIN_VOTING_POWER = 100;

    // Events
    event ConvergenceUpdated(
        uint256 indexed index,
        uint256 technicalSynergy,
        uint256 aiOptimization, 
        uint256 manufacturingQuality,
        uint256 integration
    );

    event HolographicProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        string title
    );

    event HolographicVoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        uint256 totalPower
    );

    event ManufacturingJobCreated(
        uint256 indexed jobId,
        address indexed requester,
        bytes32 designHash
    );

    event NoirProofVerified(
        bytes32 indexed proofHash,
        address indexed verifier,
        bool isValid
    );

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(AI_ORACLE_ROLE, msg.sender);
        _grantRole(MANUFACTURING_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
    }

    /**
     * @notice Update convergence metrics from the three technology pillars
     * @param _technical Blockchain/smart contract performance [0,1000]
     * @param _ai AI optimization and learning metrics [0,1000]  
     * @param _manufacturing 3D manufacturing quality and efficiency [0,1000]
     * @param _integration Cross-system integration score [0,1000]
     */
    function updateConvergenceMetrics(
        uint256 _technical,
        uint256 _ai,
        uint256 _manufacturing,
        uint256 _integration
    ) external onlyRole(AI_ORACLE_ROLE) {
        require(_technical <= 1000 && _ai <= 1000 && 
                _manufacturing <= 1000 && _integration <= 1000,
                "Metrics must be <= 1000");

        currentConvergenceIndex++;
        
        convergenceHistory[currentConvergenceIndex] = ConvergenceMetrics({
            technicalSynergy: _technical,
            aiOptimization: _ai,
            manufacturingQuality: _manufacturing,
            integration: _integration,
            timestamp: block.timestamp,
            reporter: msg.sender
        });

        emit ConvergenceUpdated(
            currentConvergenceIndex,
            _technical,
            _ai,
            _manufacturing,
            _integration
        );
    }

    /**
     * @notice Calculate Technology Synergy Index (TSI) from current metrics
     * @return TSI value [0,1000] representing overall Aurora convergence
     */
    function calculateTSI() external view returns (uint256) {
        if (currentConvergenceIndex == 0) return 0;
        
        ConvergenceMetrics memory current = convergenceHistory[currentConvergenceIndex];
        
        // Weighted average: blockchain=40%, ai=40%, manufacturing=20%
        uint256 weightedScore = (current.technicalSynergy.mul(400)
            .add(current.aiOptimization.mul(400))
            .add(current.manufacturingQuality.mul(200)))
            .div(1000);
            
        // Apply integration multiplier
        return weightedScore.mul(current.integration).div(1000);
    }

    /**
     * @notice Create a holographic proposal for system evolution
     * @param _title Proposal title
     * @param _description Detailed description
     * @param _technicalHash Hash of technical specifications
     * @param _culturalHash Hash of cultural impact assessment
     * @param _noirProofHash Hash of Noir verification proof
     */
    function createHolographicProposal(
        string memory _title,
        string memory _description,
        bytes32 _technicalHash,
        bytes32 _culturalHash,
        bytes32 _noirProofHash
    ) external returns (uint256) {
        require(stakeholderPower[msg.sender] >= MIN_VOTING_POWER, 
                "Insufficient voting power to create proposal");
        require(verifiedProofs[_noirProofHash], "Noir proof not verified");

        proposalCounter++;
        uint256 proposalId = proposalCounter;

        HolographicProposal storage proposal = proposals[proposalId];
        proposal.id = proposalId;
        proposal.proposer = msg.sender;
        proposal.title = _title;
        proposal.description = _description;
        proposal.technicalHash = _technicalHash;
        proposal.culturalHash = _culturalHash;
        proposal.noirProofHash = _noirProofHash;
        proposal.createdAt = block.timestamp;
        proposal.votingEnds = block.timestamp.add(VOTING_PERIOD);
        proposal.executed = false;

        emit HolographicProposalCreated(proposalId, msg.sender, _title);
        return proposalId;
    }

    /**
     * @notice Cast a holographic vote with multiple dimensions
     * @param _proposalId ID of the proposal to vote on
     * @param _technical Technical preference [0,1000]
     * @param _cultural Cultural alignment [0,1000]
     * @param _cosmic Cosmic wisdom contribution [0,1000]
     * @param _temporal Temporal impact consideration [0,1000]
     * @param _stakeCommitment Amount of tokens to commit
     */
    function castHolographicVote(
        uint256 _proposalId,
        uint256 _technical,
        uint256 _cultural,
        uint256 _cosmic,
        uint256 _temporal,
        uint256 _stakeCommitment
    ) external nonReentrant {
        HolographicProposal storage proposal = proposals[_proposalId];
        require(proposal.id != 0, "Proposal does not exist");
        require(block.timestamp <= proposal.votingEnds, "Voting period ended");
        require(!proposal.votes[msg.sender].hasVoted, "Already voted");
        require(_technical <= 1000 && _cultural <= 1000 && 
                _cosmic <= 1000 && _temporal <= 1000, "Invalid vote values");
        require(_stakeCommitment <= stakeholderPower[msg.sender], 
                "Insufficient stake");

        // Calculate holographic voting power using quadratic formula
        uint256 basePower = sqrt(_stakeCommitment);
        
        // Apply dimensional multipliers (simplified for demo)
        uint256 culturalMultiplier = (_cultural.add(500)).div(500); // [0.5, 2.0]
        uint256 cosmicMultiplier = (_cosmic.add(500)).div(500);     // [0.5, 2.0]
        uint256 temporalMultiplier = (_temporal.add(500)).div(500); // [0.5, 2.0]
        
        uint256 totalPower = basePower
            .mul(culturalMultiplier)
            .mul(cosmicMultiplier)
            .mul(temporalMultiplier)
            .div(1000000); // Normalize

        proposal.votes[msg.sender] = HolographicVote({
            technicalPreference: _technical,
            culturalAlignment: _cultural,
            cosmicWisdom: _cosmic,
            temporalImpact: _temporal,
            stakeCommitment: _stakeCommitment,
            hasVoted: true
        });

        proposal.totalVotingPower = proposal.totalVotingPower.add(totalPower);

        emit HolographicVoteCast(_proposalId, msg.sender, totalPower);
    }

    /**
     * @notice Create a manufacturing job with AI optimization
     * @param _designHash IPFS hash of 3D design file
     * @param _aiOptimizationHash Hash of AI optimization parameters
     * @return jobId Unique identifier for the manufacturing job
     */
    function createManufacturingJob(
        bytes32 _designHash,
        bytes32 _aiOptimizationHash
    ) external returns (uint256) {
        require(_designHash != bytes32(0), "Invalid design hash");
        
        jobCounter++;
        uint256 jobId = jobCounter;

        manufacturingJobs[jobId] = ManufacturingJob({
            id: jobId,
            requester: msg.sender,
            designHash: _designHash,
            aiOptimizationHash: _aiOptimizationHash,
            qualityProofHash: bytes32(0),
            createdAt: block.timestamp,
            completedAt: 0,
            status: ManufacturingStatus.Pending,
            qualityScore: 0
        });

        emit ManufacturingJobCreated(jobId, msg.sender, _designHash);
        return jobId;
    }

    /**
     * @notice Update manufacturing job status and quality
     * @param _jobId Manufacturing job ID
     * @param _status New status
     * @param _qualityScore Quality score [0,1000]
     * @param _qualityProofHash Noir proof of quality verification
     */
    function updateManufacturingJob(
        uint256 _jobId,
        ManufacturingStatus _status,
        uint256 _qualityScore,
        bytes32 _qualityProofHash
    ) external onlyRole(MANUFACTURING_ROLE) {
        ManufacturingJob storage job = manufacturingJobs[_jobId];
        require(job.id != 0, "Job does not exist");
        require(_qualityScore <= 1000, "Invalid quality score");

        job.status = _status;
        job.qualityScore = _qualityScore;
        job.qualityProofHash = _qualityProofHash;

        if (_status == ManufacturingStatus.Completed || 
            _status == ManufacturingStatus.Failed) {
            job.completedAt = block.timestamp;
        }
    }

    /**
     * @notice Verify a Noir proof for system integrity
     * @param _proofHash Hash of the Noir proof
     * @param _isValid Whether the proof verification succeeded
     */
    function verifyNoirProof(
        bytes32 _proofHash,
        bool _isValid
    ) external onlyRole(VERIFIER_ROLE) {
        verifiedProofs[_proofHash] = _isValid;
        emit NoirProofVerified(_proofHash, msg.sender, _isValid);
    }

    /**
     * @notice Grant stakeholder voting power
     * @param _stakeholder Address to grant power to
     * @param _power Voting power amount
     */
    function grantStakeholderPower(
        address _stakeholder,
        uint256 _power
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        stakeholderPower[_stakeholder] = _power;
    }

    /**
     * @notice Get convergence trend over time
     * @param _fromIndex Starting index
     * @param _toIndex Ending index  
     * @return trends Array of TSI values
     */
    function getConvergenceTrend(
        uint256 _fromIndex,
        uint256 _toIndex
    ) external view returns (uint256[] memory trends) {
        require(_fromIndex <= _toIndex && _toIndex <= currentConvergenceIndex,
                "Invalid index range");
        
        uint256 length = _toIndex.sub(_fromIndex).add(1);
        trends = new uint256[](length);
        
        for (uint256 i = 0; i < length; i++) {
            uint256 index = _fromIndex.add(i);
            ConvergenceMetrics memory metrics = convergenceHistory[index];
            
            // Calculate TSI for this point
            uint256 weightedScore = (metrics.technicalSynergy.mul(400)
                .add(metrics.aiOptimization.mul(400))
                .add(metrics.manufacturingQuality.mul(200)))
                .div(1000);
                
            trends[i] = weightedScore.mul(metrics.integration).div(1000);
        }
    }

    /**
     * @notice Calculate square root using Babylonian method
     * @param x Input number
     * @return y Square root of x
     */
    function sqrt(uint256 x) internal pure returns (uint256 y) {
        if (x == 0) return 0;
        uint256 z = x.add(1).div(2);
        y = x;
        while (z < y) {
            y = z;
            z = x.div(z).add(z).div(2);
        }
    }

    /**
     * @notice Get system health metrics
     * @return technicalHealth Current technical performance
     * @return aiHealth Current AI optimization level
     * @return manufacturingHealth Current manufacturing quality
     * @return overallTSI Overall technology synergy index
     */
    function getSystemHealth() external view returns (
        uint256 technicalHealth,
        uint256 aiHealth,
        uint256 manufacturingHealth,
        uint256 overallTSI
    ) {
        if (currentConvergenceIndex == 0) {
            return (0, 0, 0, 0);
        }
        
        ConvergenceMetrics memory current = convergenceHistory[currentConvergenceIndex];
        technicalHealth = current.technicalSynergy;
        aiHealth = current.aiOptimization;
        manufacturingHealth = current.manufacturingQuality;
        
        // Calculate TSI
        uint256 weightedScore = (current.technicalSynergy.mul(400)
            .add(current.aiOptimization.mul(400))
            .add(current.manufacturingQuality.mul(200)))
            .div(1000);
            
        overallTSI = weightedScore.mul(current.integration).div(1000);
    }
}