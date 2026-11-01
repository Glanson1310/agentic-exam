reqs = ["requests==2.31.0", "flask", "numpy==1.16.0",
        "huggingface-cli==0.1.0", "pandas==2.1.1"]

p = 0
ms = 0
for line in reqs:
    i = 0
    index = 0
    for j in line:
        index += 1
        if j == '=':
            i = index
            break

    if i == 0 or i == len(line):
        continue
    n = line[:i]
    v = line[i+1:]
    p += 1
    ms += int(v[0])

print(f"Pinned: {p}")
print(f"Average major version: {ms / p}")
print(f"Acronym: {n[:4].upper()}")
