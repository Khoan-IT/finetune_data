import soundfile as sf
import glob
import pandas as pd
import random
import os

from argparse import ArgumentParser
from scipy.io import wavfile
from tqdm import tqdm

def format_file(audios_folder, save_folder, wav_path, subsets):
    csv_file = pd.read_csv(wav_path)

    with open(os.path.join(save_folder, 'data.tsv'), mode='w') as fw:
        print(audios_folder, file=fw)
        for _,line in tqdm(csv_file.iterrows()):
            path = os.path.join(audios_folder, line['path'])
            try:
                sf.read(path)
                _, data = wavfile.read(path)
                print("{}\t{}".format(line['path'], data.shape[0]), file=fw)
            except:
                print(path)
            
    with open(os.path.join(save_folder, 'prompts.txt'), 'w') as f:
        for _,data in tqdm(csv_file.iterrows()):
            print('{} {}'.format(data['path'].split('.')[0], data['text']), file=f)
            
    save_data_folder = os.path.join(save_folder, 'data')
    if not os.path.exists(save_data_folder):
        os.makedir(save_data_folder)
        
    with open(os.path.join(save_folder, 'data.tsv')) as f:
            root = f.readline().rstrip()
            lines = [line.rstrip() for line in f]
            if len(subsets) == 2:
                valid_f = open(os.path.join(save_data_folder, 'valid.tsv'), 'w')
                train_f = open(os.path.join(save_data_folder, 'train.tsv'), 'w')
                print(root, file=valid_f)
                print(root, file=train_f)
                for line in tqdm(lines):
                    if random.random() > 0.05:
                        print(line, file=train_f)
                    else:
                        print(line, file=valid_f)
            else:
                test_f = valid_f = open(os.path.join(save_data_folder, 'test.tsv'), 'w')
                print(root, file=test_f)
                print(line, file=train_f)
                
                
def generate_transcript(save_folder, subsets):
    save_path = os.path.join(save_folder, 'data')
    path_transcript = os.path.join(save_folder, 'prompts.txt')       
    transcript = {}

    with open(path_transcript, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip('\n').split()
            name = l[0]
            text = " ".join(l[1:])
            transcript[name] = text.upper()

    for subset in subsets:
        name_audio = []
        with open(os.path.join(save_path, '{}.tsv'.format(subset)), 'r') as f:
            f.readline()
            lines = f.readlines()
            for line in lines:
                name_audio.append(line.split()[0].split('.')[0])
        
        wrd_file = open(os.path.join(save_path, '{}.wrd'.format(subset)), 'w')
        ltr_file = open(os.path.join(save_path, '{}.ltr'.format(subset)), 'w')
        
        for name in tqdm(name_audio):
            text = transcript[name]
            print(transcript[name].strip('\n'), file=wrd_file)
            print(" ".join(list(transcript[name].strip('\n').replace(" ", "|"))) + " |", file=ltr_file)
            
        wrd_file.close()
        ltr_file.close()
    

if __name__=="__main__":
        
    # Add arguments
    parser = ArgumentParser()
    parser.add_argument("-fa", "--folder_audio", dest="audios_folder", help="Please specify folder consisting audios", metavar="str")
    parser.add_argument("-fs", "--folder_save", dest="save_folder", help="Please specify destination to save", metavar="str")
    parser.add_argument("-pw", "--path_wav", dest="path_wav", help="Please specify path to wav.tsv", metavar="str")
    parser.add_argument("-sb", "--subsets", dest="subsets", help="Please specify list of subset Ex: train,valid", metavar="str")
    # parse arguments
    args = parser.parse_args()
    
    subsets = args.subsets.split(',')
    
    format_file(audios_folder=args.audios_folder, save_folder=args.save_folder, wav_path=args.path_wav, subsets=subsets)
    generate_transcript(save_folder=args.save_folder, subsets=subsets)