#!/usr/bin/env python3
import subprocess
import sys
import tomllib
import zipfile
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
ADDON_DIR = ROOT_DIR / "blentom"
BUILD_DIR = ROOT_DIR / "build"

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


def inject_manifest(BUILD_DIR: Path):
    """Reads, modifies, and overwrites the manifest at the root of staging."""
    manifest_path = BUILD_DIR / "blender_manifest.toml"
    content = manifest_path.read_text(encoding="utf-8")

    wheels = [f'"./wheels/{w.name}"' for w in (BUILD_DIR / "wheels").glob("*.whl")]
    injection = f"\nwheels = [\n    {',\n    '.join(wheels)}\n]\n\n"

    lines = content.splitlines()
    # Insert before the first table header
    insert_idx = next(
        (i for i, line in enumerate(lines) if line.strip().startswith("[")), len(lines)
    )
    lines.insert(insert_idx, injection)
    manifest_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    wheels_dir = BUILD_DIR / "wheels"
    license_dir = wheels_dir / "licenses"
    license_dir.mkdir(parents=True, exist_ok=True)

    with open(ADDON_DIR / "blender_manifest.toml", "rb") as f:
        manifest = tomllib.load(f)

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
            "-d",
            str(wheels_dir),
        ],
        check=True,
    )

    for w in (wheels_dir).glob("*.whl"):
        pkg = w.name.split("-")[0].lower()
        extract_license(pkg, w, license_dir)

    # 2. Copy source and files
    shutil.copytree(ADDON_DIR, BUILD_DIR, dirs_exist_ok=True)
    shutil.copy2(ROOT_DIR / "README.rst", BUILD_DIR)
    shutil.copy2(ROOT_DIR / "LICENSE", BUILD_DIR)
    shutil.copy2(ROOT_DIR / "ATTRIBUTIONS", BUILD_DIR)

    # 3. Patch Manifest
    inject_manifest(
        BUILD_DIR,
    )

    # 4. Zip
    zip_path = f"blentom-{manifest['version']}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in BUILD_DIR.rglob("*"):
            if f.is_file():
                z.write(f, f.relative_to(BUILD_DIR))
    shutil.rmtree(BUILD_DIR)
    print(f"Bundled: {zip_path}")


if __name__ == "__main__":
    main()
