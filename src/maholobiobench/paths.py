"""Path helpers for the standalone MaholoBioBench repository."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"
DOCS_DIR = PROJECT_ROOT / "docs"

TASK_REGISTRY = CONFIG_DIR / "task_registry.yaml"
PROTOCOL_STATE_SCHEMA = CONFIG_DIR / "protocol_state_schema.yaml"
EPISODE_OUTPUT_SCHEMA = CONFIG_DIR / "episode_output_schema.yaml"

