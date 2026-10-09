"""delete_scene_files must promote the keeper before deleting."""

import asyncio
from unittest.mock import AsyncMock

from stash_client_unified import StashClientUnified


def test_keeper_promoted_before_delete_regardless_of_file_order():
    client = StashClientUnified.__new__(StashClientUnified)
    calls = []
    client.set_scene_primary_file = AsyncMock(side_effect=lambda *a: calls.append(("primary", a)))
    client.delete_files = AsyncMock(side_effect=lambda ids: calls.append(("delete", ids)) or True)

    # Keeper listed first, as the duplicate_scene_files analyzer orders them.
    asyncio.run(client.delete_scene_files("7", ["2"], "1", ["1", "2"]))

    assert calls == [("primary", ("7", "1")), ("delete", ["2"])]
