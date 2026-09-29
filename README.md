# TruthBridge

## Two Agents, One Truth

TruthBridge lets two AI agents examine the same question, produce competing claims, compare supporting evidence, and use Omega/MeTTa symbolic reasoning to produce an explainable resolution that a human can inspect and challenge.

## Problem

Different AI agents can give conflicting answers to the same question. TruthBridge makes the disagreement visible and records how the system evaluates the evidence and reaches its resolution.

## How It Works

Question
   |
   +-------------------+
   |                   |
   v                   v
Agent A             Agent B
ASI:One             ASI:One
   |                   |
   v                   v
Claim A             Claim B
   \                   /
    \                 /
     +---------------+
             |
             v
   Claim Relationship
             |
             v
    Evidence Evaluation
             |
             v
      Omega / MeTTa
   Symbolic Resolution
             |
             v
        Resolution
             |
             v
       Human Review
             |
             v
        Audit Trail

## Claim Relationships

TruthBridge identifies:

AGREE
QUALIFY
CONTRADICT
UNRELATED

The main competition scenario is:

Agent A -> Claim X
Agent B -> Claim Y
           |
       CONTRADICT

## Evidence

TruthBridge evaluates evidence using:

- source quality
- relevance
- directness
- freshness

Evidence is classified as:

strong
moderate
weak

## Omega / MeTTa

TruthBridge contains a real MeTTa plugin loaded through Omega.

Omega receives:

relationship
Agent A evidence strength
Agent B evidence strength

The MeTTa rules produce symbolic outcomes such as:

agreement
qualified-resolution
claim-a-better-supported
claim-b-better-supported
unresolved
insufficient-evidence

Example:

CONTRADICT
Agent A = strong
Agent B = weak

        |
        v
  Omega / MeTTa
        |
        v
claim-a-better-supported

The MeTTa rules are part of the actual resolution logic.

## Human Review

After the machine resolution, a human reviewer can accept or challenge it.

A challenge reason is recorded in the audit trail.

## Audit Trail

TruthBridge records:

- both claims
- both evidence items
- evidence scores
- claim relationship
- Python resolution
- Omega/MeTTa resolution
- human review decision
- human challenge reason

## Run

From the TruthBridge directory:

    cd ~/TruthBridge
    python app/pipeline.py

## Test the Agents

    python app/multi_agent_test.py

## Test Omega / MeTTa

    cd ~/PeTTa
    ./run.sh ~/TruthBridge/metta/test_truthbridge_rules.metta

## Project Structure

TruthBridge/
├── app/
│   ├── agent_a.py
│   ├── agent_b.py
│   ├── audit.py
│   ├── claim_relation.py
│   ├── demo_agents.py
│   ├── evidence.py
│   ├── evidence_evaluator.py
│   ├── multi_agent_test.py
│   ├── pipeline.py
│   ├── resolver.py
│   └── test_evidence.py
├── metta/
├── omega_plugin/
├── LICENSE
└── README.md

## AI Disclosure

TruthBridge was developed with AI assistance.

- ChatGPT was used for architecture, coding assistance, debugging, testing guidance, and documentation.
- ASI:One powers Agent A and Agent B at runtime.
- Omega/MeTTa powers the symbolic resolution rules at runtime.

The team is responsible for the implementation, testing, decisions, and final submission.

## What Comes Next

The hackathon version focuses on proving the core two-agent conflict-resolution behavior rather than building a complete platform.

Future extensions could include richer evidence provenance, persistent case history, additional negotiation strategies, and a graphical interface.
