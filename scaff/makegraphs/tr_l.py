t = dict()
with open("lenses_recoded.td") as f:
    for line in f:
        for w in line.split():
            if w not in t:
                t[w] = input(w + '? ')
with open("lenses_recoded.td") as f:
    with open("lenshort.td", 'w') as g:
        for line in f:
            out = ' '.join(t[w] for w in line.split())
            print(out, file = g)
