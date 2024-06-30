import os
import argparse
from Converter import chordpro_to_latex

def convert_files(songsDir, latexDir, verbose):
    os.makedirs(latexDir, exist_ok=True)
    if verbose:
        print(f"* Converter: Creating or using existing directory: {latexDir}")

    songsTex = os.path.join(latexDir, "index.tex")

    with open(songsTex, "w") as file:
        for song_file in os.listdir(songsDir):
            if song_file.endswith(
                (".cho", ".chopro", ".chordpro", ".crd", ".txt", ".pro")
            ):
                if verbose:
                    print(f"* Converter: Converting file: {song_file}")
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
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    if args.test:
        print("* Converter: No tests defined.")
    else:
        convert_files(args.songs, args.latex, args.verbose)