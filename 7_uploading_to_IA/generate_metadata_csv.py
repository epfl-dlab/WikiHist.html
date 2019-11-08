"""This script generates the metadata csv file needed by the 'ia' command to upload files.

"""

import os
import csv

dir_to_upload = os.path.split(os.getcwd())[1]

header = ['identifier',
 'file',
 'collection',
 'title',
 'mediatype',
 'description',
 'licenseurl',
 'subject[0]',
 'subject[1]',
 'subject[2]',
 'subject[3]',
 'subject[4]',
 'subject[5]',
 'subject[6]']

first_line = ['<identifier>',
 '<file 0>',
 'opensource',
 '<title>',
 'data',
 'This is one file from the full articles dump of the English Wikipedia transformed to HTML format.',
 'https://creativecommons.org/licenses/by-sa/3.0/',
 'html',
 'wiki',
 'dumps',
 'data dumps',
 'enwiki',
 'English',
 'Wikipedia']

# set identifier, title, and file
first_line[header.index("identifier")] = dir_to_upload + "_html_dlab"
first_line[header.index("title")] = dir_to_upload
first_line[header.index("file")] = "page_id_count.txt"

with open('metadata.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(header)
    csv_writer.writerow(first_line)
