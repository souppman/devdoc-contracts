from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class GitMetadata(BaseModel):
    git_commit_hash: str
    git_branch: str
    file_path: Optional[str] = None
    author_id: str
    repo_url: str

class RAGIndexMetadata(GitMetadata):
    id: str
    source: Literal['journal', 'code_file', 'commit_message']
    project_id: str
    created_at: datetime
    linked_jira_issue: Optional[str] = None

class RAGIndexRequest(BaseModel):
    content: str
    metadata: RAGIndexMetadata

class JournalEntryWithGitContext(BaseModel):
    id: str
    content: str
    created_at: datetime
    updated_at: datetime
    author_id: str
    project_id: str
    git_context: GitMetadata
    linked_issues: Optional[List[str]] = None
    tags: Optional[List[str]] = None

# BFF Types needed for reference or if Python BFF implementation is ever needed (unlikely per arch, but good for parity)
class ProjectMeta(BaseModel):
    id: str
    name: str
    repo_url: str
    last_indexed_at: datetime

class GitCommit(BaseModel):
    hash: str
    message: str
    author: str
    date: datetime

class DocSection(BaseModel):
    id: str
    title: str
    content: str
    relevance_score: Optional[float] = None

class BFFProjectDashboardResponse(BaseModel):
    project: ProjectMeta
    recent_commits: List[GitCommit]
    journal_entries: List[JournalEntryWithGitContext]
    documentation: List[DocSection]

class BFFProjectDashboardRequest(BaseModel):
    project_id: str
    user_id: str
