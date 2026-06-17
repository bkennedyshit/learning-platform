"""Imports drill scripts by path and runs their generators."""

import importlib.util
import random
import sys
from pathlib import Path
from types import ModuleType


_module_cache: dict[str, ModuleType] = {}


def _load_script(script_path: Path) -> ModuleType:
    key = str(script_path)
    if key in _module_cache:
        return _module_cache[key]
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load spec for {script_path}")
    module = importlib.util.module_from_spec(spec)
    # Prevent the script's if __name__ == "__main__" from running
    module.__name__ = script_path.stem
    sys.modules[script_path.stem] = module
    spec.loader.exec_module(module)
    _module_cache[key] = module
    return module


def run_drill(script_path: Path, count: int, seed: int | None) -> dict:
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
    module = _load_script(script_path)
    rng = random.Random(seed)
    problems = module.build_problem_set(count, rng)
    markdown = module.render_markdown(problems, seed)
    return {"seed": seed, "markdown": markdown}
