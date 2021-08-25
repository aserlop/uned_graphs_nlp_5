from typing import List
import networkx as nx


def get_vocab(token_LL: List[List[str]]):
    """
    Creates a dictionary containing all the unique tokens found in token_LL {'token': id}
    :param token_LL: List of list with all the tokens in the corpus
    :return: dictionary with unique tokens and ids {token1: id}
    """
    vocabulary_dic = dict()
    i = 0
    for token_list in token_LL:
        for token in token_list:
            if token not in vocabulary_dic:
                vocabulary_dic[token] = i
                i += 1

    return vocabulary_dic


def get_token_pairs(token_LL: List[List[str]], window_size: int):
    """
    Get all tokens pairs found in a window also it counts its frequency in all corpus
    :param token_LL: List of list with all the tokens in the corpus
    :param window_size: number of tokens to consult after each token
    :return: Dictionary with all token pairs and its frequency {(token1, token2): frequency}
    """
    token_pairs_dic = dict()
    for token_list in token_LL:
        for i, word in enumerate(token_list):
            for j in range(i + 1, i + window_size):
                if j >= len(token_list):
                    break
                pair = (word, token_list[j])
                if pair not in token_pairs_dic:
                    token_pairs_dic[pair] = 1
                else:
                    token_pairs_dic[pair] += 1

    return token_pairs_dic


def export_coocurrence_graph(vocabulary_dic,
                             token_pairs_dic,
                             output_path: str):
    """
    Given a vocabulary and token pairs, exports coocurrence graph (pajek format) using networkx parser
    :param vocabulary_dic: dictionary with unique tokens and ids {token1: id}
    :param token_pairs_dic: Dictionary with all token pairs and its frequency {(token1, token2): frequency}
    :param output_path: path to write output file
    :return:
    """
    graph = nx.Graph()

    nodes = vocabulary_dic.keys()
    graph.add_nodes_from(nodes)

    edges = [(*k, {'weight': str(v)}) for k, v in token_pairs_dic.items()]
    graph.add_edges_from(edges)

    pajek_str = '\n'.join([line.replace(' 0.0 0.0 ellipse', '') for line in nx.generate_pajek(graph)])

    open(output_path, 'w').write(pajek_str)
