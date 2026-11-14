"""Minimal LTspice .raw (binary, transient) reader -> dict of numpy arrays."""
import numpy as np

def read_raw(path):
    b = open(path, "rb").read()
    # header is UTF-16LE text (new LTspice) or ASCII (old); find "Binary:"
    for enc, marker in (("utf-16-le", "Binary:\n".encode("utf-16-le")), ("ascii", b"Binary:\n")):
        i = b.find(marker)
        if i >= 0:
            break
    else:
        raise ValueError("not a binary raw file")
    head = b[:i].decode(enc)
    data = b[i + len(marker):]
    lines = head.splitlines()
    npts = int(next(l for l in lines if l.startswith("No. Points:")).split(":")[1])
    nvar = int(next(l for l in lines if l.startswith("No. Variables:")).split(":")[1])
    k = lines.index("Variables:")
    names = [lines[k + 1 + j].split("\t")[2] for j in range(nvar)]
    flags = next(l for l in lines if l.startswith("Flags:"))
    dbl = "double" in flags
    rec = 8 + 4 * (nvar - 1) if not dbl else 8 * nvar
    arr = np.frombuffer(data[:npts * rec], dtype=np.uint8).reshape(npts, rec)
    out = {names[0]: np.ascontiguousarray(arr[:, :8]).view("<f8").ravel()}
    for j, n in enumerate(names[1:]):
        if dbl:
            out[n] = np.ascontiguousarray(arr[:, 8 * (j + 1):8 * (j + 2)]).view("<f8").ravel()
        else:
            out[n] = np.ascontiguousarray(arr[:, 8 + 4 * j:12 + 4 * j]).view("<f4").ravel().astype(float)
    out["time"] = np.abs(out[names[0]])  # LTspice marks some time points negative
    return out
