"""
    Script for renaming the labels to a custom classes.names, based on
    the COCO dataset.

    Author: Rodrigo Heira Akamine
    Last modified: November 14, 2021
"""
import os


def get_original_to_custom(original_path, custom_path):
    """ Reads the original coco.names file and the custom classes.names file
    then returns a dictionary like {original_index: custom_index}, with only
    the classes presented in the custom classes.names file.

    Parameters:
    -----------
        original_path: str
            Path to the original classes.names file
        custom_path: str
            Path to the custom classes.names file

    Returns:
    --------
        dict_custom: dict
            Dictionary linkin the original class index with the custom class
            index, and containing only the classes present in the custom file.
    """
    original_file = original_path
    custom_file = custom_path
    try:
        with open(original_file, 'r') as f:
            lines = f.readlines()
    except:
        print('File "%s" not found' % original_file)
    original_coco_list = [line.rstrip() for line in lines] 
    print("ORIGINAL:\n", original_coco_list)

    try:
        with open(custom_file, 'r') as f:
            lines = f.readlines()
    except:
        print('File "%s" not found' % custom_file)
    custom_coco_list = [line.rstrip() for line in lines]
    print("CUSTOM:\n", custom_coco_list)

    dict_custom = {}
    for name in custom_coco_list:
        dict_custom[original_coco_list.index(name)] = custom_coco_list.index(name)

    print("DICTIONARY:\n", dict_custom)
    return dict_custom


def modify_labels(dict_custom, file_path):
    """Takes the dictionary linking the original classes and the custom classes,
    and re-writes the labels files with only the custom classes.

    Parameters:
    -----------
        dict_custom: dict
            Dictionary linking the original classes indexes to the custom classes
            indexes
        file_path: str
            Path to the file to be rewritten with the custom classes index.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    with open(file_path, 'w') as f:
        for line in lines:
            values = line.split(' ')
            if int(values[0]) in dict_custom:
                for i, value in enumerate(values):
                    if i == 0:
                        custom_idx = str(dict_custom[int(value)])
                        f.write(custom_idx + ' ')
                    elif(i != (len(values) - 1)):
                        f.write(str(value) + ' ')
                    else:
                        f.write(str(value))


def main():
    original_path = './coco/classes.names'
    custom_path = './custom/coco/classes.names'
    dict_custom = get_original_to_custom(
        original_path=original_path,
        custom_path=custom_path
    )

    dir_path = "./data/custom/labels/val2014_custom/"
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        modify_labels(dict_custom, file_path)

    return 0


if __name__ == "__main__":
    main()
