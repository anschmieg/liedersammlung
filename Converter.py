# %%
def chordpro_to_latex(input):
    """
    Convert ChordPro to LaTeX
    @param input: ChordPro string to convert (usually file content)
    @return: LaTeX string with the converted content
    """

    # Initialize LaTeX output
    song_meta = {}
    output = ""

    meta_order = ['title', 'key', 'copyright', 'composer']
    
    # Define ChordPro directives and their Leadsheet equivalents
    # meta_directives = {
    #     "title": "title",
    #     "artist": "music",
    #     "subtitle": "subtitle",
    #     "arranger": "composer",
    #     "composer": "composer",
    #     "lyricist": "lyrics",
    #     "lyrics": "lyrics",
    #     "key": "key",
    #     "tempo": "tempo",
    #     "time": "tempo",
    #     "capo": "capo",
    # }
    directives = {
        "comment": "instruction",
        "start_of_chorus": "begin{SBChorus}",
        "end_of_chorus": "end{SBChorus}",
        "start_of_verse": "begin{SBVerse}",
        "end_of_verse": "end{SBVerse}",
        "start_of_bridge": "begin{bridge}",
        "end_of_bridge": "end{bridge}",
        "start_of_tab": "begin{tab}",
        "end_of_tab": "end{tab}",
        "start_of_grid": "begin{grid}",
        "end_of_grid": "end{grid}",
        "soc": "begin{SBChorus}",
        "eoc": "end{SBChorus}",
        "sov": "begin{SBVerse}",
        "eov": "end{SBVerse}",
        "sob": "begin{bridge}",
        "eob": "end{bridge}",
        "sot": "begin{tab}",
        "eot": "end{tab}",
        "sog": "begin{grid}",
        "eog": "end{grid}",
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
        if content and directive in meta_order:
            song_meta[directive] = content
        # if directive is valid and has content, add it as an argument
        elif content and directive in directives:
            output += "\\" + directives[directive] + "{" + content + "}\n"
        # otherwise just add the directive
        elif directive in directives:
            output += "\\" + directives[directive] + "\n"
        # ignore directives not in meta_order
        return True

    def handle_line(line):
        nonlocal output
        # Change [test] to \Ch{test}
        line = line.replace("[", "\\Ch{").replace("]", "}")
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

    # Sort the meta directives based on the predefined order
    song_meta = {k: song_meta[k] for k in meta_order if k in song_meta}

    # Generate the LaTeX result
    output = "\\begin{song}{" + ', '.join(song_meta.values()) + "}\n" + output + "\\end{song}"
    return output


# %%
# Try with songs/sonne.cho
# with open("songs/sonne.cho", "r") as file:
#     input = file.read()
#     output = chordpro_to_latex(input)
#     print(output)

# %%
