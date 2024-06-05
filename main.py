import os
import argparse
from Converter import chordpro_to_latex

def convert_files(songsDir, latexDir):
    os.makedirs(latexDir, exist_ok=True)

    songsTex = os.path.join(latexDir, "index.tex")

    with open(songsTex, "w") as file:
        for song_file in os.listdir(songsDir):
            if song_file.endswith(
                (".cho", ".chopro", ".chordpro", ".crd", ".txt", ".pro")
            ):
                with open(os.path.join(songsDir, song_file), "r", encoding="utf-8") as f:
                    input = f.read()
                    output = chordpro_to_latex(input)
                    file.write(output)
                    file.write("\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true", help="Run tests")
    parser.add_argument("-i", "--songs", type=str, help="Directory containing song files, default 'songs'", action="store", default="songs")
    parser.add_argument("-o", "--latex", type=str, help="Directory to write output files, default 'src'", action="store", default="src")
    args = parser.parse_args()

    if args.test:
        print("No tests defined.")
    else:
        convert_files(args.songs, args.latex)
