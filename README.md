# DevDoc API Contracts

**Phase 1: Foundation**

## Purpose
This repository is the **Single Source of Truth** for all service-to-service communication in the DevDoc architecture. It prevents "contract drift" by strictly defining:

1.  **TypeScript Interfaces** (for Frontend, BFF, Journal Service)
2.  **pydantic Models** (for Python RAG Service)

## Installation

### TypeScript (Frontend, BFF, Journal)
```bash
npm install devdoc-contracts
# or
yarn add devdoc-contracts
```

Usage:
```typescript
import { RAGIndexRequest, JournalEntryWithGitContext } from 'devdoc-contracts';
```

### Python (RAG Service)
```bash
pip install devdoc-contracts
# or via poetry
poetry add devdoc_contracts
```

Usage:
```python
from devdoc_contracts import RAGIndexRequest, JournalEntryWithGitContext
```

## Core Contracts defined

### Journal <-> RAG
- `RAGIndexRequest`: Payload sent when indexing a new journal entry. Includes Git metadata.

### BFF <-> API
- `BFFProjectDashboardRequest/Response`: Aggregated data for the main dashboard.

### Shared Data Models
- `GitMetadata`: Standardized git context (hash, branch, author).
- `JournalEntryWithGitContext`: The enriched journal entity.

## Development
This is a hybrid repository.
- `src/types.ts`: Master TypeScript definitions.
- `src/devdoc_contracts/schemas.py`: Master Python Pydantic definitions.

**Note:** When you update one, you **MUST** update the other to keep them in sync.
