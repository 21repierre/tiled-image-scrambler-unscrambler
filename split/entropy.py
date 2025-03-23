import skimage as ski
from scipy.stats import entropy
import numpy as np
import matplotlib.pyplot as plt
import os
from split_image import split_image, reverse_split

def count(arr, e):
    counter = 0
    for i in range(arr.shape[0]):
        if arr[i] == e:
            counter += 1

    return counter


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


# split_image(image_path="image-test.jpg", rows=3, cols=3, should_square=False, should_cleanup=False, output_dir="tiles")
# split_image(image_path="puzzle-trouble-easy.jpg", rows=8, cols=8, should_square=False, should_cleanup=False, output_dir="tiles")

rename_tiles()

rows = 8
columns = 8
number_of_tiles = rows * columns
all_tiles = np.array([ski.color.rgb2gray(ski.io.imread("tiles/" + path)) for path in os.listdir("tiles")], dtype=np.float64)

best_entropies = np.zeros(number_of_tiles)
best_indexes = np.zeros(number_of_tiles, dtype=np.int64)
is_in_last_column = np.array([False] for _ in range(number_of_tiles))

for i in range(number_of_tiles):
    best_entropy = np.inf
    best_index = i

    for j in range(number_of_tiles):
        if i == j:
            continue
        
        tile_1 = all_tiles[i]
        tile_2 = all_tiles[j]
        current_entropy = np.var(entropy(np.concatenate((tile_1[:, [-1]], tile_2[:, [0]]), axis=1)))

        if current_entropy < best_entropy:
            best_entropy = current_entropy
            best_index = j

    best_entropies[i] = best_entropy
    best_indexes[i] = best_index
    print(f"For image {i}, best is {best_index} with entropy {best_entropy}")

setup = - np.ones(number_of_tiles, dtype=np.int64)
ind_setup = 0

# for i in range(number_of_tiles):
#     if best_indexes[i] not in setup and count(best_indexes, best_indexes[i]) != 1:
#         setup[ind_setup] = best_indexes[i]
#         ind_setup += 1
#         print(f"Adding {best_indexes[i]} to setup")


for i in range(number_of_tiles):
    if i in setup or count(best_indexes, best_indexes[i]) != 1:
        continue

    adding_to_block = True
    block = [i]
    while adding_to_block:
        adding_to_block = False
        for j in range(i, number_of_tiles):
            if count(best_indexes, best_indexes[j]) != 1:
                continue

            if best_indexes[j] == block[0] and j not in setup:
                block = [j] + block
                adding_to_block = True

            elif block[-1] == j:
                block += [best_indexes[j]]
                adding_to_block = True

    for j in range(len(block)):
        setup[ind_setup] = block[j]
        ind_setup += 1

for i in range(number_of_tiles):
    if i not in setup:
        setup[ind_setup] = i
        ind_setup += 1

print(setup)

# rename_tiles_setup(setup)

# file_paths = sorted(["tiles/" + image_path for image_path in os.listdir("tiles")], key=get_index)
# reverse_split(file_paths, rows, columns, "result.jpg", False)
