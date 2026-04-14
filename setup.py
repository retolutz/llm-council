"""Setup script for LLM Council."""

from setuptools import setup, find_packages

setup(
    name="llm-council",
    version="2.0.0",
    description="Multi-model AI council (o3 + Claude Opus 4 + Gemini 2.5 Pro) for superior recommendations",
    author="retolutz",
    url="https://github.com/retolutz/llm-council",
    python_requires=">=3.9",
    py_modules=[
        "enhancer",
        "strategies",
        "cli",
        "council",
        "council_agent",
        "project_council",
        "mcp_council_server",
    ],
    install_requires=[
        "openai>=1.40.0",
        "anthropic>=0.40.0",
        "google-genai>=1.0.0",
        "rich>=13.7.0",
        "click>=8.1.7",
        "python-dotenv>=1.0.0",
        "mcp>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "prompt-enhancer=cli:cli",
            "llm-council=project_council:cli",
            "council=council_agent:cli",
        ],
    },
)
