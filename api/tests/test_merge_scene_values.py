"""Tests for folding duplicate scenes' metadata into the kept scene."""

from stash_client_unified import merged_scene_values


def test_dest_wins_and_sources_fill_gaps():
    dest = {
        "title": "Kept", "date": None, "organized": False, "urls": ["u1"],
        "studio": None, "performers": [{"id": "p1"}], "tags": [{"id": "t1"}],
        "galleries": [], "groups": [],
        "stash_ids": [{"endpoint": "sdb", "stash_id": "A"}],
    }
    src = {
        "title": "Dropped", "date": "2024-01-02", "organized": True, "urls": ["u1", "u2"],
        "studio": {"id": "s9"}, "performers": [{"id": "p1"}, {"id": "p2"}],
        "tags": [{"id": "t2"}], "galleries": [{"id": "g1"}],
        "groups": [{"group": {"id": "m1"}, "scene_index": 3}],
        "stash_ids": [{"endpoint": "sdb", "stash_id": "B"}, {"endpoint": "pdb", "stash_id": "C"}],
    }

    v = merged_scene_values(dest, [src])

    assert v["title"] == "Kept"
    assert v["date"] == "2024-01-02"
    assert v["studio_id"] == "s9"
    assert v["organized"] is True
    assert v["urls"] == ["u1", "u2"]
    assert v["performer_ids"] == ["p1", "p2"]
    assert v["tag_ids"] == ["t1", "t2"]
    assert v["gallery_ids"] == ["g1"]
    assert v["groups"] == [{"group_id": "m1", "scene_index": 3}]
    assert v["stash_ids"] == [
        {"endpoint": "sdb", "stash_id": "A"},
        {"endpoint": "pdb", "stash_id": "C"},
    ]
    assert "details" not in v
