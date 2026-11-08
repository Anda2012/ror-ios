import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from patches.verify_ipa import find_app_bundle


def test_find_app_bundle_accepts_non_ror_names():
    names = [
        "Payload/RoRNative.app/Info.plist",
        "Payload/RoRNative.app/RoRNative",
        "Payload/RoRNative.app/rorres/skeleton.zip",
    ]

    assert find_app_bundle(names) == "Payload/RoRNative.app"


def test_find_app_bundle_keeps_ror_app_default():
    names = [
        "Payload/RoR.app/Info.plist",
        "Payload/RoR.app/RoR",
        "Payload/RoR.app/rorres/skeleton.zip",
    ]

    assert find_app_bundle(names) == "Payload/RoR.app"
