from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MANIFEST_RELATIVE_PATH = Path(".agents/python-coding-agent/agent.json")
DEFAULT_ROUTE_KEY = "default"


@dataclass(frozen=True)
class ManifestEntry:
    id: str
    path: str


@dataclass(frozen=True)
class RouteSelection:
    agents: tuple[str, ...]
    skills: tuple[str, ...]
    agent_paths: tuple[str, ...]
    skill_paths: tuple[str, ...]
    quality_gates: tuple[str, ...]
    rationale: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "agents": list(self.agents),
            "skills": list(self.skills),
            "agent_paths": list(self.agent_paths),
            "skill_paths": list(self.skill_paths),
            "quality_gates": list(self.quality_gates),
            "rationale": list(self.rationale),
            "warnings": list(self.warnings),
        }


def find_agent_root(start: Path) -> Path:
    base = start.resolve()
    if base.is_file():
        base = base.parent
    for candidate in (base, *base.parents):
        if (candidate / MANIFEST_RELATIVE_PATH).is_file():
            return candidate
    return base


def load_agent_manifest(root: Path) -> dict[str, object]:
    manifest_path = find_agent_root(root) / MANIFEST_RELATIVE_PATH
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Agent manifest must contain a JSON object.")
    return data


def manifest_entries(manifest: dict[str, object], key: str) -> tuple[ManifestEntry, ...]:
    entries: list[ManifestEntry] = []
    raw_items = manifest.get(key, [])
    if not isinstance(raw_items, list):
        return ()
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        item_path = item.get("path", "")
        if isinstance(item_id, str):
            entries.append(ManifestEntry(item_id, item_path if isinstance(item_path, str) else ""))
    return tuple(entries)


def manifest_ids(manifest: dict[str, object], key: str) -> frozenset[str]:
    return frozenset(entry.id for entry in manifest_entries(manifest, key))


def manifest_paths_for(
    manifest: dict[str, object],
    key: str,
    ids: tuple[str, ...],
) -> tuple[str, ...]:
    path_by_id = {entry.id: entry.path for entry in manifest_entries(manifest, key)}
    return tuple(path_by_id[item_id] for item_id in ids if item_id in path_by_id)


def route_task(
    task_type: str,
    manifest: dict[str, object],
    *,
    requested_agents: tuple[str, ...] = (),
    requested_skills: tuple[str, ...] = (),
    requested_quality_gates: tuple[str, ...] = (),
) -> RouteSelection:
    routes = route_matrix(manifest)
    route_config = routes.get(task_type) or routes.get(DEFAULT_ROUTE_KEY) or {}
    agents = dedupe((*route_items(route_config, "agents"), *requested_agents))
    skills = dedupe((*route_items(route_config, "skills"), *requested_skills))
    quality_gates = dedupe(requested_quality_gates or route_items(route_config, "quality_gates"))
    rationale = route_items(route_config, "rationale")
    if not rationale:
        rationale = (f"Route selected for task type: {task_type}",)
    warnings = validate_route_links(agents, skills, manifest)
    return RouteSelection(
        agents,
        skills,
        manifest_paths_for(manifest, "roles", agents),
        manifest_paths_for(manifest, "skills", skills),
        quality_gates,
        rationale,
        warnings,
    )


def route_matrix(manifest: dict[str, object]) -> dict[str, dict[str, Any]]:
    raw_routes = manifest.get("agent_routes", {})
    if not isinstance(raw_routes, dict):
        return {}
    routes: dict[str, dict[str, Any]] = {}
    for key, value in raw_routes.items():
        if isinstance(key, str) and isinstance(value, dict):
            routes[key] = value
    return routes


def route_items(route_config: dict[str, Any], key: str) -> tuple[str, ...]:
    value = route_config.get(key, [])
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def validate_route_links(
    agents: tuple[str, ...],
    skills: tuple[str, ...],
    manifest: dict[str, object],
) -> tuple[str, ...]:
    role_ids = manifest_ids(manifest, "roles")
    skill_ids = manifest_ids(manifest, "skills")
    warnings = [
        f"unknown agent role: {agent_id}" for agent_id in agents if agent_id not in role_ids
    ]
    warnings.extend(
        f"unknown skill: {skill_id}" for skill_id in skills if skill_id not in skill_ids
    )
    return tuple(warnings)


def dedupe(items: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return tuple(result)
