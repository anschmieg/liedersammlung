import os
import argparse
import unittest
from Converter import chordpro_to_latex


class TestChordproToLatex(unittest.TestCase):
    def test_basic_conversion(self):
        chordpro_input = "{title:Test Song}\n{key:C}\n[C]This is a [G]test song"
        expected_output = "\\begin{songWithKeys}[key=C]{Test Song}\n\\Ch{C}This is a \\Ch{G}test song\n\\end{songWithKeys}"
        self.assertEqual(chordpro_to_latex(chordpro_input), expected_output)

    def test_unknown_directive(self):
        chordpro_input = "{unknown:Test}\n[C]This is a [G]test song"
        expected_output = (
            "unknown:Test\n\\Ch{C}This is a \\Ch{G}test song\n\\end{songWithKeys}"
        )
        self.assertEqual(chordpro_to_latex(chordpro_input), expected_output)


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChordproToLatex)
    unittest.TextTestRunner().run(suite)


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
        run_tests()
    else:
        convert_files(args.songs, args.latex)
