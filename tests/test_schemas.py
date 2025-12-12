import unittest
from datetime import datetime
from pydantic import ValidationError
from src.devdoc_contracts.schemas import RAGIndexRequest, GitMetadata

class TestRAGIndexContracts(unittest.TestCase):
    def setUp(self):
        self.valid_payload = {
            "content": "function login() { ... }",
            "metadata": {
                "id": "entry_123",
                "source": "code_file",
                "project_id": "proj_abc",
                "created_at": datetime.now().isoformat(),
                "author_id": "user_1",
                "repo_url": "https://github.com/org/repo",
                "git_commit_hash": "a1b2c3d",
                "git_branch": "main"
            }
        }

    def test_valid_rag_request(self):
        """Ensure a valid payload passes Pydantic validation."""
        request = RAGIndexRequest(**self.valid_payload)
        self.assertEqual(request.content, "function login() { ... }")
        self.assertEqual(request.metadata.git_commit_hash, "a1b2c3d")

    def test_missing_required_field(self):
        """Ensure missing git_commit_hash raises an error."""
        invalid_payload = self.valid_payload.copy()
        # Remove a required field from metadata
        del invalid_payload["metadata"]["git_commit_hash"]
        
        with self.assertRaises(ValidationError):
            RAGIndexRequest(**invalid_payload)

    def test_invalid_source_enum(self):
        """Ensure invalid source type raises an error."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["metadata"]["source"] = "invalid_source_type"
        
        with self.assertRaises(ValidationError):
            RAGIndexRequest(**invalid_payload)

if __name__ == "__main__":
    unittest.main()
