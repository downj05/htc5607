from tables import *

programmes = [Programme(tuple) for tuple in get_all_rows('PROGRAMME')]

