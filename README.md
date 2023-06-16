# Format data for finetune Speech2c and Wav2vec22

## Usage

This function is used to format finetuning data for Speech2c and Wav2vec2 (Create file `.tsv`, `.ltr`, `.wrd`)
```
$ python generate_finetune.py \
    --folder_audio path_to_folder_consisting_audio \
    --folder_save path_to_folder_save_all_files \
    --path_wav path_to_wav.tsv \
    --subsets list_of_subsets
    
###
python generate_finetune.py \
    --folder_audio ./unlabeled/ \
    --folder_save ./data/ \
    --path_wav ./wav.tsv \
    --subsets train,valid
###
```
