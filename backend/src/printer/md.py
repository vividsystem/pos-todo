from printer.options import TextOptions
# Capabilities (see https://docs.slack.dev/reference/block-kit/blocks/markdown-block/)
# 4. Links ([text](href))
# 8. Block quote (> and \n)
# 10. HL (---)
# 11. Task Lists (- [ ] and \n)
# 12. Tables
# | Col 1 | Col 2 |
# | ----- | ----- |
# | A      | B      |
# 13. Images (![logo](href))
# this can be escaped: (\`*_()[]{}#+-.!%)


SLACK_DELIM_MAP = {
    "```": "code-multiline",
    "***": "bolditalic",
    "__": "bold",
    "**": "bold",
    # "~~": "strikethrough",
    "*": "italic",
    "_": "italic",
    "`": "code-inline",
}


NO_NEST = ["code-inline", "code-multiline", "italic"]
INLINE_DELIMS = sorted(SLACK_DELIM_MAP.keys(), key=len, reverse=True)

SLACK_NL_START_DELIM_MAP = {">": "blockquote", "# ": "header1"}
NL_DELIMS = SLACK_NL_START_DELIM_MAP.keys()

PRINTER_DELIM_MAP = {
    "bold": [TextOptions(bold=True), TextOptions(bold=False)],
    "italic": [TextOptions(font="b"), TextOptions(font="a")],
    "bolditalic": [TextOptions(bold=True, font="b"), TextOptions(bold=False, font="a")],
    "code-inline": [TextOptions(invertColors=True), TextOptions(invertColors=False)],
    "code-multiline": [TextOptions(invertColors=True), TextOptions(invertColors=False)],
    "header1": [
        TextOptions(underlineType=1, bold=True),
        TextOptions(underlineType=0, bold=False),
    ],
    # TODO: blockquote
}


# return queue
def convert_markdown(text_md: str):
    unterminated_delims = []
    exec: list[TextOptions | str] = []
    for line in text_md.split("\n"):
        n = 0

        # case: not in no-further-format block check for NL_DELIMS
        if (
            len(unterminated_delims) == 0
            or SLACK_DELIM_MAP[unterminated_delims[-1]] not in NO_NEST
        ):
            for delim in NL_DELIMS:
                if line.startswith(delim):
                    unterminated_delims.append(delim)
                    exec.append(PRINTER_DELIM_MAP[SLACK_NL_START_DELIM_MAP[delim]][0])
                    n += len(delim)
                    break

        text = ""
        i = n
        while i < len(line):
            subt = line[i:]

            if (
                len(unterminated_delims) != 0
                and unterminated_delims[-1] in SLACK_DELIM_MAP
                and SLACK_DELIM_MAP[unterminated_delims[-1]] in NO_NEST
            ):
                if subt.startswith(unterminated_delims[-1]):
                    delim = unterminated_delims.pop()
                    exec.append(PRINTER_DELIM_MAP[SLACK_DELIM_MAP[delim]][1])
                    i += len(delim)
                else:
                    text += line[i]
                    i += 1
                continue

            for delim in INLINE_DELIMS:
                if subt.startswith(delim):
                    if len(text) != 0:
                        exec.append(text)
                        text = ""
                    if (
                        len(unterminated_delims) != 0
                        and delim == unterminated_delims[-1]
                    ):
                        unterminated_delims.pop()
                        exec.append(PRINTER_DELIM_MAP[SLACK_DELIM_MAP[delim]][1])
                    else:
                        unterminated_delims.append(delim)
                        exec.append(PRINTER_DELIM_MAP[SLACK_DELIM_MAP[delim]][0])
                    i += len(delim)
                    break
            else:
                text += line[i]
                i += 1
        if len(text) != 0:
            exec.append(text)
            text = ""
        while len(unterminated_delims) != 0 and unterminated_delims[-1] in NL_DELIMS:
            delim = unterminated_delims.pop()
            exec.append(PRINTER_DELIM_MAP[SLACK_NL_START_DELIM_MAP[delim]][1])
        exec.append("\n")
    return exec


if __name__ == "__main__":
    with open("../../TEST.md", "rt") as f:
        bt = f.read()

        print(convert_markdown(bt))
