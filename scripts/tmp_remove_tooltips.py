import pathlib
root = pathlib.Path(r'C:\Users\Anthony\OneDrive\Modding\StarfieldBlenderExtension\scripts\starfield_blender_extension\ui')
changed = []
for path in root.glob('*.py'):
    text = path.read_text(encoding='utf-8')
    new = ''
    i = 0
    while True:
        idx = text.find('tooltip=', i)
        if idx == -1:
            new += text[i:]
            break
        new += text[i:idx]
        j = idx + len('tooltip=')
        if j >= len(text):
            break
        quote = text[j]
        if quote not in ('"', "'"):
            new += 'tooltip='
            i = j
            continue
        j += 1
        while j < len(text):
            if text[j] == quote and text[j-1] != '\\':
                j += 1
                break
            j += 1
        while j < len(text) and text[j] in ' \t':
            j += 1
        if j < len(text) and text[j] == ',':
            j += 1
        i = j
    if new != text:
        path.write_text(new, encoding='utf-8')
        changed.append(str(path))
print('changed files:', changed)
