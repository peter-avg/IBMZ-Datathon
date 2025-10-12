from dotenv import load_dotenv
from pathlib import Path
from os import getenv


class TestEnvVariables:
    """Tests to ensure environment variables are properly loaded from agent/.env"""

    @classmethod
    def setup_class(cls):
        """Load environment variables before running tests"""
        # test file: tests/agent/test_env_vars.py
        # .env file: agent/.env
        base_dir = Path(__file__).resolve().parent.parent.parent  # .../IBM-Z/
        cls.dotenv_path = base_dir / "agent" / ".env"

        # Load .env
        load_dotenv(dotenv_path=cls.dotenv_path)

        cls.openai_key = getenv("OPENAI_API_KEY")
        cls.gemini_key = getenv("GOOGLE_API_KEY")

    def test_env_file_exists(self):
        """Check that the .env file exists"""
        assert self.dotenv_path.exists(), f".env file not found at {self.dotenv_path}"

    def test_openai_api_key_loaded(self):
        """Ensure OPENAI_API_KEY is present and looks valid"""
        assert self.openai_key, "OPENAI_API_KEY not loaded or empty"
        assert self.openai_key.startswith("sk-"), "OPENAI_API_KEY format looks invalid"

    def test_google_api_key_loaded(self):
        """Ensure GOOGLE_API_KEY is present"""
        assert self.gemini_key, "GOOGLE_API_KEY not loaded or empty"
        assert len(self.gemini_key) > 20, "GOOGLE_API_KEY seems too short"

    def test_keys_are_not_identical(self):
        """Sanity check that both keys are different"""
        assert self.openai_key != self.gemini_key, "OPENAI_API_KEY and GOOGLE_API_KEY should not be the same"
