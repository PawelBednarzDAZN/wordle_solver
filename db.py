def fetch(filepath):
    return map(lambda s: unicode(s.strip(), 'utf-8'), open(filepath).readlines())

