
gl = {}
gl['Server'] = None
gl['Midi'] = None
gl['Glitch'] = None
gl['Scream'] = None


# Enregistre une reference dans le dictionnaire.
def set(key, obj):
    gl[key] = obj
    
# Recupere une reference dans le dictionnaire.
def get(key):
    return gl.get(key, None)