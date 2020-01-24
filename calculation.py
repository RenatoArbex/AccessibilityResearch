'''
Run accessibility calculations.

'''

import accessibility as ac

#Parameters
graph_name = 'region'
maximum_walkin_distance = 2000
gravity_alfa = 0.355
gravity_beta = 0.029

#Calculates main accessibility indicators
mt, access = ac.accessibility_calculation(graph_name, maximum_walkin_distance,
                                          gravity_alfa,gravity_beta)

#Calculates population weighted average accessibility by areas
waverage = ac.population_weighted_average_and_comparisons(graph_name, access)


