"""This scripts extracts all the templates and modules from one given XML file.

The script processes the XML files in stream like fashion using using a SAX parser.
Whenever the script finds a template or a module page, it saves all the meta data
and all the information needed by MediaWiki for that page. It saves the pages in
MySQL insertion file, where every row contains 70 pages.

Arguments
---------
input_file : string
   The XML input file to be processed.
output_directory: string
   The output directory where to save the extracted templates and modules.

Example
-------
python extract_templates_and_modules.py input_file output_directory

"""


import xml.sax
import codecs
import MySQLdb
import dateutil.parser
import sys
import os

class TemplatesAndModulesHandler( xml.sax.ContentHandler ):
   def __init__(self, input_file, output_file_name):
      self.init()
      self.input_file = input_file
      self.output_file_name = output_file_name
      self.file_output = open(output_file_name, 'wb')
      line = "BEGIN;\n\n".encode('utf8')
      self.file_output.write(line)
      self.num_per_row = 70
      self.count = 0
      self.total = 0
      self.closed_row = False


   def finalize(self):
      if self.closed_row == False:
         self.file_output.write(";\n".encode('utf8'))
      line = "\nCOMMIT;".encode('utf8')
      self.file_output.write(line)
      self.file_output.close()
      os.system("rm " + self.input_file)
      output_dir_path = os.path.dirname(self.output_file_name)
      with open(os.path.join(output_dir_path,  "log.txt"), "a") as myfile:
         myfile.write("done " + os.path.basename(self.output_file_name) + "\n")


   def init(self):
      self.page_title = ""
      self.page_ns = "-1"
      self.page_redirect = False
      self.revision_text = ""
      self.revision_sha1 = ""
      self.revision_timestamp = ""
      self.revision_model = ""
      self.data = ""


   # Call when an element starts
   def startElement(self, tag, attributes):
      self.data = ""
      if tag == "page":
         self.init()
      elif tag == "redirect":
         self.page_redirect = True


   # Call when an elements ends
   def endElement(self, tag):
      if tag == "revision" and (self.page_ns == "10" or self.page_ns == "828"):
         self.parse_revision()
      elif tag == "title":
         self.page_title = self.data
      elif tag == "ns":
         self.page_ns = self.data
      elif tag == "text":
         self.revision_text = self.data
      elif tag == "sha1":
         self.revision_sha1 = self.data
      elif tag == "timestamp":
         self.revision_timestamp = self.data
      elif tag == "model":
         self.revision_model = self.data
      elif tag == "mediawiki":
         self.finalize()


   # Call when data is read
   def characters(self, content):
      if self.page_ns == "-1" or self.page_ns == "10" or self.page_ns == "828":
         self.data = self.data + content


   def parse_revision(self):
      if self.total % 10000 == 0:
         print("%s processed..." % (self.total))

      comma = True
      if self.count == 0:
         line = "INSERT INTO tmtable ( id, page_len, redirect, model, timestamp, sha1, ns, title, text, new_timestamp ) VALUES ".encode('utf8')
         self.file_output.write(line)
         comma = False
         self.closed_row = False

      page_len = self.utf8len(self.revision_text)
      if self.page_redirect == False:
         redirect = 0
      else:
         redirect = 1
      timestamp = int(dateutil.parser.parse(self.revision_timestamp).timestamp())
      if self.page_ns == "10":
         title = MySQLdb.escape_string(self.page_title[9:]).decode()
      else:
         title = MySQLdb.escape_string(self.page_title[7:]).decode()
      text = MySQLdb.escape_string(self.revision_text).decode()

      if comma:
         line = ", ( 1, %s, %s, '%s', %s, '%s', %s, '%s', '%s', 1 )" % \
            (page_len, redirect, self.revision_model, timestamp, self.revision_sha1, self.page_ns, title, text)
      else:
         line = "( 1, %s, %s, '%s', %s, '%s', %s, '%s', '%s', 1 )" % \
            (page_len, redirect, self.revision_model, timestamp, self.revision_sha1, self.page_ns, title, text)

      line = line.encode('utf8')
      self.file_output.write(line)
      self.count += 1
      self.total += 1

      if self.count == self.num_per_row:
         self.file_output.write(";\n".encode('utf8'))
         self.count = 0
         self.closed_row = True
  

   def utf8len(self, s):
      return len(s.encode('utf-8'))


def parse_file(input_file, output_file):
   # Create an XMLReader
   parser = xml.sax.make_parser()
   # Turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # Override the default ContextHandler
   Handler = TemplatesAndModulesHandler(input_file, output_file)
   parser.setContentHandler( Handler )
   
   parser.parse(input_file)


if ( __name__ == "__main__"):
   if len(sys.argv) != 3:
      print("Please provide the input XML and the output directory!")
      exit(1)
   input_file = sys.argv[1]
   output_directory = sys.argv[2]
   output_file = os.path.join(output_directory, os.path.basename(input_file) + ".sql")
   
   parse_file(input_file, output_file)
