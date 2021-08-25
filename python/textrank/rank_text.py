import numpy as np
from typing import List, Tuple


def rank_tokens(vocab,
                token_pairs,
                damping: float = 0.85,
                min_diff: float = 1e-5,
                num_epochs: int = 10) -> List[Tuple[str, float]]:
    """
    Based on a input vocabulary and token pairs, rank the vocabulary usin textrank algorithm
    :param vocab: dictionary with unique tokens and ids {token1: id}
    :param token_pairs: Dictionary with all token pairs and its frequency {(token1, token2): frequency}
    :param damping: damping factor, by default 0.85
    :param min_diff: minimun difference to pass to next epoch
    :param num_epochs: number of epoch to iterate
    :return: list of ranked tokens ([(token, weight)])
    """

    # Init Normalized matrix
    norm_matrix = get_norm_matrix(vocab, token_pairs)

    # Init weights(pagerank value)
    weight = np.array([1] * len(vocab))

    # Iteration
    previous_weight = 0
    for epoch in range(num_epochs):
        weight = (1 - damping) + damping * np.dot(norm_matrix, weight)
        if abs(previous_weight - sum(weight)) < min_diff:
            break
        else:
            previous_weight = sum(weight)

    # Get weight for each node
    token_weight_list = list()
    for word, index in vocab.items():
        token_weight_list.append((word, weight[index]))

    # Sort tokens according the weight
    ranked_tokens = sorted(token_weight_list, key=lambda item: item[1], reverse=True)

    return ranked_tokens


def get_norm_matrix(vocabulary_dic, token_pairs_dic) -> np.ndarray:
    """
    Get a normalized matrix from a vocabulary and tokens paris, it creates
    :param vocabulary_dic: dictionary with unique tokens and ids {token1: id}
    :param token_pairs_dic: dictionary with all token pairs and its frequency {(token1, token2): frequency}
    :return: Normalized matrix
    """
    # Build matrix
    vocab_size = len(vocabulary_dic)
    matrix = np.zeros((vocab_size, vocab_size), dtype='float')
    for word1, word2 in token_pairs_dic:
        i, j = vocabulary_dic[word1], vocabulary_dic[word2]
        matrix[i][j] = 1

    # Get Symmeric matrix
    matrix = symmetrize(matrix)

    # Normalize matrix by column
    norm = np.sum(matrix, axis=0)
    norm_matrix = np.divide(matrix, norm, where=norm != 0)  # this is ignore the 0 element in norm

    return norm_matrix


def symmetrize(matrix: np.ndarray) -> np.ndarray:
    """
    Makes a matrix symmetric
    :param matrix: matrix to make symmetric
    :return: symmetric matrix
    """
    return matrix + matrix.T - np.diag(matrix.diagonal())


def get_keyphrases(ranked_tokens: List[Tuple[str, float]], num_keyphrases: List[str]) -> List[str]:
    """
    From a textranked list of tokens obtain the top ones
    :param ranked_tokens: list of ranked tokens ([(token, weight)])
    :param num_keyphrases: number of keyphrases to extract from top
    :return: list of the top keyphrases
    """
    keyphrases = [tup[0] for tup in ranked_tokens][:num_keyphrases]

    return keyphrases


def export_keyphrases(keyphrases: List[str], output_path: str):
    """
    Export kephrases in a textfile
    :param keyphrases:
    :param output_path: path to write output file
    :return:
    """
    keyphrases_str = '\n'.join(keyphrases)
    open(output_path, 'w').write(keyphrases_str)
