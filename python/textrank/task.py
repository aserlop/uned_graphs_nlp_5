import os
import sys
import logging.config
import json
from datetime import datetime

import utils as ut
from clean_tokenize import clean_tokenize
from create_graph import get_vocab, get_token_pairs, export_coocurrence_graph
from rank_text import rank_tokens, export_keyphrases

if '__main__' == __name__:

    # ------------------------------------------------------------------------------------------------------------------
    # Configuracion de logging
    # ------------------------------------------------------------------------------------------------------------------
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    logging.basicConfig(filename=f'./textrank_{now}.log', filemode='w', level=logging.INFO)
    logging.info('START')

    # --------------------------------------------------------------------------------------------------------------
    # Arguments
    # --------------------------------------------------------------------------------------------------------------

    args_dic = json.load(open(sys.argv[1]))

    input_base_path = args_dic['input_base_path']
    output_base_path = args_dic['output_base_path']
    duplicated_char_list = args_dic['duplicated_char_list']
    valid_tag_list = args_dic['valid_tag_list']
    do_global_corpus = ut.str2bool(args_dic['do_global'])
    do_textrank = ut.str2bool(args_dic['do_textrank'])
    textrank_params_dic = args_dic['textrank_params']
    num_tokens_window = args_dic['num_tokens_window']
    num_keyphrases = args_dic['num_keyphrases']

    logging.info(sys.version)
    logging.info('Parametros:')
    logging.info('> input_base_path: {}'.format(input_base_path))
    logging.info('> output_base_path: {}'.format(output_base_path))
    logging.info('> duplicated_char_list: {}'.format(duplicated_char_list))
    logging.info('> valid_tag_list: {}'.format(valid_tag_list))
    logging.info('> do_global_corpus: {}'.format(do_global_corpus))
    logging.info('> do_textrank: {}'.format(do_textrank))
    logging.info('> textrank_params_dic: {}'.format(textrank_params_dic))
    logging.info('> num_tokens_window: {}'.format(num_tokens_window))
    logging.info('> num_keyphrases: {}'.format(num_keyphrases))

    # ----------------------------------------------------------------------------------------------------------
    # Main process
    # ----------------------------------------------------------------------------------------------------------

    logging.info(f'Reading files in input base path...')
    input_filename_list = [f for f in os.listdir(input_base_path) if 'txt' in f]
    corpus_dic = {i: {'raw_text':      open(f'{input_base_path}/{input_filename_list[i]}').read(),
                      'base_filename': '.'.join(input_filename_list[i].split('.')[:-1])}
                  for i in range(0, len(input_filename_list), 1)}
    logging.info(f'> total files readed: {len(input_filename_list)}')

    logging.info("Tokenizing documents...")
    for k in corpus_dic.keys():
        valid_token_pattern = '(^.+/[[A-Z]|$|\.|\:]+$)'
        corpus_dic[k]['tokens'] = [clean_tokenize(raw_text=corpus_dic[k]['raw_text'],
                                                  repeated_char_list=duplicated_char_list,
                                                  valid_pattern=valid_token_pattern,
                                                  valid_tag_list=valid_tag_list)]

    if do_global_corpus:
        logging.info("> Merging all document tokens into one...")
        corpus_dic = {0: {'tokens': ut.flatten_LL([v['tokens'] for k, v in corpus_dic.items()]),
                          'base_filename': 'global.txt'}}

    logging.info('Starting main process...')
    for doc_id in corpus_dic.keys():

        logging.info(f'> Starting document {doc_id} ...')

        logging.info(f'>>> Generating vocabulary and token pairs using a window of {num_tokens_window} tokens...')
        corpus_dic[doc_id]['vocabulary'] = get_vocab(corpus_dic[doc_id]['tokens'])
        logging.info(f'>>> Total num of tokens in vocabulary: {len(corpus_dic[doc_id]["vocabulary"])}')

        corpus_dic[doc_id]['token_pairs'] = get_token_pairs(corpus_dic[doc_id]['tokens'], num_tokens_window)
        logging.info(f'>>> Total num of tokens pairs: {len(corpus_dic[doc_id]["token_pairs"])}')

        logging.info(f'>>> Exporting coocurrence matrix...')
        output_filename = corpus_dic[doc_id]['base_filename'] + '.paj'
        output_path = f'{output_base_path}/{output_filename}'
        export_coocurrence_graph(vocabulary_dic=corpus_dic[doc_id]['vocabulary'],
                                 token_pairs_dic=corpus_dic[doc_id]['token_pairs'],
                                 output_path=output_path)

        if do_textrank:
            logging.info(f'>>> Ranking tokens...')
            corpus_dic[doc_id]['ranked_tokens'] = \
                rank_tokens(vocab=corpus_dic[doc_id]['vocabulary'],
                            token_pairs=list(corpus_dic[doc_id]['token_pairs'].keys()),
                            **textrank_params_dic)

            logging.info(f'>>> Selecting {num_keyphrases} keyphrases...')
            keyphrases = [tup[0] for tup in corpus_dic[doc_id]['ranked_tokens']][:num_keyphrases]
            corpus_dic[doc_id]['kephrases'] = keyphrases

            logging.info(f'>>> Exporting keyphrases...')
            output_filename = corpus_dic[doc_id]['base_filename'] + '.result'
            output_path = f'{output_base_path}/{output_filename}'
            export_keyphrases(keyphrases, output_path)

    logging.info('END')
