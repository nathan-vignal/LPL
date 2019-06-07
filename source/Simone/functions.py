import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cmath as mt
import math
from matplotlib import colors
import pickle
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import sklearn.model_selection
import matplotlib.pyplot as plt
from IPython.core.debugger import Tracer
import time, sys
import sklearn
from sklearn.linear_model import LinearRegression
import sklearn.model_selection
import matplotlib as mpl
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import random
import itertools
from itertools import cycle
from matplotlib.pyplot import cm
import matplotlib.patches as mpatches
from IPython.core.debugger import Tracer
from source.pathManagment import getSimoneOutputPath
import os.path


# data = pd.read_pickle('..\output\data.pkl')
def download_data(n_directory, name_file):
    path = os.path.join(getSimoneOutputPath(), "X"+ str(n_directory))
    path_name_file = os.path.join(path, str(name_file) +".pkl")
    file = pd.read_pickle(path_name_file)
    return file


def upload_data(N, file, name_file):

    path = os.path.join(getSimoneOutputPath(),"X"+ str(N))
    path_name_file_plk = os.path.join(path,name_file+".pkl")
    path_name_file_csv = os.path.join(path,name_file+".csv")


    file.to_pickle(path_name_file_plk)
    file.to_csv(path_name_file_csv, sep='\t', encoding='utf-8')
    return path_name_file_plk




def linear_regression_parameter(X, test_SIZE):
    # Use only one feature
    X_input = X[['lenght_utterance', 'distance_to_end', 'median_duration']]
    Y_output = X['duration']

    # Split the data into training/testing sets
    # Split the targets into training/testing sets

    if test_SIZE == 0:
        X_train = X_input
        Y_train = Y_output
    else:
        X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X_input, Y_output,
                                                                                     test_size=test_SIZE,
                                                                                     random_state=5)

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(X_train, Y_train)
    parameters = pd.DataFrame(list(zip(X_input.columns, regr.coef_)), columns=['features', 'estimate_coefficients'])
    print(parameters)

    if test_SIZE == 0:
        return regr, parameters, X_train, Y_train
    else:

        # Make predictions using the testing set
        Y_pred = regr.predict(X_test)

        # The coefficients
        # The mean squared error
        print("\nMean squared error: %.3f" % mean_squared_error(Y_test, Y_pred))
        # Explained variance score: 1 is perfect prediction
        print('\nVariance score: %.2f' % r2_score(Y_test, Y_pred))

        # Plot outputs
        Y_test = pd.DataFrame(Y_test)
        result = pd.concat([Y_test, X_test], axis=1)
        index_selected = result.index.values
        df = pd.DataFrame({'index': index_selected, 'predicted_duration': Y_pred})
        df = df.set_index('index')
        result = pd.concat([df, result], axis=1)
        result['distance_to_end'] = pd.to_numeric(result['distance_to_end'], errors='coerce').fillna(0)
        result['lenght_utterance'] = pd.to_numeric(result['lenght_utterance'], errors='coerce').fillna(0)

        result.plot(x='distance_to_end', y='predicted_duration', kind='scatter', grid=False, alpha=0.15, color='black',
                    figsize=(15, 10))
        result.plot(x='distance_to_end', y='duration', kind='scatter', grid=False, alpha=0.15, color='blue',
                    figsize=(15, 10))
        plt.xlabel("Distance utterance to the end (word)")
        plt.ylabel("Duration(s) ")
        plt.title("Expected & real duration vs distance utterance to the end ")
        plt.show()

        return regr, parameters, result, X_train, Y_train





# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def merging_consecutive_silence(X, N_directory):
    silence_tot = X[(X['word'] == '[silence]')]
    silence_tot.index = range(len(silence_tot.index))
    N = len(silence_tot)
    i = 0
    progress = (1 / N)
    condition = True
    while condition:

        if (silence_tot.loc[[i]].end_time.item() == silence_tot.loc[[i + 1]].start_time.item()):

            silence_tot.at[(i + 1), 'start_time'] = silence_tot.loc[[i]].start_time

            silence_tot = silence_tot.drop([i])
            i = i + 1
        else:
            i = i + 1

        condition = i < N - 1
        progress = progress + (1 / N)
        update_progress(progress)
    upload_data(N_directory, silence_tot, 'silence_tot')
    return silence_tot


def mark_short_silence(X, silence_tot, min_time_silence):
    silence_tot['duration'] = silence_tot['end_time'] - silence_tot['start_time']
    silence_tot.loc[silence_tot['duration'] < min_time_silence, 'word'] = 'SHORT[silence]'
    NO_silence_tot = X[(~X['word'].isin(['[silence]']))]
    frames = [silence_tot, NO_silence_tot]
    conversation_tot_new = pd.concat(frames)
    conversation_tot_new.sort_values(['ID_conversation', 'ID_speaker', 'start_time'], ascending=[True, True, True],
                                     inplace=True)
    conversation_tot_new.reset_index(inplace=True)

    return conversation_tot_new


def label_new_turn(conversation_tot_new, min_time_silence, N_directory):
    list_id_conv = conversation_tot_new['ID_conversation'].unique()
    progress = (1 / len(list_id_conv))
    for conv in list_id_conv:

        for id_speaker in ['A', 'B']:
            selection = conversation_tot_new[(conversation_tot_new['ID_conversation'] == conv)
                                             & (conversation_tot_new['ID_speaker'] == id_speaker)]
            silence_start = selection[selection['word'] == '[silence]'].start_time
            silence_end = selection[selection['word'] == '[silence]'].end_time
            time_silence = pd.concat([silence_start, silence_end])

            time_silence = time_silence.sort_values()
            time_silence = time_silence.tolist()

            if not time_silence:
                time_silence.append(0)
                time_silence.append(max(selection.end_time))
            else:
                if time_silence[0] == 0:
                    del time_silence[0]
                else:
                    time_silence.append(0)
                if time_silence[-1] == max(selection.end_time):
                    del time_silence[-1]
                else:
                    time_silence.append(max(selection.end_time))
            time_silence.sort()
            id_turn = 1
            for start, end in zip(time_silence[0::2], time_silence[1::2]):
                indice_modify = selection[((selection['start_time'] >= start) & (selection['end_time'] <= end))].index
                conversation_tot_new.set_value(indice_modify, 'ID_turn', id_turn, takeable=False)

                id_turn = id_turn + 1
        progress = progress + (1 / len(list_id_conv))
        update_progress(progress)

    min_time_silence_ms = min_time_silence * 1000
    name_upload = 'conversation_label_silence' + str(int(min_time_silence_ms)) + 'ms'
    upload_data(N_directory, conversation_tot_new, name_upload)
    return conversation_tot_new


def overlapping(N_intervals_perc, id_conv, min_turn_duration, n_significative_word, id_speaker1, id_speaker2,
                Stop_words, conversation_tot_new):
    OVERLAP = []
    OVERLAP_VECTOR = []
    T_OVERLAP_VECTOR = []
    TURN_LATENCY = []
    TURN_LATENCY_VECTOR = []
    T_TURN_LATENCY_VECTOR = []
    TIME_INTERVENT = []
    AVERAGE_TURN1 = []
    AVERAGE_SILENCE1 = []
    NUMBER_TURN1 = []
    NUMBER_TRANSITION = []
    PERC_TURN_LESS_2SEC = []

    convers_1 = conversation_tot_new[
        (conversation_tot_new['ID_conversation'] == str(id_conv)) & (conversation_tot_new['ID_speaker'] == id_speaker1)]
    convers_2 = conversation_tot_new[
        (conversation_tot_new['ID_conversation'] == str(id_conv)) & (conversation_tot_new['ID_speaker'] == id_speaker2)]
    inf = min(convers_1['start_time'].min(), convers_2['start_time'].min())
    sup = max(convers_1['end_time'].max(), convers_2['end_time'].max())

    duration = sup - inf

    if sum(N_intervals_perc[:len(N_intervals_perc)]) == 1:
        pass
    else:
        print('Error the % interval in not = 1.0 ')
        return None

    limits = [(inf + sum(N_intervals_perc[:i]) * duration) for i in range(len(N_intervals_perc))]
    limits.append(sup)

    # incr = (sup - inf)/N
    # limits = [(incr*i + inf)  for i in range(N + 1)]

    silence_1 = convers_1[convers_1['ID_turn'].isnull()]
    silence_2 = convers_2[convers_2['ID_turn'].isnull()]

    turn_duration1 = (
                convers_1.groupby(['ID_turn'])['end_time'].max() - convers_1.groupby(['ID_turn'])['start_time'].min())
    turn_duration1 = pd.DataFrame({'ID_turn': turn_duration1.index, 'duration': turn_duration1.values})

    turn_start1 = (convers_1.groupby(['ID_turn'])['start_time'].min())
    turn_start1 = pd.DataFrame({'ID_turn': turn_start1.index, 'start': turn_start1.values})

    turn_end1 = (convers_1.groupby(['ID_turn'])['end_time'].max())
    turn_end1 = pd.DataFrame({'ID_turn': turn_end1.index, 'end': turn_end1.values})

    number_significative_word1 = convers_1[(~convers_1['word'].isin(Stop_words))].groupby(['ID_turn']).count().ID
    number_significative_word1 = pd.DataFrame(
        {'ID_turn': number_significative_word1.index, 'n_significative_word': number_significative_word1.values})

    frames = [turn_duration1, number_significative_word1['n_significative_word']]
    number_significative_word1 = pd.merge(turn_duration1, number_significative_word1, how='left', on='ID_turn')

    frames = [turn_duration1, turn_start1['start'], turn_end1['end'],
              number_significative_word1['n_significative_word']]

    turn1 = pd.concat(frames, axis=1)

    turn_duration2 = (
                convers_2.groupby(['ID_turn'])['end_time'].max() - convers_2.groupby(['ID_turn'])['start_time'].min())
    turn_duration2 = pd.DataFrame({'ID_turn': turn_duration2.index, 'duration': turn_duration2.values})

    turn_start2 = (convers_2.groupby(['ID_turn'])['start_time'].min())
    turn_start2 = pd.DataFrame({'ID_turn': turn_start2.index, 'start': turn_start2.values})

    turn_end2 = (convers_2.groupby(['ID_turn'])['end_time'].max())
    turn_end2 = pd.DataFrame({'ID_turn': turn_end2.index, 'end': turn_end2.values})

    number_significative_word2 = convers_2[(~convers_2['word'].isin(Stop_words))].groupby(['ID_turn']).count().ID
    number_significative_word2 = pd.DataFrame(
        {'ID_turn': number_significative_word2.index, 'n_significative_word': number_significative_word2.values})

    frames = [turn_duration2, number_significative_word2['n_significative_word']]
    number_significative_word2 = pd.merge(turn_duration2, number_significative_word2, how='left', on='ID_turn')

    frames = [turn_duration2, turn_start2['start'], turn_end2['end'],
              number_significative_word2['n_significative_word']]

    turn2 = pd.concat(frames, axis=1)

    list_turn2 = turn2[
        (turn2['duration'] >= min_turn_duration) & (turn2['n_significative_word'] >= n_significative_word)].ID_turn
    list_turn2 = list_turn2.tolist()

    for j in range(len(N_intervals_perc)):

        ## select turn in the j-imo inteval
        turn1_interval = turn1[((turn1['start'] < limits[j + 1]) & (turn1['start'] > limits[j])) |
                               ((turn1['end'] < limits[j + 1]) & (turn1['end'] > limits[j]))]
        turn2_interval = turn2[((turn2['start'] < limits[j + 1]) & (turn2['start'] > limits[j])) |
                               ((turn2['end'] < limits[j + 1]) & (turn2['end'] > limits[j]))]

        # print(limits)
        # print('turn1_interval',turn1_interval)
        ## redifine the limits of the interval turns
        ## speaker A

        if turn1_interval.empty:
            NUMBER_TURN1.append(float('NaN'))
            AVERAGE_TURN1.append(float('NaN'))
            PERC_TURN_LESS_2SEC.append(float('NaN'))
            OVERLAP.append(float('NaN'))
            OVERLAP_VECTOR.append([])
            T_OVERLAP_VECTOR.append([])
            TURN_LATENCY.append(float('NaN'))
            TURN_LATENCY_VECTOR.append([])
            T_TURN_LATENCY_VECTOR.append([])
            TIME_INTERVENT.append(float('NaN'))
            NUMBER_TRANSITION.append(float('NaN'))

            continue
        else:
            pass

        if ((turn1_interval.iloc[[0]].start.item() < limits[j]) & (turn1_interval.iloc[[0]].end.item() > limits[j])):
            # print(turn1_interval.head(1).index )
            indice = turn1_interval.head(1).index
            turn1_interval.at[indice, 'start'] = limits[j]
        else:
            pass

        if ((turn1_interval.iloc[[-1]].start.item() < limits[j + 1]) & (
                turn1_interval.iloc[[-1]].end.item() > limits[j + 1])):
            # print(turn1_interval.tail(1).index )
            indice = turn1_interval.tail(1).index
            turn1_interval.at[indice, 'end'] = limits[j + 1]
        else:
            pass

        ## re-compute duration
        turn1_interval['duration'] = turn1_interval['end'] - turn1_interval['start']

        list_turn1 = turn1_interval[(turn1_interval['duration'] >= min_turn_duration) & (
                    turn1_interval['n_significative_word'] >= n_significative_word)].ID_turn
        list_turn1 = list_turn1.tolist()
        # print('turn1_interval ', turn1_interval)
        ## speaker B
        if turn2_interval.empty:
            OVERLAP.append(0)
            OVERLAP_VECTOR.append([])
            T_OVERLAP_VECTOR.append([])
            TURN_LATENCY_VECTOR.append([])
            T_TURN_LATENCY_VECTOR.append([])
            TURN_LATENCY.append(0)
            TIME_INTERVENT.append(turn1_interval['duration'].sum())
            number_turn_duration1 = turn1_interval['duration'].count()
            avg_turn_duration1 = turn1_interval['duration'].mean()
            NUMBER_TURN1.append(number_turn_duration1)
            NUMBER_TRANSITION.append(0)
            AVERAGE_TURN1.append(avg_turn_duration1)
            PERC_TURN_LESS_2SEC.append(
                (turn1_interval[turn1_interval['duration'] < 2].ID_turn.count()) / (turn1_interval.ID_turn.count()))

            continue
        else:
            pass
        # print('turn2_interval', turn2_interval)
        if ((turn2_interval.iloc[[0]].start.item() < limits[j]) & (turn2_interval.iloc[[0]].end.item() > limits[j])):
            # print(turn2_interval.head(1).index )
            indice = turn2_interval.head(1).index
            turn2_interval.at[indice, 'start'] = limits[j]
        else:
            pass

        if ((turn2_interval.iloc[[-1]].start.item() < limits[j + 1]) & (
                turn2_interval.iloc[[-1]].end.item() > limits[j + 1])):
            # print(turn1_interval.tail(1).index )
            indice = turn2_interval.tail(1).index
            turn2_interval.at[indice, 'end'] = limits[j + 1]
        else:
            pass
        ## re-compute duration
        turn2_interval['duration'] = turn2_interval['end'] - turn2_interval['start']

        list_turn2 = turn2_interval[(turn1_interval['duration'] >= min_turn_duration) & (
                    turn2_interval['n_significative_word'] >= n_significative_word)].ID_turn
        list_turn2 = list_turn2.tolist()

        # print('turn2_interval', turn2_interval)
        # compute average turn duration and count turns

        # speaker A
        number_turn_duration1 = turn1_interval['duration'].count()
        avg_turn_duration1 = turn1_interval['duration'].mean()

        NUMBER_TURN1.append(number_turn_duration1)
        AVERAGE_TURN1.append(avg_turn_duration1)
        # compute percentage of the number of turn less than 2 seconds

        PERC_TURN_LESS_2SEC.append(
            (turn1_interval[turn1_interval['duration'] < 2].ID_turn.count()) / (turn1_interval.ID_turn.count()))

        ## select silences in the j-imo inteval
        silence1_interval = silence_1[
            ((silence_1['start_time'] < limits[j + 1]) & (silence_1['start_time'] > limits[j])) |
            ((silence_1['end_time'] < limits[j + 1]) & (silence_1['end_time'] > limits[j]))]
        silence2_interval = silence_2[
            ((silence_2['start_time'] < limits[j + 1]) & (silence_2['start_time'] > limits[j])) |
            ((silence_2['end_time'] < limits[j + 1]) & (silence_2['end_time'] > limits[j]))]

        ## redifine limits of silences turn
        ## speaker A
        # print(limits)
        # print(silence1_interval)
        if ((silence1_interval.iloc[[0]].start_time.item() < limits[j]) & (
                silence1_interval.iloc[[0]].end_time.item() > limits[j])):
            # print(silence1_interval.head(1).index )
            indice = silence1_interval.head(1).index
            silence1_interval.at[indice, 'start_time'] = limits[j]
        else:
            pass

        if ((silence1_interval.iloc[[-1]].start_time.item() < limits[j + 1]) & (
                silence1_interval.iloc[[-1]].end_time.item() > limits[j + 1])):
            # print(silence1_interval.tail(1).index )
            indice = silence1_interval.tail(1).index
            silence1_interval.at[indice, 'end_time'] = limits[j + 1]
        else:
            pass
        # print(silence1_interval)

        ## compute overlap and turn latency

        overlap = 0
        overlap_vector = []
        t_overlap_vector = []
        turn_latency = 0
        turn_latency_vector = []
        t_turn_latency_vector = []
        number_transition = 0
        p_start_turn2 = limits[j]
        p_end_turn1 = limits[j]

        for id_turn1 in list_turn1:
            c_start_turn1 = turn1_interval[turn1_interval['ID_turn'] == id_turn1].start.item()
            # print('c_start_turn1' , c_start_turn1)
            # print('p_start_turn2',p_start_turn2)
            c_start_turn2 = turn2_interval[
                (turn2_interval['start'] < c_start_turn1) & (turn2_interval['start'] >= p_start_turn2)
                & (turn2_interval['end'] >= p_end_turn1)].start
            # print('c_start_turn2 \n', c_start_turn2)
            p_end_turn1 = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].end).item()
            if len(c_start_turn2) == 0:
                continue
            else:
                c_start_turn2M = max(c_start_turn2)
                c_end_turn2M = turn2_interval[turn2_interval['start'] == c_start_turn2M].end
                # print('c_end_turn2M',c_end_turn2M.item())

                ##total overlap
                if (c_end_turn2M.item() > (turn1_interval[turn1_interval['ID_turn'] == id_turn1].end).item()):

                    overlap = overlap + (turn1_interval[turn1_interval['ID_turn'] == id_turn1].duration).item()
                    p_start_turn2 = c_start_turn2M

                    overlap_vector.append((turn1_interval[turn1_interval['ID_turn'] == id_turn1].duration).item())
                    START = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item()
                    END = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].end).item()
                    t_overlap_vector.append(START + ((END - START) / 2))
                else:

                    number_transition = number_transition + 1
                    if (c_end_turn2M.item() - (turn1_interval[turn1_interval['ID_turn'] == id_turn1].start)).item() < 0:
                        turn_latency = turn_latency + (c_end_turn2M.item() - (
                            turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item())
                        turn_latency_vector.append((c_end_turn2M.item() - (
                            turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item()))

                        START = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item()
                        END = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].end).item()
                        t_turn_latency_vector.append(START + ((END - START) / 2))
                    # partial overlap
                    else:
                        overlap = overlap + (c_end_turn2M.item() - (
                            turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item())
                        overlap_vector.append(
                            c_end_turn2M.item() - (turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item())
                        START = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item()
                        END = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].end).item()
                        t_overlap_vector.append(START + ((END - START) / 2))

                    p_start_turn2 = (turn1_interval[turn1_interval['ID_turn'] == id_turn1].start).item()

                # print('overlap \n',  overlap)
        # print(turn_latency_vector)
        time_intervent = turn1_interval['duration'].sum()

        NUMBER_TRANSITION.append(number_transition)

        TURN_LATENCY.append(turn_latency)
        OVERLAP.append(overlap)
        OVERLAP_VECTOR.append(overlap_vector)
        T_OVERLAP_VECTOR.append(t_overlap_vector)
        TURN_LATENCY_VECTOR.append(turn_latency_vector)
        T_TURN_LATENCY_VECTOR.append(t_turn_latency_vector)
        TIME_INTERVENT.append(time_intervent)

    return [id_conv, id_speaker1, OVERLAP_VECTOR, T_OVERLAP_VECTOR, OVERLAP, TURN_LATENCY_VECTOR, T_TURN_LATENCY_VECTOR,
            TURN_LATENCY, TIME_INTERVENT, PERC_TURN_LESS_2SEC, AVERAGE_TURN1, NUMBER_TURN1, NUMBER_TRANSITION, limits]





def turn_taking_corpus(id_speaker1, id_speaker2, N, min_turn_duration, n_significative_word, Stop_words, id_conve_list,
                       conversation_tot_new):
    OVERLAP_TOT = []
    OVERLAP_VECTOR_TOT = []
    T_OVERLAP_VECTOR_TOT = []
    TURN_LATENCY_TOT = []
    TURN_LATENCY_VECTOR_TOT = []
    T_TURN_LATENCY_VECTOR_TOT = []
    TIME_INTERVENT_TOT = []
    NUMBER_TURN_LESS_2SEC_TOT = []
    AVERAGE_TURN1_TOT = []
    NUMBER_TURN1_TOT = []
    LIMITS = []
    NUMBER_TRANSITION_TOT = []
    progress = (1 / len(id_conve_list))

    # id_conve_list = [2001, 2005, 2007]
    for conv in id_conve_list:
        [id_conv, id_speaker1, OVERLAP_VECTOR, T_OVERLAP_VECTOR, OVERLAP, TURN_LATENCY_VECTOR, T_TURN_LATENCY_VECTOR,
         TURN_LATENCY, TIME_INTERVENT, NUMBER_TURN_LESS_2SEC, AVERAGE_TURN1, NUMBER_TURN1, NUMBER_TRANSITION1,
         limits] = overlapping(N, conv, min_turn_duration, n_significative_word, id_speaker1, id_speaker2, Stop_words,
                               conversation_tot_new)
        OVERLAP_TOT.append(OVERLAP)
        OVERLAP_VECTOR_TOT.append(OVERLAP_VECTOR)
        T_OVERLAP_VECTOR_TOT.append(T_OVERLAP_VECTOR)
        TURN_LATENCY_TOT.append(TURN_LATENCY)
        TURN_LATENCY_VECTOR_TOT.append(TURN_LATENCY_VECTOR)
        T_TURN_LATENCY_VECTOR_TOT.append(T_TURN_LATENCY_VECTOR)
        TIME_INTERVENT_TOT.append(TIME_INTERVENT)
        NUMBER_TURN_LESS_2SEC_TOT.append(NUMBER_TURN_LESS_2SEC)
        AVERAGE_TURN1_TOT.append(AVERAGE_TURN1)
        NUMBER_TRANSITION_TOT.append(NUMBER_TRANSITION1)
        NUMBER_TURN1_TOT.append(NUMBER_TURN1)
        LIMITS.append(limits)
        # if (len(NUMBER_TRANSITION1) != 2):
        #    print('number of transition %s' % str(NUMBER_TRANSITION1))

        progress = progress + (1 / len(id_conve_list))
        update_progress(progress)

    OVERLAP_TOT = np.array(OVERLAP_TOT)
    OVERLAP_VECTOR_TOT = np.array(OVERLAP_VECTOR_TOT)
    T_OVERLAP_VECTOR_TOT = np.array(T_OVERLAP_VECTOR_TOT)
    TURN_LATENCY_TOT = np.array(TURN_LATENCY_TOT)
    TURN_LATENCY_VECTOR_TOT = np.array(TURN_LATENCY_VECTOR_TOT)
    T_TURN_LATENCY_VECTOR_TOT = np.array(T_TURN_LATENCY_VECTOR_TOT)
    TIME_INTERVENT_TOT = np.array(TIME_INTERVENT_TOT)
    NUMBER_TURN_LESS_2SEC_TOT = np.array(NUMBER_TURN_LESS_2SEC_TOT)
    AVERAGE_TURN1_TOT = np.array(AVERAGE_TURN1_TOT)
    NUMBER_TURN1_TOT = np.array(NUMBER_TURN1_TOT)
    NUMBER_TRANSITION_TOT = np.array(NUMBER_TRANSITION_TOT)

    OVERLAP_TOT_df = pd.DataFrame(
        {'overlap_' + str(i) + '_' + id_speaker1: OVERLAP_TOT[:, i] for i in range(OVERLAP_TOT.shape[1])})
    TURN_LATENCY_TOT_df = pd.DataFrame({'turn_latency' + str(i) + '_' + id_speaker1: TURN_LATENCY_TOT[:, i] for i in
                                        range(TURN_LATENCY_TOT.shape[
                                                  1])})  # TIME_INTERVENT_TOT_df = pd.DataFrame({'time_intervent_' + str(i)+ '_' + id_speaker1: TIME_INTERVENT_TOT[:,i] for i in range(TIME_INTERVENT_TOT.shape[1]) })
    NUMBER_TURN_LESS_2SEC_TOT_df = pd.DataFrame(
        {'number_turn_less_' + str(i) + '_' + id_speaker1: NUMBER_TURN_LESS_2SEC_TOT[:, i] for i in
         range(NUMBER_TURN_LESS_2SEC_TOT.shape[1])})
    AVERAGE_TURN1_TOT_df = pd.DataFrame({'average_turn_' + str(i) + '_' + id_speaker1: AVERAGE_TURN1_TOT[:, i] for i in
                                         range(AVERAGE_TURN1_TOT.shape[1])})
    NUMBER_TURN1_TOT_df = pd.DataFrame(
        {'number_turn_' + str(i) + '_' + id_speaker1: NUMBER_TURN1_TOT[:, i] for i in range(NUMBER_TURN1_TOT.shape[1])})

    # Tracer()()

    OVERLAP_VECTOR_TOT_df = pd.DataFrame(
        columns=['overlap_vec_' + str(id_speaker1) + '_' + str(i) for i in range(OVERLAP_VECTOR_TOT.shape[1])])

    T_OVERLAP_VECTOR_TOT_df = pd.DataFrame(
        columns=['t_overlap_vec_' + str(id_speaker1) + '_' + str(i) for i in range(T_OVERLAP_VECTOR_TOT.shape[1])])

    TURN_LATENCY_VECTOR_TOT_df = pd.DataFrame(
        columns=['latency_vec_' + str(id_speaker1) + '_' + str(i) for i in range(TURN_LATENCY_VECTOR_TOT.shape[1])])
    T_TURN_LATENCY_VECTOR_TOT_df = pd.DataFrame(
        columns=['t_turn_latency_vec_' + str(id_speaker1) + '_' + str(i) for i in
                 range(T_TURN_LATENCY_VECTOR_TOT.shape[1])])

    TIME_INTERVENT_TOT_df = pd.DataFrame(
        {'time_intervent_' + str(i) + '_' + id_speaker1: TIME_INTERVENT_TOT[:, i] for i in
         range(TIME_INTERVENT_TOT.shape[1])})
    NUMBER_TRANSITION_TOT_df = pd.DataFrame(
        {'number_turn_transition_' + str(i) + '_' + id_speaker1: NUMBER_TRANSITION_TOT[:, i] for i in
         range(NUMBER_TRANSITION_TOT.shape[1])})

    for i, j in itertools.product(range(OVERLAP_VECTOR_TOT.shape[1]), range(OVERLAP_VECTOR_TOT.shape[0])):
        OVERLAP_VECTOR_TOT_df.at[j, OVERLAP_VECTOR_TOT_df.columns[i]] = OVERLAP_VECTOR_TOT[j, i]

    for i, j in itertools.product(range(T_OVERLAP_VECTOR_TOT.shape[1]), range(T_OVERLAP_VECTOR_TOT.shape[0])):
        T_OVERLAP_VECTOR_TOT_df.at[j, T_OVERLAP_VECTOR_TOT_df.columns[i]] = T_OVERLAP_VECTOR_TOT[j, i]

    for i, j in itertools.product(range(TURN_LATENCY_VECTOR_TOT.shape[1]), range(TURN_LATENCY_VECTOR_TOT.shape[0])):
        TURN_LATENCY_VECTOR_TOT_df.at[j, TURN_LATENCY_VECTOR_TOT_df.columns[i]] = TURN_LATENCY_VECTOR_TOT[j, i]

    for i, j in itertools.product(range(T_TURN_LATENCY_VECTOR_TOT.shape[1]), range(T_TURN_LATENCY_VECTOR_TOT.shape[0])):
        T_TURN_LATENCY_VECTOR_TOT_df.at[j, T_TURN_LATENCY_VECTOR_TOT_df.columns[i]] = T_TURN_LATENCY_VECTOR_TOT[j, i]

    df0 = OVERLAP_TOT_df.join(TURN_LATENCY_TOT_df)
    df1 = df0.join(TIME_INTERVENT_TOT_df)
    df2 = NUMBER_TURN_LESS_2SEC_TOT_df.join(AVERAGE_TURN1_TOT_df)
    df3 = df1.join(df2)
    df4 = df3.join(NUMBER_TURN1_TOT_df)
    df5 = df4.join(NUMBER_TRANSITION_TOT_df)
    df5 = df5.join(OVERLAP_VECTOR_TOT_df)
    df5 = df5.join(T_OVERLAP_VECTOR_TOT_df)
    df5 = df5.join(TURN_LATENCY_VECTOR_TOT_df)
    df5 = df5.join(T_TURN_LATENCY_VECTOR_TOT_df)

    df = pd.DataFrame({'id_conv': id_conve_list})

    df = df.join(df5)
    return df


def visualize_timing1(id_conv, X, word_trash, conversation_tot_new, x, delta):
    # original timing of the conersation

    convers_A = X[(X['ID_conversation'] == str(id_conv)) & (X['ID_speaker'] == 'A')]
    convers_B = X[(X['ID_conversation'] == str(id_conv)) & (X['ID_speaker'] == 'B')]

    # assign delta if it's
    # Tracer()()
    if delta <= 0:
        delta = max(convers_A.end_time.tolist() + convers_B.end_time.tolist())

    # speaker A
    significative_A = convers_A[(~convers_A['word'].isin(word_trash))]
    start_duration_significative_A = [(x, y) for x, y in
                                      zip(significative_A.start_time.tolist(), significative_A.duration.tolist())]

    silence_A = convers_A[(convers_A['word'].isin(['[silence]']))]
    start_duration_silence_A = [(x, y) for x, y in zip(silence_A.start_time.tolist(), silence_A.duration.tolist())]

    noise_A = convers_A[(convers_A['word'].isin(['[vocalized-noise]', '[noise]']))]
    start_duration_noise_A = [(x, y) for x, y in zip(noise_A.start_time.tolist(), noise_A.duration.tolist())]

    laughter_A = convers_A[(convers_A['word'].isin(['[laughter]']))]
    start_duration_laughter_A = [(x, y) for x, y in zip(laughter_A.start_time.tolist(), laughter_A.duration.tolist())]

    # speaker B

    significative_B = convers_B[(~convers_B['word'].isin(word_trash))]
    start_duration_significative_B = [(x, y) for x, y in
                                      zip(significative_B.start_time.tolist(), significative_B.duration.tolist())]

    silence_B = convers_B[(convers_B['word'].isin(['[silence]']))]
    start_duration_silence_B = [(x, y) for x, y in zip(silence_B.start_time.tolist(), silence_B.duration.tolist())]

    noise_B = convers_B[(convers_B['word'].isin(['[vocalized-noise]', '[noise]']))]
    start_duration_noise_B = [(x, y) for x, y in zip(noise_B.start_time.tolist(), noise_B.duration.tolist())]

    laughter_B = convers_B[(convers_B['word'].isin(['[laughter]']))]
    start_duration_laughter_B = [(x, y) for x, y in zip(laughter_B.start_time.tolist(), laughter_B.duration.tolist())]
    #####################################################################################
    # filtering silences and create new turns

    convers_A1 = conversation_tot_new[
        (conversation_tot_new['ID_conversation'] == str(id_conv)) & (conversation_tot_new['ID_speaker'] == 'A')]
    convers_B1 = conversation_tot_new[
        (conversation_tot_new['ID_conversation'] == str(id_conv)) & (conversation_tot_new['ID_speaker'] == 'B')]
    # [(i,j) for i in range(x) for j in range(y)]
    word_trash = ['[silence]', '[noise]', '[laughter]', '[vocalized-noise]']

    # speaker A
    significative_A1 = convers_A1[(~convers_A1['word'].isin(word_trash))]
    start_duration_significative_A1 = [(x, y) for x, y in
                                       zip(significative_A1.start_time.tolist(), significative_A1.duration.tolist())]

    silence_A1 = convers_A1[(convers_A1['word'].isin(['[silence]']))]
    start_duration_silence_A1 = [(x, y) for x, y in zip(silence_A1.start_time.tolist(), silence_A1.duration.tolist())]

    noise_A1 = convers_A1[(convers_A1['word'].isin(['[vocalized-noise]', '[noise]']))]
    start_duration_noise_A1 = [(x, y) for x, y in zip(noise_A1.start_time.tolist(), noise_A1.duration.tolist())]

    laughter_A1 = convers_A1[(convers_A1['word'].isin(['[laughter]']))]
    start_duration_laughter_A1 = [(x, y) for x, y in
                                  zip(laughter_A1.start_time.tolist(), laughter_A1.duration.tolist())]

    # speaker B

    significative_B1 = convers_B1[(~convers_B1['word'].isin(word_trash))]
    start_duration_significative_B1 = [(x, y) for x, y in
                                       zip(significative_B1.start_time.tolist(), significative_B1.duration.tolist())]

    silence_B1 = convers_B1[(convers_B1['word'].isin(['[silence]']))]
    start_duration_silence_B1 = [(x, y) for x, y in zip(silence_B1.start_time.tolist(), silence_B1.duration.tolist())]

    noise_B1 = convers_B1[(convers_B1['word'].isin(['[vocalized-noise]', '[noise]']))]
    start_duration_noise_B1 = [(x, y) for x, y in zip(noise_B1.start_time.tolist(), noise_B1.duration.tolist())]

    laughter_B1 = convers_B1[(convers_B1['word'].isin(['[laughter]']))]
    start_duration_laughter_B1 = [(x, y) for x, y in
                                  zip(laughter_B1.start_time.tolist(), laughter_B1.duration.tolist())]

    fig1 = plt.figure(figsize=(12, 7))

    ax = fig1.add_subplot(111)
    # ax = plt.subplots()
    ax.broken_barh(start_duration_noise_A, (20, 9), facecolors='gray')
    ax.broken_barh(start_duration_silence_A, (20, 9), facecolors='palegreen')
    ax.broken_barh(start_duration_laughter_A, (20, 9), facecolors='violet')
    ax.broken_barh(start_duration_significative_A, (20, 9), facecolors='orange')

    ax.broken_barh(start_duration_noise_B, (10.8, 9), facecolors='gray')
    ax.broken_barh(start_duration_silence_B, (10.8, 9), facecolors='palegreen')
    ax.broken_barh(start_duration_laughter_B, (10.8, 9), facecolors='violet')
    ax.broken_barh(start_duration_significative_B, (10.8, 9), facecolors='orange')
    ax.set_ylim(8, 33)
    ax.set_xlim(x, x + delta)
    ax.tick_params(labelsize=16)
    ax.set_xlabel('seconds', fontsize=14)
    ax.set_yticks([15, 25])
    ax.set_yticklabels(['speaker B', 'speaker A'], fontsize=34)
    ax.grid(True)

    ax.legend(['Noise', 'Silence', 'Laughter', 'Discourse'], bbox_to_anchor=(1.14, 1.04), fontsize=20)
    fig1.set_size_inches(35, 15, forward=True)
    ###################################################################################

    fig2 = plt.figure(figsize=(12, 7))
    ax1 = fig2.add_subplot(111)

    ax1.broken_barh(start_duration_noise_A1, (20, 9), facecolors='gray')
    ax1.broken_barh(start_duration_silence_A1, (20, 9), facecolors='palegreen')
    ax1.broken_barh(start_duration_laughter_A1, (20, 9), facecolors='violet')
    ax1.broken_barh(start_duration_significative_A1, (20, 9), facecolors='orange')

    ax1.broken_barh(start_duration_noise_B1, (10.8, 9), facecolors='gray')
    ax1.broken_barh(start_duration_silence_B1, (10.8, 9), facecolors='palegreen')
    ax1.broken_barh(start_duration_laughter_B1, (10.8, 9), facecolors='violet')
    ax1.broken_barh(start_duration_significative_B1, (10.8, 9), facecolors='orange')
    ax1.set_ylim(8, 33)
    ax1.set_xlim(x, x + delta)
    ax1.tick_params(labelsize=16)
    ax1.set_xlabel('seconds', fontsize=14)
    ax1.set_yticks([15, 25])
    ax1.set_yticklabels(['speaker B', 'speaker A'], fontsize=34)
    ax1.grid(True)

    ax1.legend(['Noise', 'Silence', 'Laughter', 'Discourse'], bbox_to_anchor=(1.14, 1.04), fontsize=20)
    fig2.set_size_inches(35, 15, forward=True)

    return plt.show()
#   --------------------------------------------------------------------------------------

def visualize_timing(id_conv, X, word_trash, x, delta, list_colors, fig1, ax):
    # original timing of the conersation
    convers_A = X[(X['ID_conversation'] == str(id_conv)) & (X['ID_speaker'] == 'A')]
    convers_B = X[(X['ID_conversation'] == str(id_conv)) & (X['ID_speaker'] == 'B')]
    # assign delta if it's
    # Tracer()()
    if delta <= 0:
        delta = max(convers_A.end_time.tolist() + convers_B.end_time.tolist())

    colors = itertools.cycle(list_colors)
    f_color_A = list()
    # speaker A
    start_duration_tot_A = list()
    for word in word_trash:
        silence_A = convers_A[(convers_A['word'].isin([word]))]
        start_duration_silence_A = [(x, y) for x, y in zip(silence_A.start_time.tolist(), silence_A.duration.tolist())]
        start_duration_tot_A.extend(start_duration_silence_A)
        f_color_A.extend([next(colors)] * len(start_duration_silence_A))

    silence_A = convers_A[(~convers_A['word'].isin(word_trash))]
    start_duration_silence_A = [(x, y) for x, y in zip(silence_A.start_time.tolist(), silence_A.duration.tolist())]
    start_duration_tot_A.extend(start_duration_silence_A)
    f_color_A.extend(['orange'] * len(start_duration_silence_A))
    # speaker B
    colors = itertools.cycle(list_colors)
    f_color_B = list()
    start_duration_tot_B = list()
    for word in word_trash:
        silence_B = convers_B[(convers_B['word'].isin([word]))]
        start_duration_silence_B = [(x, y) for x, y in zip(silence_B.start_time.tolist(), silence_B.duration.tolist())]
        start_duration_tot_B.extend(start_duration_silence_B)
        f_color_B.extend([next(colors)] * len(start_duration_silence_B))

    silence_B = convers_B[(~convers_B['word'].isin(word_trash))]
    start_duration_silence_B = [(x, y) for x, y in zip(silence_B.start_time.tolist(), silence_B.duration.tolist())]
    start_duration_tot_B.extend(start_duration_silence_B)
    f_color_B.extend(['orange'] * len(start_duration_silence_B))
    #####################################################################################
    if fig1 is None:
        fig1 = plt.figure(figsize=(12, 7))
        ax = fig1.add_subplot(111)
    ax.broken_barh(start_duration_tot_A, (20, 9), facecolors=f_color_A)
    ax.broken_barh(start_duration_tot_B, (10.8, 9), facecolors=f_color_B)
    ax.set_ylim(8, 33)
    ax.set_xlim(x, x + delta)
    ax.tick_params(labelsize=16)
    ax.set_xlabel('seconds', fontsize=14)
    ax.set_yticks([15, 25])
    ax.set_yticklabels(['speaker B', 'speaker A'], fontsize=34)
    ax.grid(True)

    legend_dict = {}
    for key, color in zip(word_trash, list_colors):
        legend_dict[key] = color
    legend_dict['discourse'] = 'orange'
    patchList = []
    for key in legend_dict:
        data_key = mpatches.Patch(color=legend_dict[key], label=key)
        patchList.append(data_key)

    ax.legend(handles=patchList, bbox_to_anchor=(1.14, 1.04), fontsize=20)
    # ax.legend(word_trash, bbox_to_anchor=(1.14, 1.04),fontsize=20)
    # ax.legend((line1, line2, line3), ('label1', 'label2', 'label3'))
    fig1.set_size_inches(35, 15, forward=True)
    #plt.show()
    return fig1, ax



