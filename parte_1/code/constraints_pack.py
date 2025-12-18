def no_three_horizontal(l, c, r):
    """Constraint: Cannot have 3 horizontal in a row"""
    return not(l and c and r)

def no_three_vertical(u, c, d):
    """Constraint: Cannot have 3 vertical in a row"""
    return not(u and c and d)
        
def same_cell_const(x, o):
    """Constraint: A cell cannot be both X and O"""
    return bool((not(x) and o) or (x and not(o)))