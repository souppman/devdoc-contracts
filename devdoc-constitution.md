# **DEVDOC PROJECT CONSTITUTION & AI AGENT PRIMER**
**Project:** DevDoc - AI-Powered Documentation Generator with Developer Journal  
**Status:** ENTERPRISE PRODUCTION GRADE  
**Architecture Version:** 2.0 (Modular API-First)  
**Last Updated:** new  
**Authority:** Lead Architect & Principal Engineer  
**Compliance:** REQUIRED FOR ALL AGENTS & DEVELOPERS  

---

## **1.0 ARCHITECTURAL SUPREMACY & CORE PRINCIPLES**

### **1.1 FOUNDATIONAL RULE: EXPLAIN BEFORE EXECUTE**
**"You are an expert, enterprise-grade, production-ready, full-stack engineer."**  
Before ANY code, API design, or architectural decision:
1. **ANALYZE** the problem against our established architecture
2. **ARTICULATE** your proposed solution with reference to this document
3. **JUSTIFY** technology choices against our stack constraints
4. **DOCUMENT** the decision in the architecture log

### **1.2 MODULARITY AS RELIGION**
Our system is **NOT** a monolith. It is a federation of specialized services communicating via **strict API contracts**. Violating this principle is the highest offense.

**Architecture Visualization:**
```
┌─────────────────┐     ┌───────────────────┐     ┌─────────────────────┐
│   NEXT.JS       │     │   BFF/GATEWAY     │     │   JOURNAL & GIT     │
│   FRONTEND      │────▶│   (Next.js API)   │────▶│   SERVICE           │
│   (TypeScript)  │  1  │   (TypeScript)    │  2  │   (TypeScript/Node) │
└─────────────────┘     └───────────────────┘     └──────────┬──────────┘
         ▲                                                  │ 4
         │ 6                                                ▼
         │                                          ┌─────────────────────┐
    ┌────┴────┐                                    │   RAG & AI SERVICE  │
    │  USER   │                                    │   (Python/FastAPI)  │
    └─────────┘                                    └──────────┬──────────┘
                                                               │
                                               ┌───────────────┼───────────────┐
                                               │               │               │
                                               ▼               ▼               ▼
                                        ┌──────────┐   ┌──────────┐   ┌──────────┐
                                        │ PINECONE │   │ OPENAI/  │   │ S3       │
                                        │ (Vector) │   │ CLAUDE   │   │ (Export) │
                                        └──────────┘   └──────────┘   └──────────┘
```

**Numbered Contracts:**
- **1:** REST/GraphQL for UI data (Next.js → BFF)
- **2:** Internal REST for orchestration (BFF → Journal Service)
- **3:** Internal REST for AI tasks (BFF → RAG Service)
- **4:** `RAGIndexRequest` for indexing (Journal → RAG Service)
- **5a/b:** GitHub webhooks & Supabase operations (Journal Service → External)
- **6a/b/c:** Vector queries, LLM calls, storage (RAG Service → External)

### **1.3 TECHNOLOGY STACK (NON-NEGOTIABLE)**
| Component | Technology | Justification | Official Docs |
|-----------|------------|---------------|---------------|
| **Frontend** | Next.js 15 (App Router), TypeScript, CodeMirror 6 | Server components, type safety, proven editor | [Next.js](https://nextjs.org/docs) |
| **BFF Layer** | Next.js API Routes, tRPC | Colocation with frontend, end-to-end types | [tRPC](https://trpc.io/docs) |
| **Journal Service** | Node.js + Express/Fastify, TypeScript, Prisma | API logic, type consistency, ORM maturity | [Prisma](https://www.prisma.io/docs) |
| **RAG & AI Service** | Python 3.11+, FastAPI, LlamaIndex, Pydantic | AI ecosystem dominance, async API, validation | [FastAPI](https://fastapi.tiangolo.com/) |
| **Primary Database** | Supabase (PostgreSQL) | Auth, realtime, managed PostgreSQL | [Supabase](https://supabase.com/docs) |
| **Vector Database** | Pinecone | Production vector operations, managed service | [Pinecone](https://docs.pinecone.io/) |
| **External Integrations** | GitHub REST API, Slack Webhooks, Jira API | Industry standard APIs | [GitHub](https://docs.github.com/en/rest) |

---

## **2.0 DEVELOPMENT PROTOCOLS & WORKFLOWS**

### **2.1 THE PRIMACY OF API CONTRACTS**
All service communication MUST use these defined contracts:

**Contract A: Journal → RAG Service (Indexing)**
```typescript
// FROM: devdoc-contracts package (shared dependency)
interface RAGIndexRequest {
  content: string;
  metadata: {
    id: string; // "journal_entry_123" or "code_file_abc"
    source: 'journal' | 'code_file' | 'commit_message';
    project_id: string;
    git_commit_hash?: string; // CRITICAL: Links to Git
    git_branch?: string;
    file_path?: string;
    author_id: string;
    created_at: ISOString;
    linked_jira_issue?: string;
  };
}
```

**Contract B: BFF → Services (Orchestration)**
```typescript
// BFF aggregates data from multiple services
interface BFFProjectDashboardResponse {
  project: ProjectMeta;
  recent_commits: GitCommit[];
  journal_entries: JournalEntry[];
  documentation: DocSection[];
  // All data formatted for UI consumption
}
```

**ENFORCEMENT:** Services must import types from `devdoc-contracts` package. No ad-hoc types.

### **2.2 SERVICE RESPONSIBILITY MATRIX**
| Service | Owns | Never Touches | Communication Pattern |
|---------|------|---------------|----------------------|
| **Frontend** | UI state, components, user interactions | Business logic, database queries | Calls BFF only via defined endpoints |
| **BFF** | Request orchestration, auth, API aggregation | External service integration logic | Calls Journal & RAG services, formats UI responses |
| **Journal Service** | Journal CRUD, Git metadata, webhook handling | AI/LLM logic, vector operations | Calls RAG `/index` endpoint, stores in Supabase |
| **RAG Service** | Vector indexing, retrieval, LLM prompting, doc generation | Git operations, user management, journal storage | Called by Journal & BFF, uses Pinecone/OpenAI |

### **2.3 DATA FLOW WORKFLOWS (HOW THINGS ACTUALLY WORK)**

**Workflow 1: Developer Journals a Commit**
```
TRIGGER: Developer submits journal entry in UI
1. Frontend → BFF (`POST /api/journal`)
2. BFF → Journal Service (`POST /journal/entries` with git_context)
3. Journal Service:
   a. Validates Git context (commit hash exists in repo)
   b. Stores in Supabase (journal_entries table)
   c. → RAG Service (`POST /index` with RAGIndexRequest)
4. RAG Service:
   a. Creates embedding via OpenAI
   b. Stores in Pinecone with metadata
   c. Returns vector_id to Journal Service
OUTPUT: Journal entry stored in 2 systems: relational (Supabase) + vector (Pinecone)
```

**Workflow 2: AI Generates Context-Aware Documentation**
```
TRIGGER: User requests "Explain auth middleware"
1. Frontend → BFF (`POST /api/rag/query`)
2. BFF → RAG Service (`POST /query` with filters)
3. RAG Service:
   a. Converts query to embedding
   b. Queries Pinecone for top 10 relevant chunks (code + journal)
   c. Constructs LLM prompt with: "Using context, generate docs..."
   d. Calls OpenAI/Claude with prompt
   e. Returns structured documentation
4. BFF formats, returns to Frontend
OUTPUT: Non-generic docs citing specific code lines and journal notes
```

**Workflow 3: Keeping Docs Fresh (Staleness Prevention)**
```
TRIGGER: GitHub webhook on push to main
1. GitHub → Journal Service (`POST /webhooks/github`)
2. Journal Service:
   a. Parses commit diff for changed files
   b. → RAG Service (`POST /query` filtered by file_path)
   c. Receives affected documentation IDs
   d. Flags docs as "stale" in Supabase
   e. Optionally triggers regeneration via BFF
3. UI shows "⚠️ This doc references old code" badge
OUTPUT: Proactive staleness detection, never silently outdated docs
```

---

## **3.0 AI AGENT INTERACTION PROTOCOLS**

### **3.1 BEFORE ANY EXECUTION: THE EXPLANATION MANDATE**
When tasked with implementation:
1. **STATE:** "As enterprise architect, analyzing requirement..."
2. **REFERENCE:** Cite relevant section of this Constitution
3. **MAP:** Diagram how solution fits in architecture (ASCII or mermaid)
4. **VALIDATE:** Check against stack constraints and API contracts
5. **PROPOSE:** Offer 1-2 implementation options with tradeoffs
6. **WAIT:** For explicit approval before writing code

### **3.2 IMPLEMENTATION TEMPLATE FOR AGENTS**
```
## **ARCHITECTURAL ANALYSIS** [Required Section]

**Requirement:** [Briefly restate task]
**Relevant Constitution Sections:** [Cite 1.2, 2.1, etc.]

**Service Impact Analysis:**
- Frontend Changes: [Yes/No] - [Details]
- BFF Changes: [Yes/No] - [New endpoint?]
- Journal Service: [Yes/No] - [Database schema?]
- RAG Service: [Yes/No] - [New index type?]
- External Services: [GitHub/Supabase/Pinecone impact]

**API Contract Review:**
- Existing contracts affected: [List]
- New contracts needed: [Propose interface]
- Contract versioning: [Backward compatible?]

**Data Flow Diagram:**
[ASCII or description of new flow]

## **PROPOSED SOLUTION** [After analysis]

**Option 1: [Preferred approach]**
- Implementation steps (1. 2. 3.)
- Compliance check: [✓] Constitutional
- Risk assessment: Low/Medium/High

**Option 2: [Alternative if requested]**
- [Brief alternative]

**Official Documentation References:**
- [Next.js docs link for relevant API]
- [FastAPI docs for endpoint pattern]
- [LlamaIndex docs for retrieval method]

## **AWAITING APPROVAL TO PROCEED**
```

### **3.3 PROHIBITED ACTIONS (ZERO TOLERANCE)**
1. **NO** direct database access from Frontend (always via BFF)
2. **NO** bypassing API contracts with ad-hoc communication
3. **NO** mixing TypeScript and Python responsibilities
4. **NO** implementing Git logic in RAG service
5. **NO** implementing AI logic in Journal service
6. **NO** silent failures - all errors must be logged and surfaced
7. **NO** deviation from shared type contracts without team approval

---

## **4.0 DEPLOYMENT & PRODUCTION READINESS**

### **4.1 SERVICE BOOTSTRAP SEQUENCE**
```
PHASE 1 (Weeks 1-2): Foundations
1. Create devdoc-contracts package (v0.1.0)
2. Scaffold RAG Service (Python/FastAPI) - mock endpoints
3. Scaffold Journal Service (TypeScript/Express) - basic CRUD
4. Verify contract compliance between services

PHASE 2 (Weeks 3-5): Core AI & Integration
5. Implement RAG indexing pipeline (LlamaIndex + Pinecone)
6. Implement Journal Git integration (GitHub webhooks)
7. Connect Journal → RAG indexing flow
8. Basic BFF orchestration endpoints

PHASE 3 (Weeks 6-8): UI & Production Polish
9. Frontend with journal editor (CodeMirror)
10. Complete BFF for all UI data needs
11. Staleness detection system
12. Export to S3 feature
```

### **4.2 PRODUCTION CHECKLIST (PER SERVICE)**
**RAG Service (Python) Must Have:**
- [ ] Request/response validation with Pydantic
- [ ] Async/await for all external calls (OpenAI, Pinecone)
- [ ] Comprehensive error handling with retry logic
- [ ] Request logging with correlation IDs
- [ ] Health check endpoint (`/health`)
- [ ] Rate limiting per API key
- [ ] Unit tests for embedding generation
- [ ] Integration tests with Pinecone mock

**Journal Service (TypeScript) Must Have:**
- [ ] Database migrations versioned (Prisma)
- [ ] GitHub webhook signature verification
- [ ] Transaction handling for journal+index operations
- [ ] Proper error rollback if RAG indexing fails
- [ ] Environment-based configuration
- [ ] Structured logging (Pino or Winston)
- [ ] Input validation (Zod)
- [ ] API documentation (Swagger/OpenAPI)

**BFF (Next.js) Must Have:**
- [ ] End-to-end type safety (tRPC preferred)
- [ ] Authentication middleware (Supabase auth)
- [ ] Request validation at edge
- [ ] Response caching where appropriate
- [ ] Circuit breaker pattern for service calls
- [ ] Comprehensive error formatting for UI
- [ ] API versioning strategy

---

## **5.0 REFERENCE & COMPLIANCE**

### **5.1 QUICK DECISION TREE FOR AGENTS**
```
Question: "Where should I implement [feature]?"
           │
           ▼
    "Which service OWNS this data/concern?"
           │
           ├── Git metadata, journal entries? → JOURNAL SERVICE
           │
           ├── Vector search, AI generation? → RAG SERVICE  
           │
           ├── UI data aggregation, auth? → BFF
           │
           └── React components, editor UI? → FRONTEND
```

### **5.2 CONSTITUTIONAL AMENDMENT PROCESS**
This document is versioned. Proposed changes must:
1. Be submitted as PR to `devdoc-constitution.md`
2. Include impact analysis on all services
3. Demonstrate backward compatibility
4. Receive approval from 2 senior architects
5. Update version number and changelog

### **5.3 IMMUTABLE PRINCIPLES (CANNOT BE AMENDED)**
1. **Modularity Principle:** Services are independent, communicate via APIs
2. **Contract First:** All inter-service communication uses shared types
3. **Python for AI:** RAG/LLM logic exclusively in Python service
4. **BFF Isolation:** Frontend only communicates with BFF
5. **Git Context Binding:** Journal entries must link to commit metadata at creation

---

**CONSTITUTION ACKNOWLEDGMENT**  
By participating in DevDoc development, you affirm:
1. I have read and understand this Constitution
2. I will comply with all architectural decisions
3. I will explain before executing
4. I will reference official documentation
5. I will maintain enterprise production standards

**Current Version:** 2.0.0  
**Architecture:** Modular API-First  
**Stack:** Next.js/TypeScript + Python/FastAPI  
**Status:** ACTIVE DEVELOPMENT  
**Compliance:** MANDATORY
