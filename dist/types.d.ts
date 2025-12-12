export interface GitMetadata {
    git_commit_hash: string;
    git_branch: string;
    file_path?: string;
    author_id: string;
    repo_url: string;
}
export interface RAGIndexRequest {
    content: string;
    metadata: {
        id: string;
        source: 'journal' | 'code_file' | 'commit_message';
        project_id: string;
        created_at: string;
        linked_jira_issue?: string;
    } & GitMetadata;
}
export interface JournalEntryWithGitContext {
    id: string;
    content: string;
    created_at: string;
    updated_at: string;
    author_id: string;
    project_id: string;
    git_context: GitMetadata;
    linked_issues?: string[];
    tags?: string[];
}
export interface ProjectMeta {
    id: string;
    name: string;
    repo_url: string;
    last_indexed_at: string;
}
export interface GitCommit {
    hash: string;
    message: string;
    author: string;
    date: string;
}
export interface DocSection {
    id: string;
    title: string;
    content: string;
    relevance_score?: number;
}
export interface BFFProjectDashboardResponse {
    project: ProjectMeta;
    recent_commits: GitCommit[];
    journal_entries: JournalEntryWithGitContext[];
    documentation: DocSection[];
}
export interface BFFProjectDashboardRequest {
    project_id: string;
    user_id: string;
}
