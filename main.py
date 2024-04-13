# %%
# This script converts all files in the songs directory from
# ChordPro to LaTeX and saves the result to a new file named
# > latex/songs.tex <

import os
from Converter import chordpro_to_latex

cwd = os.getcwd()
songDir = os.path.join(cwd, "songs")
sourceDir = os.path.join(cwd, "src")

# Remove old file, create dir and new file
os.makedirs(sourceDir) if not os.path.exists(sourceDir) else None

songsTex = os.path.join(sourceDir, "index.tex")

if os.path.exists(songsTex):
    os.remove(songsTex)

with open(songsTex, "w") as file:
    file.write("")

# %%
# Iterate over the files and convert them to LaTeX
# then append the result to songs.tex

# Get all files in the songs directory that end with .cho, .chopro, .chordpro, .crd, .txt, .pro
files = [
    file
    for file in os.listdir("songs")
    if file.endswith(".cho")
    or file.endswith(".chopro")
    or file.endswith(".chordpro")
    or file.endswith(".crd")
    or file.endswith(".txt")
    or file.endswith(".pro")
]

for file in files:
    with open(os.path.join(songDir, file), "r", encoding="utf-8") as file:
        input = file.read()
        output = chordpro_to_latex(input)
        with open(songsTex, "a") as file:
            file.write(output)
            file.write("\n\n")
# %%
