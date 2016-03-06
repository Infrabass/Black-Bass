
vars = {}
vars['Server'] = None
vars['Midi'] = None

# Enregistre une reference dans le dictionnaire.
def set(key, obj):
    vars[key] = obj
    
# Recupere une reference dans le dictionnaire.
def get(key):
    return vars.get(key, None)