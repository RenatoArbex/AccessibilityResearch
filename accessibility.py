'''
Accessibility calculation functions.

'''


import pandas as pd
import numpy as np


def accessibility_calculation(graph_file_name, max_walk_distance, alfa, beta):

    print('** Calculating accessibility for Graph file ', graph_file_name)

    # ---------------------------------------------------------------------
    # Data input

    #Read travel time matrix between cells
    mt = pd.read_csv('data\\traveltime_matrix_' + graph_file_name + '.csv')

    #Read job and population data for cells
    jobs_pop = pd.read_csv('data\\id_jobs_pop_' + graph_file_name + '.csv')

    #Read cell id to the larger area mapping
    id_to_region = pd.read_csv('data\\id_to_larger_area_' + graph_file_name + '.csv')

    #Read travel time percentile to cap accessibility (for each larger area)
    travel_time_limit_by_area_from_percentile = pd.read_csv(
        'data\\travel_time_limit_from_percentile_' + graph_file_name + '.csv')

    #Read buffer time for all OD pairs (between larger areas)
    buffer_time_between_areas = pd.read_csv(
        'data\\buffer_time_between_areas_' + graph_file_name + '.csv')


    # ---------------------------------------------------------------------
    # Add data to travel time matrix

    print('Adding data to travel time matrix...')

    map_id_jobs = jobs_pop.set_index('id')['jobs']
    map_id_pop = jobs_pop.set_index('id')['pop']
    map_id_area = id_to_region.set_index('id')['area']
    map_area_travel_time_limit = travel_time_limit_by_area_from_percentile.set_index('area')['time']
    map_od_buffer_time = buffer_time_between_areas.set_index('od')['buffer_time']

    mt['jobs_dest'] = mt.Destination.map(map_id_jobs)
    mt['code_area_orig'] = mt.Origin.map(map_id_area)
    mt['code_area_dest'] = mt.Destination.map(map_id_area)
    mt['travel_time_threshold'] = mt.code_area_orig.map(map_area_travel_time_limit)
    mt['od_pair'] = mt.code_area_orig + '-' + mt.code_area_dest
    mt['buffer_time'] = mt.od_pair.map(map_od_buffer_time).fillna(0)
    mt['Travel_time_with_buffer'] = mt.Travel_time + mt.buffer_time


    # ---------------------------------------------------------------------
    # Accessibility

    # Accessible jobs using Gravity-based impedance function
    mt['jobs_grav_without_reliability'] = mt.jobs_dest * alfa * np.exp(-beta * (mt.Travel_time/60))
    mt['jobs_grav_with_reliability'] = mt.jobs_dest * alfa * np.exp(-beta * (mt.Travel_time_with_buffer/60))

    # Calculation for each cell
    ids = np.unique(mt.Origin)
    total_ids = len(ids)
    gOrigin = mt.groupby('Origin')

    all_ids = []
    all_jobs_grav_base = []
    all_jobs_grav_reliability = []
    all_jobs_perc_base = []
    all_jobs_perc_reliability = []
    all_jobs_cumul30_base = []
    all_jobs_cumul30_reliability = []
    all_jobs_cumul60_base = []
    all_jobs_cumul60_reliability = []
    all_jobs_cumul90_base = []
    all_jobs_cumul90_reliability = []

    print('Calculating accessibility indicators (gravity, variable time threshold, fixed 30, 60, 90...)')
    for current_id in ids:
        print('id:',current_id,'of',total_ids)

        dest = gOrigin.get_group(current_id)
        all_ids.append(current_id)

        # ** Gravity-based **
        jobs_grav_base = dest.jobs_grav_without_reliability.sum()
        jobs_grav_reliability = dest.jobs_grav_with_reliability.sum()
        all_jobs_grav_base.append(jobs_grav_base)
        all_jobs_grav_reliability.append(jobs_grav_reliability)

        # ** Area specific time threshold based on percentile **
        area = map_id_area.loc[current_id]
        maximum_travel_time = map_area_travel_time_limit.loc[area]

        # Without reliability of travel time
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time <= maximum_travel_time)]
        qty_jobs_perc_base = destv['jobs_dest'].sum()
        all_jobs_perc_base.append(qty_jobs_perc_base)
        # With reliability of travel time (includes buffer time)
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time_with_buffer <= maximum_travel_time)]
        qty_jobs_perc_reliability = destv['jobs_dest'].sum()
        all_jobs_perc_reliability.append(qty_jobs_perc_reliability)


        # ** Cumulative opportunities (30 min) **

        # Without reliability of travel time
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time <= (30*60))]
        qty_jobs_cumul30_base = destv['jobs_dest'].sum()
        all_jobs_cumul30_base.append(qty_jobs_cumul30_base)
        # With reliability of travel time (includes buffer time)
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time_with_buffer <= (30 * 60))]
        qty_jobs_cumul30_reliability = destv['jobs_dest'].sum()
        all_jobs_cumul30_reliability.append(qty_jobs_cumul30_reliability)


        #** Cumulative opportunities (60 min) **

        # Without reliability of travel time
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time <= (60*60))]
        qty_jobs_cumul60_base = destv['jobs_dest'].sum()
        all_jobs_cumul60_base.append(qty_jobs_cumul60_base)
        # With reliability of travel time (includes buffer time)
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time_with_buffer <= (60 * 60))]
        qty_jobs_cumul60_reliability = destv['jobs_dest'].sum()
        all_jobs_cumul60_reliability.append(qty_jobs_cumul60_reliability)

        #** Cumulative opportunities (90 min) **

        # Without reliability of travel time
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time <= (90*60))]
        qty_jobs_cumul90_base = destv['jobs_dest'].sum()
        all_jobs_cumul90_base.append(qty_jobs_cumul90_base)
        # With reliability of travel time (includes buffer time)
        destv = dest[(dest.Walk_distance <= max_walk_distance) & (dest.Travel_time_with_buffer <= (90 * 60))]
        qty_jobs_cumul90_reliability = destv['jobs_dest'].sum()
        all_jobs_cumul90_reliability.append(qty_jobs_cumul90_reliability)



    access = pd.DataFrame({'id': all_ids,
                          'graph': graph_file_name,
                          'jobs_variablethreshold_base': all_jobs_perc_base,
                          'jobs_variablethreshold_reliability': all_jobs_perc_reliability,
                          'jobs_grav_base':all_jobs_grav_base,
                          'jobs_grav_reliability':all_jobs_grav_reliability,
                          'jobs_cumul30_base':all_jobs_cumul30_base,
                          'jobs_cumul30_reliability': all_jobs_cumul30_reliability,
                          'jobs_cumul60_base': all_jobs_cumul60_base,
                          'jobs_cumul60_reliability': all_jobs_cumul60_reliability,
                          'jobs_cumul90_base': all_jobs_cumul90_base,
                          'jobs_cumul90_reliability': all_jobs_cumul90_reliability
                          })
    
    #Add population and area data
    access['area'] = access['id'].map(map_id_area)
    access['pop'] = access['id'].map(map_id_pop)

    access.to_csv('data\\out\\accessibility_' + graph_file_name + '.csv')

    return mt, access


def population_weighted_average_and_comparisons(graph_file_name, access):

    # Population-weighted average accessibility
    print('Calculating population-weighted average accessibility')
    acg = access.groupby("area")

    # For each metric, calculate weighted average
    waverage = []
    for column in access.columns:
        if column[:4] == 'jobs': #only apply weighted average to columns with job calculation
            waverage.append(
                acg.apply(lambda x: np.average(x[column], weights=x['pop'])).rename(column))
    waverage = pd.concat(waverage,axis=1)

    waverage.to_excel('data\\out\\weighted_average_' + graph_file_name + '.xlsx')

    print('Population-weighted accessibility exported.')

    return waverage
