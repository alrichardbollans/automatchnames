import time

import pandas as pd

from wcvp_download import get_wcvp_zip, get_all_taxa, wcvp_columns, wcvp_accepted_columns

native_code_column = 'native_tdwg3_codes'
introduced_code_column = 'intro_tdwg3_codes'


def get_distributions_for_accepted_taxa(df: pd.DataFrame, acc_name_col: str, include_doubtful: bool = False,
                                        include_extinct: bool = False, wcvp_version: str = None):
    start = time.time()
    wcvp_with_dists = add_distribution_list_to_wcvp(include_doubtful, include_extinct, wcvp_version=wcvp_version)
    wcvp_with_dists = wcvp_with_dists[wcvp_with_dists[wcvp_columns['status']] == 'Accepted']
    wcvp_with_dists = wcvp_with_dists.dropna(subset=wcvp_accepted_columns['name'])
    wcvp_with_dists = wcvp_with_dists[
        [wcvp_accepted_columns['name'], native_code_column, introduced_code_column]]
    # relevant_data = wcvp_with_dists[wcvp_with_dists[wcvp_columns['wcvp_id'].isin(df[wcvp_id_col].values)]]
    for name in df[acc_name_col].unique():
        if name not in wcvp_with_dists[wcvp_accepted_columns['name']].values:
            raise ValueError(
                f'{name} not an accepted name in your WCVP version when checking for distribution data. This could be an issue with incorrectly specified version. Also check spelling')

    output = pd.merge(df, wcvp_with_dists, how='left', left_on=acc_name_col,
                      right_on=wcvp_accepted_columns['name'])
    if wcvp_accepted_columns['name'] not in df.columns:
        output = output.drop(columns=[wcvp_accepted_columns['name']])

    end = time.time()
    print(f'Time elapsed for getting taxa distributions: {end - start}s')
    return output


def _sorted_tuple(iterable):
    return tuple(sorted(iterable))


def add_distribution_list_to_wcvp(include_doubtful: bool = False,
                                  include_extinct: bool = False, wcvp_version: str = None):
    """
    Gets a copy of WCVP with distribution data for all taxa
    :param include_doubtful:
    :param include_extinct:
    :return:
    """
    # Only use accepted taxa for distributions as everything else is unreliable
    all_wcvp = get_all_taxa(version=wcvp_version)
    accepted_wcvp_data = all_wcvp[all_wcvp[wcvp_columns['status']] == 'Accepted']
    zip_filetime, wcvp_zip = get_wcvp_zip(version=wcvp_version)

    csv_file = wcvp_zip.open('wcvp_distribution.csv')
    all_dist_data = pd.read_csv(csv_file, encoding='utf-8', sep='|',
                                dtype={wcvp_columns['wcvp_id']: object,
                                       'plant_locality_id': object})
    all_dist_data = all_dist_data.dropna(subset=['area_code_l3'])
    csv_file.close()

    merged = pd.merge(accepted_wcvp_data, all_dist_data, on='plant_name_id', how='left')
    if include_doubtful and include_extinct:
        natives = merged[merged['introduced'] == 0]
        intros = merged[merged['introduced'] == 1]

    elif include_extinct and not include_doubtful:
        natives = merged[(merged['introduced'] == 0) & (merged['location_doubtful'] == 0)]
        intros = merged[(merged['introduced'] == 1) & (merged['location_doubtful'] == 0)]

    elif include_doubtful and not include_extinct:
        natives = merged[(merged['introduced'] == 0) & (merged['extinct'] == 0)]
        intros = merged[(merged['introduced'] == 1) & (merged['extinct'] == 0)]

    else:
        natives = merged[
            (merged['introduced'] == 0) & (merged['extinct'] == 0) & (merged['location_doubtful'] == 0)]
        intros = merged[
            (merged['introduced'] == 1) & (merged['extinct'] == 0) & (merged['location_doubtful'] == 0)]

    grouped_natives = natives.groupby('plant_name_id')['area_code_l3'].apply(_sorted_tuple).reset_index(
        name=native_code_column)

    grouped_intros = intros.groupby('plant_name_id')['area_code_l3'].apply(_sorted_tuple).reset_index(
        name=introduced_code_column)

    accepted_taxa_with_natives = pd.merge(accepted_wcvp_data, grouped_natives, how='left', on='plant_name_id')
    accepted_taxa_with_natives_intros = pd.merge(accepted_taxa_with_natives, grouped_intros, how='left',
                                                 on='plant_name_id')
    accepted_taxa_with_natives_intros = accepted_taxa_with_natives_intros[
        [introduced_code_column, native_code_column, wcvp_columns['acc_plant_name_id']]]
    accepted_taxa_with_natives_intros = accepted_taxa_with_natives_intros.dropna(
        subset=[wcvp_columns['acc_plant_name_id']])
    # Update taxa list with distributions from accepted taxa
    wcvp_data_with_distributions = pd.merge(all_wcvp, accepted_taxa_with_natives_intros.dropna(subset=[wcvp_columns['acc_plant_name_id']]),
                                            on=wcvp_columns['acc_plant_name_id'], how='left')
    # wcvp_data_with_distributions = wcvp_data_with_distributions.dropna(
    #     subset=[introduced_code_column, native_code_column], how='all')

    return wcvp_data_with_distributions
