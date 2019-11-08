"""This script is used to combine all the MySQL insertion files obtained by the extraction process of templates and modules.

When the extraction process is done, in the directory where the results are saved,
there will be 558 MySQL insertion files generated. To make the creation of the MySQL
database which will hold the templates and the modules easier, it is best to concatenate
all the MySQL insertion files, to one big file. This script adds the begin and commit
lines at the beginning and at the end of the MySQL insertion file, and concatenates
all the 558 MySQL insertion files to one big file.

Example
-------
python generate_one_sql.py

"""


import os

all_sql = []
for (dirpath, dirnames, filenames) in os.walk("."):
	all_sql.extend([os.path.join(dirpath, x) for x in filenames if x.endswith(".sql")])

print("Total number of MySQL insertion files: " + str(len(all_sql)))

file_output = open("final_insert.sql", 'wb')
line = "BEGIN;\n\n".encode('utf8')
file_output.write(line)

for file in all_sql:
	file_input = open(file, 'rb')
	for line in file_input:
		if line.startswith(b"INSERT"):
			file_output.write(line)
	file_input.close()


line = "\nCOMMIT;".encode('utf8')
file_output.write(line)
file_output.close()
