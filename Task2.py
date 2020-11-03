import argparse
import os
import sys
import xml.etree.ElementTree as etree


def get_cmd_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', default='file.xml', help="Input XML file path. Default: file.xml")
    return arg_parser.parse_args()


def find_depth_recursively(path):
    tree = etree.parse(path)
    root = tree.getroot()

    def find_depth(root, level, max_depth):
        if level > max_depth:
            max_depth = level
        for child in list(root):
            max_depth = find_depth(child, level + 1, max_depth)
        return max_depth

    return find_depth(root, 0, 0)


def find_depth_without_recursion(path):
    max_depth = -1
    depth = -1
    for (event, _) in etree.iterparse(path, ['start', 'end']):
        if event == 'start':
            depth += 1
            if depth > max_depth:
                max_depth = depth
        if event == 'end':
            depth -= 1
    return max_depth


if __name__ == '__main__':
    args = get_cmd_args()
    if not os.path.exists(args.file):
        print('File specified does not exist')
        sys.exit(1)

    try:
        tree_depth_rec = find_depth_recursively(args.file)
        tree_depth_non_rec = find_depth_without_recursion(args.file)
        print(f'Tree depth is {tree_depth_rec} (found recursively)')
        print(f'Tree depth is {tree_depth_non_rec} (found non recursively)')
    except etree.ParseError as ex:
        print(f'Failed to parse file. Error text: {ex.msg}')
