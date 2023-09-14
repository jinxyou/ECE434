def find_missing_window(X, Y, N):
    """Identifies where data is missing.
    Args:
      X: The ground truth signal
      Y: Signal with 1 time window missing from X and added noise
      N: Approximate length of the missing time window
    Returns: Candidate indices of the missing time window in X. See section above for an example.
    You may return up to 3 candidate results. You will receive full points as long as 1 falls within the grading criteria.
    For example, if you think the missing time window starts at index 3 but indices 8 and 40 are also possible,
    then return [3, 8, 40].
    """
    len_x = len(X)
    len_y = len(Y)
    len_window = np.max([N, np.abs(len_x - len_y)])
    C = np.full((len_x + 1, len_y + 1), np.inf)
    C[0, 0] = 0

    for i in range(1, len_x + 1):
        for j in range(np.max([1, i - len_window]), np.min([len_y, i + len_window]) + 1):
            distance = np.abs(X[i - 1] - Y[j - 1])
            C[i][j] = distance + np.min([C[i - 1, j - 1], C[i, j - 1], C[i - 1, j]])

    cand = []
    for i in range(len_x + 1):
        index_min = np.argmin(C[i])
        cand.append(index_min)

    from collections import Counter
    cand_counter = Counter(cand)
    top3_cand = [x[0] for x in cand_counter.most_common(3)]

    return top3_cand
