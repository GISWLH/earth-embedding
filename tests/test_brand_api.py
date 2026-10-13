import json

import earth_embedding
import rs_embed
from rs_embed.cli import main


def test_compatibility_entrypoints_are_identical():
    for name in rs_embed.__all__:
        assert getattr(earth_embedding, name) is getattr(rs_embed, name)


def test_cli_models_and_describe_without_weights(capsys):
    main(["models", "--json"])
    assert json.loads(capsys.readouterr().out) == rs_embed.list_models()
    main(["describe", "satclip"])
    assert json.loads(capsys.readouterr().out)["type"] == "location"
