def get_step_length():
    """
    step length is approximated to be proportional to the height of pedestrian
    """
    height = 1.75  # in meters
    return 0.415 * height


def calculate_steps(accl_data):
    """
    :param accel_data: pandas dataframe with 3 columns, "x", "y", "z" representing acceleration in m/s^2
    and index of dataframe is "timestamp"

    returns: pandas dataframe with 2 columns "timestamp" and "steplength"

    for this MP assume that the step length is same for each step,
    use the get_step_length function to get the step length

    the timestamp is the time when the step is detected

    NOTE: timestamps should be among the values in the timestamp column,
    you are not expected to do any time interpolation
    """
    # replace the following dummy with your implementation
    # steps = pd.DataFrame({"timestamp": np.sort(np.random.choice(accl_data.index, 10, replace=False)).tolist(),
    #                       "steplength": get_step_length()})

    accl_data = accl_data.to_numpy()
    timestamps = []
    n = accl_data.shape[0]
    combined_accls = np.zeros((n))
    for i in range(n):
        ax, ay, az = accl_data[i, 0:3]
        combined_accls[i] = math.sqrt(ax ** 2 + ay ** 2 + az ** 2)

    sampling_freq = 100
    padding = 50
    cutoff_freq = 3

    normalized_cutoff_freq = 2 * cutoff_freq / sampling_freq
    numerator_coeffs, denominator_coeffs = signal.butter(5, normalized_cutoff_freq)
    padded_accls = np.pad(combined_accls, (padding, padding), 'wrap')
    filtered_signal = signal.lfilter(numerator_coeffs, denominator_coeffs, padded_accls)
    filtered_signal = filtered_signal[padding: -padding]

    offset = 0
    window_size = 200
    padded_filtered_signal = np.pad(filtered_signal, (0, window_size), 'wrap')
    mean_filtered_signal = np.zeros(accl_data.shape[0])
    for i in range(accl_data.shape[0]):
        mean_filtered_signal[i] = np.mean(padded_filtered_signal[i:i + window_size])
    mean_filtered_accl = mean_filtered_signal + offset

    if filtered_signal[0] > mean_filtered_accl[0]:
        start_from_above = True
    else:
        start_from_above = False
    flag = False
    for i in range(0, n, 10):
        if start_from_above:
            if filtered_signal[i] > mean_filtered_accl[i] and flag is False:
                flag = True
            elif filtered_signal[i] < mean_filtered_accl[i] and flag is True:
                timestamps.append(i)
                flag = False
        else:
            if filtered_signal[i] < mean_filtered_accl[i] and flag is False:
                flag = True
            elif filtered_signal[i] > mean_filtered_accl[i] and flag is True:
                timestamps.append(i)
                flag = False

    steps = pd.DataFrame({"timestamp": timestamps, "steplength": get_step_length()})

    return steps


def calculate_final_position(steps_with_walking_direction, start_position):
    """
    :param steps_with_walking_direction: pandas dataframe with 3 columns "timestamp", "steplength", and "walking_direction"

    walking_direction is an angle in degrees with global frame x-axis. It can be from 0 degrees to 360 degrees.
    for e.g. if walking direction is 90 degrees, user is walking in the positive y-axis direction

    NOTE: In the given test cases, the walking direction is same through out the trajectory
    but in hidden cases the walking direction may change

    step_length is in meters

    :param start_position: starting position of the user. It is tuple (x,y)

    return (x,y) coordinate of the final position in meters
    """
    n = steps_with_walking_direction.shape[0]
    x, y = start_position[0], start_position[1]
    for i in range(n):
        steplength = steps_with_walking_direction["steplength"][i]
        angle = steps_with_walking_direction["walking_direction"][i]
        x += math.cos(math.radians(angle)) * steplength
        y += math.sin(math.radians(angle)) * steplength

    return (x, y)
