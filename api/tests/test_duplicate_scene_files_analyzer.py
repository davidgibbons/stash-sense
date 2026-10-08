"""Tests for DuplicateSceneFilesAnalyzer."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _file(file_id, path):
    return {"id": file_id, "path": path, "size": 100, "duration": 60, "width": 1920, "height": 1080,
            "video_codec": "h264", "bit_rate": 5_000_000}


@pytest.mark.asyncio
async def test_quality_tie_keeps_preferred_path_and_refreshes_pending(tmp_path):
    from analyzers import duplicate_scene_files
    from analyzers.duplicate_scene_files import DuplicateSceneFilesAnalyzer
    from recommendations_db import RecommendationsDB

    rec_db = RecommendationsDB(tmp_path / "test.db")
    rec_db.create_recommendation(type="duplicate_scene_files", target_type="scene", target_id="1",
                                 details={"suggested_keeper_id": "a"})
    stash = MagicMock()
    stash.get_multi_file_scenes = AsyncMock(return_value=[
        {"id": "1", "files": [_file("a", "/adult/Organized/x.mp4"), _file("b", "/adult/Eros/x.mp4")]},
    ])

    with patch.object(duplicate_scene_files, "KEEP_PATH_PREFIX", "/adult/Eros/"):
        await DuplicateSceneFilesAnalyzer(stash, rec_db).run()

    recs = rec_db.get_recommendations(type="duplicate_scene_files", status="pending")
    assert [r.details["suggested_keeper_id"] for r in recs] == ["b"]
