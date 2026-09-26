"""
JSON Utilities
===============
Safely parses JSON responses from LLMs, handling markdown code fences,
surrounding prose, and partial JSON structures defensively.
"""

import json
import re
from typing import Any, Dict, List, Optional


def safe_json_parse(raw: str, fallback: Optional[Any] = None) -> Any:
    """
    Defensively parse JSON from LLM output.
    Handles ```json ... ``` blocks, bare JSON, and extracts JSON objects/arrays
    even if surrounded by conversational filler.
    """
    if not raw or not isinstance(raw, str):
        return fallback if fallback is not None else {}

    cleaned = raw.strip()

    # 1. Check for markdown code fences (```json ... ``` or ``` ...)
    fence_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    fence_match = re.search(fence_pattern, cleaned, re.IGNORECASE)
    if fence_match:
        fence_content = fence_match.group(1).strip()
        try:
            return json.loads(fence_content)
        except json.JSONDecodeError:
            pass

    # 2. Try direct json.loads
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 3. Find the outermost JSON object {...}
    obj_match = re.search(r"(\{[\s\S]*\})", cleaned)
    if obj_match:
        try:
            return json.loads(obj_match.group(1))
        except json.JSONDecodeError:
            pass

    # 4. Find the outermost JSON array [...]
    arr_match = re.search(r"(\[[\s\S]*\])", cleaned)
    if arr_match:
        try:
            return json.loads(arr_match.group(1))
        except json.JSONDecodeError:
            pass

    return fallback if fallback is not None else {}
