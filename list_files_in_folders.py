#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, walk
#from os.path import isfile, isdir, join
from os.path import isdir, join


def add_trailing_char(filename, char=','):
    """
    Adds trailing defined char to the end of each line in the given file.
    """
    output = []
    output_file = 'title_output.csv'

    with open(filename, 'r') as f:
        for line in f:
            if len(line) > 1:
                newline = line[:-1] + char + line[-1]
                output.append(newline)
                #print newline
            else:
                output.append('\n')

    #print output

    with open(output_file, 'w') as f:
        for line in output:
            f.write(line)

    return output_file


def add_image_after_comma(filename, char=','):
    """
    Adds image after first comma sign. For Media lead image field.
    """
    string_to_add = 'public://images/media/no-image.png,'  # string to be added on every line.
    #output = []
    output_image_file = 'title_image_output.csv'

    with open(filename, 'r') as f:
        ammended_lines = [''.join([l.strip(), string_to_add, '\n']) for l in f.readlines() if len(l) > 1]
        #print ammended_lines

    with open(output_image_file, 'w') as f:
        f.writelines(ammended_lines)

    return output_image_file


def add_audio_path(fileprefix, fileaudio):
    """
    At the end of each line there should be a path to an audio file on the server.
    """
    result = []

    with open(fileaudio, 'r') as f:
        audio = f.readlines()

    with open(fileprefix, 'r') as f:
        prefix = f.readlines()

    # Concatinate strings
    print len(prefix)
    print len(audio)
    if len(prefix) == len(audio):
        for i in range(len(audio)):
            line = prefix[i].strip() + audio[i]
            print line
            result.append(line)
    else:
        print "Something went wrong. Prefix and audio part of string length don't mach."

    with open('finish.csv', 'w') as f:
        f.writelines(result)
        #for line in result:
        #    f.write(line)
        #    result.append(line)

    #print result

    return result


def collect_filenames_in_directory():
    """
    Go in to a root directory from where you want to collect all subfolders
    files and from there run this app.
    NOTE: this doesn't run recursively on all subfolders but only on
    the first level.
    """
    mypath = './'
    #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

    onlydirs.sort()
    #print onlydirs
    #print onlyfiles

    fl = []
    books = {}
    for b in onlydirs:
        for (dirpath, dirnames, filenames) in walk(mypath + '/' + b):
            fl.extend(filenames)
            break
        #  Exclude index.php file from listing in this golgota case.
        if 'index.php' in fl:
            fl.remove('index.php')
        fl.sort()
        #print 'fl:', fl
        books[b] = fl
        fl = []

    #for value in books:
    #    print value, ':', books[value]

    # write to a file everything
    with open('file_paths.txt', 'w') as f:
        f.write('Title,Media lead image,Audio\n')
        for book_name in books:

            book_num = len(books[book_name])
            if book_num != 0:
                if book_num > 1:
                    for file_name in books[book_name]:
                        f.write('public://media/bible-studies/' + book_name + '/')
                        f.write(file_name)
                        f.write('\n')
                elif book_num == 1:
                    f.write('public://media/bible-studies/' + book_name + '/')
                    f.write(books[book_name][0])
                    f.write('\n')

                #f.write('\n')  # Starting new folder, blank line above.
            #else:
            #    f.write(book_name + ':  Not containing files.')
            #    f.write('\n')
            #    f.write('\n')  # Starting new folder, blank line above.


def main():
    collect_filenames_in_directory()
    title_file = add_trailing_char('title.csv')
    title_image_file = add_image_after_comma(title_file)
    add_audio_path(title_image_file, 'file_paths.txt')

if __name__ == '__main__':
    main()
