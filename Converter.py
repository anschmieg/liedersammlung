#%%
def chordpro_to_latex(input):
    """
    Convert ChordPro to LaTeX
    @param input: ChordPro string to convert (usually file content)
    @return: LaTeX string with the converted content
    """

    # Initialize LaTeX output
    song_meta = {}
    output = ""

    # Define ChordPro directives and their LaTeX equivalents
    meta_directives = {
        "title": "title",
        "artist": "music",
        "subtitle": "subtitle",
        "arranger": "music",
        "composer": "music",
        "lyricist": "lyrics",
        "lyrics": "lyrics",
        "key": "key",
        # "tempo": "tempo",
        # "time": "tempo",
        # "capo": "capo",
    }
    directives = {
        "comment": "instruction",
        "start_of_chorus": "begin{SBChorus}",
        "end_of_chorus": "end{SBChorus}",
        "start_of_verse": "begin{SBVerse}",
        "end_of_verse": "end{SBVerse}",
        "start_of_bridge": "begin{SBBridge}",
        "end_of_bridge": "end{SBBridge}",
        "soc": "begin{SBChorus}",
        "eoc": "end{SBChorus}",
        "sov": "begin{SBVerse}",
        "eov": "end{SBVerse}",
        "sob": "begin{SBBridge}",
        "eob": "end{SBBridge}",
        "new_page": "newpage",
        "np": "newpage",
    }

    def fallback(exp):
        nonlocal output
        output += exp + "\n"
        raise UserWarning(
            "Undefined sequence: "
            + exp
            + "\nCheck if this argument is supported. Writing original line to output."
        )

    def handle_directive(directive, content=None):
        nonlocal output
        nonlocal song_meta
        # if directive is a song property, store it in the dictionary
        if content and directive in meta_directives:
            song_meta[directive] = content
        # if directive is valid and has content, add it as an argument
        elif content and directive in directives:
            output += "\\" + directives[directive] + "{" + content + "}\n"
        # otherwise just add the directive
        elif directive in directives:
            output += "\\" + directives[directive] + "\n"
        # if directive is unknown, add it as plain text
        else:
            output += directive + ":" + (content if content else "") + "\n"
            return False  # return False to indicate that the directive is unknown
        return True

    def handle_line(line):
        nonlocal output
        # Change [test] to \Ch{test}
        line = line.replace("[", "\\Ch{").replace("]", "}{}")
        output += line + "\n"
        return True

    input = input.strip()
    lines = input.split("\n")

    # Process each line
    for line in lines:
        line = line.strip(" \t")  # strip spaces, tabs and {}
        if "{" in line:
            line = line.strip("{} ")
            if ":" in line:
                # Split directive and content by ': ' or ':'
                directive, content = (
                    line.split(": ", 1) if ": " in line else line.split(":", 1)
                )
                handle_directive(directive, content)
            else:
                try:
                    # Use standalone directive
                    handle_directive(line)
                except:
                    fallback(line)
        else:
            try:
                handle_line(line)
            except:
                fallback(line)

    # Generate the LaTeX result
    # only output the \begin{songWithKeys}[]{} command if all directives are known
    if all(handle_directive(directive, content) for directive, content in song_meta.items()):
        # output the song metadata as arguments to the \begin{songWithKeys} command
        output = "\\begin{song}[" + ", ".join(f"{k}={v}" for k, v in song_meta.items() if k != "title") + "]{" + song_meta.get("title", "") + "}\n" + output + "\\end{song}"
    # otherwise output only the known directives and unknown directives as plain text
    else:
        output = "\n".join(
            f"{k}: {v}" for k, v in song_meta.items() if k != "title"
        ) + "\n" + output + "\\end{song}"

    return output





########
# Test #
# only run in interactive mode

try:
    if __IPYTHON__:
        import os
        cwd = os.getcwd()
        songDir = os.path.join(cwd, "songs")
        sourceDir = os.path.join(cwd, "src")

        os.makedirs(sourceDir, exist_ok=True)

        songsTex = os.path.join(sourceDir, "index.tex")
        with open(songsTex, "w") as file:
            for song_file in os.listdir(songDir):
                if song_file.endswith((".cho", ".chopro", ".chordpro", ".crd", ".txt", ".pro")):
                    with open(os.path.join(songDir, song_file), "r", encoding="utf-8") as f:
                        input = f.read()
                        output = chordpro_to_latex(input)
                        print(output.split("\n")[0])
                        
except NameError:
    # running from CLI
    pass
# %%
