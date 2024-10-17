#
#loads audio files which have annotations 
#segments and saves chunks accordingly to segment size, 
#reads labels from annotations and state, save both in csv file

#all functions are defined in utils.py



import csv
import os
from info import i, printb, printr, printp, print
from utils import load_audioFiles_saves_segments, write_Statelabels_from_beeNotBeelabels, get_uniqueHives_names_from_File, split_samples_byHive, get_samples_id_perSet, get_features_from_samples, get_GT_labels_fromFiles, labels2binary, write_sample_ids_perHive, split_samples_ramdom

def get_list_samples_names(path):
    # List all .wav files in the given directory
    sample_ids = [f for f in os.listdir(path) if f.endswith('.wav')]
    return sample_ids
    

def main():
    #----------------------------------- parameters to change-----------------------------------#
    block_size = 60  # blocks of 60 seconds
    thresholds = [0, 5]  # minimum length for non-bee intervals: 0 or 5 seconds (creates one label file per threshold value)
    path_audioFiles = "D:\\archive" + os.sep  # path to audio files
    annotations_path = "D:\\archive" + os.sep  # path to .lab files
    path_save_audio_labels = 'D:\\OUT\\dataset_BeeNoBee_' + str(block_size) + 'sec' + os.sep  # path to save audio segments and label files.
    #-------------------------------------------------------------------------------------------#
    
    if not os.path.exists(path_save_audio_labels):
        os.makedirs(path_save_audio_labels)
    
    # Get the list of audio filenames from the audio file directory
    audiofilenames_list = [f for f in os.listdir(path_audioFiles) if f.endswith('.wav')]  # Example for .wav files

    # segments audio files, assigns label BeeNotBee to each block, writes labels to csv, saves segmented blocks in wav.
    load_audioFiles_saves_segments(audiofilenames_list, path_audioFiles, path_save_audio_labels, block_size, thresholds, annotations_path, read_beeNotBee_annotations='yes', save_audioSegments='yes')

    path_beeNotbee_labels = path_save_audio_labels + 'labels_BeeNotBee_th' + str(thresholds[0]) + '.csv' 
    write_Statelabels_from_beeNotBeelabels(path_save_audio_labels, path_beeNotbee_labels, states=['active', 'missing queen', 'swarm'])
    
    sample_ids = get_list_samples_names(path_save_audio_labels)  # get sample ids from audio segments folder.
    
    # split data by Hive 
    hives = write_sample_ids_perHive(sample_ids, path_save_audio_labels)  # retrieves unique hive names and also writes these to a file
    
    for i in range(3):
        split_dict = split_samples_byHive(0.1, 0.5, hives, path_save_audio_labels + 'split_byHive_' + str(i))
    
    # Split data randomly
    for i in range(3):
        split_dict = split_samples_ramdom(0.1, 0.5, path_save_audio_labels, path_save_audio_labels + 'split_random_' + str(i))

if __name__ == "__main__":
    main()
