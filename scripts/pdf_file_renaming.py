import os

folder = "data/raw"

files = sorted(
    [f for f in os.listdir(folder) if f.endswith(".pdf")],
    key=lambda x: int(x.split("---")[0])
)

for _, _, filenames in os.walk(folder):
    for filename in filenames:
        if not filename.endswith(".pdf"):
            continue

        case_number = int(filename.split("---")[0])
        new_name = f"case{case_number}.pdf"

        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)

        os.rename(old_path, new_path)
        
        print(f"Renamed {filename} -> {new_name}")

print("✅ Renaming complete!")