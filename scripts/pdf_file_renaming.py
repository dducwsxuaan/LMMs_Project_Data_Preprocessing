import os

folder = "data/raw"

files = sorted(
    [f for f in os.listdir(folder) if f.endswith(".pdf")],
    key=lambda x: int(x.split("---")[0])
)

for i, filename in enumerate(files, start=1):
    new_name = f"case{i}.pdf"
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)
    print(f"Renamed {filename} -> {new_name}")

print("✅ Renaming complete!")