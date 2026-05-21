import os
import pandas as pd
import numpy as np

from scipy.linalg import eig, inv



def analysis(SIM_DIR,
             repeat = np.arange(3),
             ratios=np.arange(2, 4.0, 0.2) ):

    result = pd.DataFrame(
        columns=['repeat', 'ratio_p', 'nb_change', 'tot_cell'])

    # repeat = np.arange(3)
    # ratios = np.arange(2, 4.2, 0.2)

    for r in repeat:
        sim_save_dir = SIM_DIR / str(r)
        for ratio in ratios:
            g = round(ratio, 1)
            dir_ = sim_save_dir / str(g)

            monolayer_d = load_datasets(
                os.path.join(sim_save_dir / str(g), 'monolayer1.hf5'))
            monolayer = Monolayer("mono", monolayer_d)
            count0 = len(np.unique(monolayer.edge_df[(monolayer.edge_df[
                                                          'face'].isin(
                monolayer.face_df[
                    monolayer.face_df['num_sides'] == 3].index)) &
                                                     (monolayer.edge_df[
                                                          'segment'] == 'lateral') & (
                                                         monolayer.edge_df[
                                                             'face'].isin(
                                                             monolayer.face_df[
                                                                 monolayer.face_df[
                                                                     'area'] > 0.01].index))][
                                       'cell']))

            try:
                monolayer_d = load_datasets(
                    os.path.join(sim_save_dir / str(g), 'monolayer299.hf5'))
            except:
                monolayer_d = load_datasets(
                    os.path.join(sim_save_dir / str(g), 'monolayer150.hf5'))
            monolayer = Monolayer("mono", monolayer_d)
            count = len(np.unique(monolayer.edge_df[(monolayer.edge_df[
                                                         'face'].isin(
                monolayer.face_df[
                    monolayer.face_df['num_sides'] == 3].index)) &
                                                    (monolayer.edge_df[
                                                         'segment'] == 'lateral') & (
                                                        monolayer.edge_df[
                                                            'face'].isin(
                                                            monolayer.face_df[
                                                                monolayer.face_df[
                                                                    'area'] > 0.01].index))][
                                      'cell']))

            count = count - count0
            result = pd.concat([result, pd.DataFrame({'repeat': r,
                                                      'ratio_p': g,
                                                      'nb_change': count,
                                                      'tot_cell': monolayer.Nc},
                                                     index=[0])],
                               ignore_index=True)

    result['pourcentage'] = result['nb_change'] / result['tot_cell'] * 100
    result.to_csv(os.path.join(SIM_DIR, 'result_pourcentage_min.csv'))

    return result


def calculate_angle_between_segments(point_a, point_b, point_c, point_d):
    # Define vectors
    vector_ab = np.array([point_b[i] - point_a[i] for i in range(3)])
    vector_cd = np.array([point_d[i] - point_c[i] for i in range(3)])

    # Calculate dot product
    dot_product = np.dot(vector_ab, vector_cd)

    # Calculate magnitudes
    magnitude_ab = np.linalg.norm(vector_ab)
    magnitude_cd = np.linalg.norm(vector_cd)

    # Ensure no division by zero
    if magnitude_ab == 0 or magnitude_cd == 0:
        raise ValueError("One of the segments is of zero length.")

    # Calculate cosine of the angle
    cos_theta = dot_product / (magnitude_ab * magnitude_cd)

    # Ensure the value is within the valid range for arccos due to numerical errors
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    # Calculate the angle in radians and convert to degrees
    theta = np.arccos(cos_theta)
    angle_degrees = np.degrees(theta)

    return angle_degrees


def tenseur_analysis(SIM_DIR,
                     repeat = np.arange(3),
                     ratios=np.arange(2, 4.0, 0.2)):

    result = pd.DataFrame(columns=['repeat', 'ratio_p', 'T_i', 'eigen'])

    for r in repeat:
        sim_save_dir = SIM_DIR / str(r)
        for ratio in ratios:
            g = round(ratio, 1)
            dir_ = sim_save_dir / str(g)
            try:
                monolayer_d = load_datasets(
                    os.path.join(sim_save_dir / str(g), 'monolayer299.hf5'))
            except:
                monolayer_d = load_datasets(
                    os.path.join(sim_save_dir / str(g), 'monolayer150.hf5'))
            monolayer = Monolayer("mono", monolayer_d)
            id_new_edges = monolayer.edge_df[(monolayer.edge_df['face'].isin(
                monolayer.face_df[monolayer.face_df['num_sides'] == 3].index))
                                             & (monolayer.edge_df['face'].isin(
                monolayer.face_df[monolayer.face_df['area'] > 0.01].index))
                                             & (((monolayer.edge_df[
                                                      'sz'] > 0.4) & (
                                                             monolayer.edge_df[
                                                                 'tz'] > 0.4)) |
                                                ((monolayer.edge_df[
                                                      'sz'] < -0.4) & (
                                                             monolayer.edge_df[
                                                                 'tz'] < -0.4)))
                                             ].index

            # Pour chaque edge apical (ou basal) d'une face triangulaire
            mm_apical = []
            mm_basal = []
            for id_ in id_new_edges:
                # Recuperation des faces voisines
                id_face_neighbours = monolayer.get_neighbors(
                    monolayer.edge_df.loc[id_]['face'], elem='face')
                neighbouring_face = monolayer.face_df.loc[
                    list(id_face_neighbours)]

                # recuperation des faces uniquement apicale(ou basale)
                faces = []
                segment = ""
                for nf in neighbouring_face.index:
                    if ((monolayer.edge_df[monolayer.edge_df['face'] == nf][
                             'sz'] > 0.2).all() & (
                            monolayer.edge_df[monolayer.edge_df['face'] == nf][
                                'tz'] > 0.2).all()):
                        if monolayer.face_df.loc[nf]['opposite'] == -1:
                            faces.append(nf)
                            segment = "apical"
                    elif ((monolayer.edge_df[monolayer.edge_df['face'] == nf][
                               'sz'] < -0.2).all() & (monolayer.edge_df[
                                                          monolayer.edge_df[
                                                              'face'] == nf][
                                                          'tz'] < -0.2).all()):
                        if monolayer.face_df.loc[nf]['opposite'] == -1:
                            faces.append(nf)
                            segment = 'basal'

                if len(faces) == 2:
                    # Creation de la matrice m
                    X, Y, Z = monolayer.face_df.loc[faces[0]][list("xyz")] - \
                              monolayer.face_df.loc[faces[1]][list("xyz")]

                    m = np.array([[X ** 2, X * Y, X * Z],
                                  [Y * X, Y ** 2, Y * Z],
                                  [Z * X, Z * Y, Z ** 2]
                                  ])
                    m = m[:2, :2]
                    if segment == 'apical':
                        mm_apical.append(m)
                    elif segment == 'basal':
                        mm_basal.append(m)

            mm_apical = np.array(mm_apical)
            mm_basal = np.array(mm_basal)
            T_i = mm_apical.shape[0] * mm_apical.mean(axis=0) - mm_basal.shape[
                0] * mm_basal.mean(axis=0)

            # Eigen value calculation
            # Diagonalisation
            vals, vecs = eig(T_i)
            diag_m = np.zeros((2, 2))
            for i in range(0, len(vals)):
                diag_m[i, i] = vals[i].real

            result = pd.concat([result, pd.DataFrame({'repeat': r,
                                                      'ratio_p': g,
                                                      'T_i': [T_i],
                                                      'eigen': [diag_m]})],
                               ignore_index=True)
    return result