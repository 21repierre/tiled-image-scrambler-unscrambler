from split_image import split_image, reverse_split
import numpy as np
import skimage as ski
import os
import matplotlib.pyplot as plt
from scipy.stats import entropy


def get_index(filename):
    # Used to sort the files according to the index in their name
    return int(filename.split('_')[-1].split('.')[0])


def numpy_index(arr, e):
    for i in range(arr.shape[0]):
        if arr[i] == e:
            return i


def rename_tiles():
    # Used for the split_image library
    all_paths = os.listdir("tiles")
    image_extension = "." + all_paths[0].split(".")[-1]

    for i in range(len(all_paths)):
        os.rename(f"tiles/{all_paths[i]}", f"tiles/tile_{i}{image_extension}")


def rename_tiles_setup(setup):
    # Rename the tiles according to the setup at the end of the research
    first_path = os.listdir("tiles")[0]
    image_extension = "." + first_path.split(".")[-1]
    path_type = first_path.split(".")[0]
    path_type = path_type[:len(path_type) - 1]

    for i in range(len(setup)):
        os.rename(f"tiles/{path_type}{i}{image_extension}", f"tiles/result_{numpy_index(setup, i)}{image_extension}")


def concatenate_setup(all_tiles_color, setup, columns):
    image = 0
    line = 0

    reset_line = True
    first_line = True

    for i in range(all_tiles_color.shape[0]):
        if reset_line:
            line = np.copy(all_tiles_color[setup[i]])
            reset_line = False

        else:
            line = np.concatenate((line, all_tiles_color[setup[i]]), axis=1)

        if i % columns == columns - 1 and first_line:
            image = np.copy(line)
            reset_line = True
            first_line = False

        elif i % columns == columns - 1 and not first_line:
            image = np.concatenate((image, line))
            reset_line = True

    return image


def score(im1, im2):
    return np.var(entropy(np.concatenate((im1[:, [-1]], im2[:, [0]]), axis=1)))


# def total_score(all_tiles, setup, rows, columns):
#     setup_score = 0

#     for i in range(all_tiles.shape[0]):
#         if i % columns != columns - 1:
#             setup_score += score(all_tiles[setup[i]], all_tiles[setup[i + 1]])

#     return setup_score


def total_score(all_tiles, setup, columns):
    return np.var(entropy(concatenate_setup(all_tiles, setup, columns)))


def greedy_search(all_tiles, all_tiles_color, rows, columns, max_iterations):
    number_of_tiles = rows * columns
    setup = np.array(range(number_of_tiles))
    np.random.shuffle(setup)
    best_setup = np.copy(setup)
    best_score = total_score(all_tiles, best_setup, columns)

    # See the evolution of the best_score and current_score
    timeline_best_score = np.zeros(max_iterations)
    timeline_current_score = np.zeros(max_iterations)
    
    for i in range(max_iterations):
        if i % 100 == 0:
            print(i)

        idx1, idx2 = np.random.choice(setup.shape[0], 2, replace=False)
        setup[idx1], setup[idx2] = setup[idx2], setup[idx1]
        current_score = total_score(all_tiles, setup, columns)

        if current_score < best_score: # If better, we keep the permutation
            best_setup[idx1], best_setup[idx2] = best_setup[idx2], best_setup[idx1]
            best_score = current_score

        # 1 chance out of two to still keep the bad permutation, or we reverse
        elif np.random.uniform() > 0.1:
            setup[idx1], setup[idx2] = setup[idx2], setup[idx1]
        
        timeline_best_score[i] = best_score
        timeline_current_score[i] = current_score

    return best_setup, best_score, timeline_best_score, timeline_current_score


def unshuffle_image(image_path, need_split, rows, columns, max_iterations):
    if need_split:
        split_image(image_path=image_path, rows=rows, cols=columns, should_square=False, should_cleanup=False, output_dir="tiles")

    all_tiles = np.array([ski.color.rgb2gray(ski.io.imread("tiles/" + path)) for path in os.listdir("tiles")], dtype=np.float64)
    all_tiles_color = np.array([ski.io.imread("tiles/" + path) for path in os.listdir("tiles")], dtype=np.float64)
    best_setup, best_score, timeline_best_score, timeline_current_score = greedy_search(all_tiles, all_tiles_color, rows, columns, max_iterations)

    rename_tiles_setup(best_setup)

    file_paths = sorted(["tiles/" + image_path for image_path in os.listdir("tiles")], key=get_index)
    reverse_split(file_paths, rows, columns, "result.jpg", False)

    x_axis = np.array(range(timeline_best_score.shape[0]))

    print(f"Final score: {best_score}")

    plt.plot(x_axis, timeline_best_score)
    # plt.plot(x_axis, timeline_current_score)
    plt.show()



# all_tiles = np.array([ski.color.rgb2gray(ski.io.imread("tiles/" + path)) for path in os.listdir("tiles")], dtype=np.float64)
# score_test = score(all_tiles[4], None, all_tiles[7], None, None)
# print(score_test)

# score_test = total_score(all_tiles, [i for i in range(9)], 3, 3)
# print(score_test)

# setup = np.array(range(9))
# np.random.shuffle(setup)
# print(setup)
# setup_score = total_score(all_tiles, setup, 3, 3)
# print(setup_score)

# rename_tiles()
# unshuffle_image("image-test.jpg", False, 3, 3, 10000)
unshuffle_image("puzzle-trouble-easy.jpg", True, 8, 8, 10000)

# split_image(image_path="image-test.jpg", rows=3, cols=3, should_square=False, should_cleanup=False, output_dir="tiles")
# file_paths = sorted(["tiles/" + image_path for image_path in os.listdir("tiles")], key=get_index)
# print(file_paths)
# reverse_split(file_paths, 8, 8, "recreated.jpg", False)
