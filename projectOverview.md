




Core Concept & Value Proposition
DevDoc automates developer documentation by intelligently merging two information streams: your **codebase** and your **development journal**. Unlike generic documentation generators, it uses structured journal notes attached to specific commits and branches as guided prompts for an AI, ensuring the generated documentation is accurate, context rich, and directly relevant to the developer's actual work and intent.

System Architecture
The system is built as a set of independent, modular services that communicate via strict API contracts. This design isolates complexity, making the system testable, scalable, and easier to maintain.

*   **Next.js Frontend:** The user interface for writing journal entries and browsing documentation.
*   **Backend-for-Frontend (BFF):** A dedicated Next.js API layer that orchestrates all frontend requests, aggregating data from the backend services.
*   **Journal & Git Service (TypeScript/Node.js):** The "context weaver." It manages journal entries, captures Git metadata, and links notes to commits, branches, and tickets.
*   **RAG & AI Service (Python/FastAPI):** The "brain." It indexes code and journal text into vectors, retrieves relevant context, and uses LLMs to generate non-generic documentation. Built in **Python** to leverage the superior LlamaIndex and AI ecosystem.
*   **External Services:** GitHub (webhooks), Supabase (primary database & auth), Pinecone (vector storage for embeddings), OpenAI/Claude (LLMs), and S3 (for doc exports).

Critical API Contracts (The Glue)
The success of the modular design hinges on these defined data exchanges:

1.  **Journal → AI Service (Indexing):** The `Journal Service` sends a `RAGIndexRequest` to the AI service whenever new content is created. This request packages the **text content** with critical **metadata** (like `git_commit_hash`, `file_path`, `author_id`), solving the "wiring" problem at the source.
2.  **BFF → AI Service (Query/Generation):** The BFF sends a `RAGQueryRequest` with a user's question and filters. The AI service uses Retrieval-Augmented Generation (RAG) to fetch the most relevant code and journal snippets from Pinecone and instructs an LLM to synthesize an answer or document.
3.  **Frontend/BFF → Journal Service (CRUD):** The frontend creates journal entries with automatically captured `git_context`, ensuring every note is intrinsically linked to a specific state of the code.

Implementation Roadmap

*   **Phase 1: Foundation (Weeks 1-2)**
    *   Set up repositories and define shared API TypeScript/Python interfaces.
    *   Scaffold the **Python RAG & AI Service** with FastAPI, LlamaIndex, and mock endpoints.

*   **Phase 2: Core AI & Journal (Weeks 3-5)**
    *   Build the RAG service's indexing and query pipelines with Pinecone.
    *   Develop the **TypeScript Journal & Git Service** to handle journal CRUD and GitHub webhooks.
    *   Connect the services: Ensure a new journal entry triggers an index request to the RAG service.

*   **Phase 3: Integration & UI (Weeks 6-8)**
    *   Build the **Next.js BFF** routes to orchestrate data flow for key user stories.
    *   Develop the main React frontend with the integrated Markdown editor.
    *   Implement staleness checks (via webhooks) and export features.

How This Plan Solves the Core Challenges

*   **Avoiding a "Mess" of Wiring:** Git context is attached by the **Journal Service** when an entry is created and embedded as metadata in the **RAG Index**. This creates a single, authoritative link.
*   **Preventing Generic AI Docs:** The AI is fed precise, retrieved context (specific code + relevant journal notes) via the **RAG pipeline**, moving it far beyond generic boilerplate generation.
*   **Keeping Docs Fresh:** The **Git webhook pipeline** automatically triggers staleness analysis and can re-generate or flag documentation when the underlying code changes.

**Your next immediate action is to create the shared `devdoc-interfaces` repository containing the formal definitions for `RAGIndexRequest` and `JournalEntryWithGitContext`. This will lock in the contracts that enable all subsequent parallel development.**


