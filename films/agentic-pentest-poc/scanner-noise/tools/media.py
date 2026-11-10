"""Immutable provider originals + manifest (playbook §5.2).

Provider bytes are written to media/original/<kind>/<id>.<take>.<ext> BEFORE any processing,
never overwritten (a new generation becomes a new take), and hashed into media/manifest.json.
Derived files (media/derived/...) are rebuilt from originals by tools/derive.py."""
import hashlib, json, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent.parent
MF = HERE / "media" / "manifest.json"

def load():
    return json.loads(MF.read_text()) if MF.exists() else {"originals": {}, "selected": {}, "derivations": {}}

def save(m):
    MF.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")

def next_take(kind, item_id, ext):
    d = HERE / "media" / "original" / kind; d.mkdir(parents=True, exist_ok=True)
    n = 1
    while (d / f"{item_id}.t{n}.{ext}").exists(): n += 1
    return d / f"{item_id}.t{n}.{ext}", f"t{n}"

def write_original(kind, item_id, ext, data: bytes, meta: dict, select=True):
    path, take = next_take(kind, item_id, ext)
    with open(path, "xb") as fh:          # 'x' = fail rather than overwrite
        fh.write(data)
    m = load()
    key = f"{kind}/{item_id}.{take}"
    m["originals"][key] = {"path": str(path.relative_to(HERE)), "sha256": hashlib.sha256(data).hexdigest(),
                           "bytes": len(data), "saved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **meta}
    if select: m["selected"][f"{kind}/{item_id}"] = take
    save(m)
    return path, take

def selected_path(kind, item_id):
    m = load(); take = m["selected"].get(f"{kind}/{item_id}")
    if not take: raise SystemExit(f"no selected take for {kind}/{item_id}")
    return HERE / m["originals"][f"{kind}/{item_id}.{take}"]["path"]
