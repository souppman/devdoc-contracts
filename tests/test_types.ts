import { RAGIndexRequest, JournalEntryWithGitContext } from '../src/types';

// This file is primarily a "compile-time" test. 
// If it compiles, the interfaces are working as expected.

const validRequest: RAGIndexRequest = {
    content: "This is a journal entry about the auth system.",
    metadata: {
        id: "journal_1",
        source: "journal",
        project_id: "proj_1",
        created_at: "2023-01-01T00:00:00Z",
        author_id: "ryan",
        git_commit_hash: "8201293",
        git_branch: "feature/auth",
        repo_url: "https://github.com/dev/doc",
        file_path: "src/auth.ts"
    }
};

console.log("TypeScript Contract Test: RAGIndexRequest is valid.");

const validJournal: JournalEntryWithGitContext = {
    id: "j1",
    content: "Refactoring the login flow",
    created_at: "2023-01-01T00:00:00Z",
    updated_at: "2023-01-01T00:00:00Z",
    author_id: "ryan",
    project_id: "p1",
    git_context: {
        git_commit_hash: "abc1234",
        git_branch: "dev",
        author_id: "ryan",
        repo_url: "http://git"
    }
};

console.log("TypeScript Contract Test: JournalEntryWithGitContext is valid.");
