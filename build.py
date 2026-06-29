#!/usr/bin/env python3
import subprocess
import sys
import tomllib
import zipfile
import shutil
from pathlib import Path

PLATFORMS = {"macos-arm64": "macosx_14_0_arm64"}

ROOT_DIR = Path(__file__).parent.resolve()
ADDON_DIR = ROOT_DIR / "blentom"
BUILD_DIR = ROOT_DIR / "build"
BLENDER_PROVIDED = {
    "numpy",
    "pyopenvdb",
    "requests",
    "certifi",
    "charset-normalizer",
    "idna",
    "urllib3",
}


def extract_license(pkg_name: str, wheels_file: Path, license_dir: Path):
    with zipfile.ZipFile(wheels_file, "r") as z:
        dist_infos = [f for f in z.namelist() if ".dist-info" in f]
        if not dist_infos:
            return
        dist_info = dist_infos[0].split("/")[0]
        for lf in [
            f
            for f in z.namelist()
            if f.startswith(dist_info)
            and ("LICENSE" in f or "METADATA" in f or "COPYING" in f)
        ]:
            (license_dir / f"{pkg_name}_{Path(lf).name}").write_bytes(z.read(lf))


def inject_manifest(staging_dir: Path, platform: str):
    """Reads, modifies, and overwrites the manifest at the root of staging."""
    manifest_path = staging_dir / "blender_manifest.toml"
    content = manifest_path.read_text(encoding="utf-8")

    wheels = [f'"./wheels/{w.name}"' for w in (staging_dir / "wheels").glob("*.whl")]
    injection = (
        f'\nplatforms = ["{platform}"]\nwheels = [\n    {",\n    ".join(wheels)}\n]\n\n'
    )

    lines = content.splitlines()
    # Insert before the first table header
    insert_idx = next(
        (i for i, line in enumerate(lines) if line.strip().startswith("[")), len(lines)
    )
    lines.insert(insert_idx, injection)
    manifest_path.write_text("\n".join(lines), encoding="utf-8")


def build_for_platform(platform: str, pip_tag: str, manifest: dict):
    staging_dir = BUILD_DIR / platform
    wheels_dir = staging_dir / "wheels"
    license_dir = staging_dir / "wheels" / "licenses"
    staging_dir.mkdir(parents=True, exist_ok=True)
    wheels_dir.mkdir(parents=True, exist_ok=True)
    license_dir.mkdir(parents=True, exist_ok=True)

    # 1. Download and Filter
    py_ver = str(manifest.get("build", {}).get("python_version")).replace(".", "")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--no-cache-dir",
            "-r",
            str(ROOT_DIR / "requirements.txt"),
            "--only-binary",
            ":all:",
            "--python-version",
            py_ver[:3],
            "--implementation",
            "cp",
            "--abi",
            f"cp{py_ver}",
            "--platform",
            pip_tag,
            "-d",
            str(staging_dir / "wheels"),
        ],
        check=True,
    )

    for w in (staging_dir / "wheels").glob("*.whl"):
        pkg = w.name.split("-")[0].lower()
        if pkg in BLENDER_PROVIDED:
            w.unlink()
        else:
            extract_license(pkg, w, staging_dir / "wheels" / "licenses")

    # 2. Copy source and files
    shutil.copytree(ADDON_DIR, staging_dir, dirs_exist_ok=True)
    shutil.copy2(ROOT_DIR / "README.rst", staging_dir)
    shutil.copy2(ROOT_DIR / "LICENSE", staging_dir)

    # 3. Patch Manifest
    inject_manifest(staging_dir, platform)

    # 4. Zip
    zip_path = BUILD_DIR / f"blentom-{manifest['version']}-{platform}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in staging_dir.rglob("*"):
            if f.is_file():
                z.write(f, f.relative_to(staging_dir))
    shutil.rmtree(staging_dir)
    print(f"Bundled: {zip_path.name}")


def main():
    with open(ADDON_DIR / "blender_manifest.toml", "rb") as f:
        manifest = tomllib.load(f)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    for p, tag in PLATFORMS.items():
        build_for_platform(p, tag, manifest)


if __name__ == "__main__":
    main()
