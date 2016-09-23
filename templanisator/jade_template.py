import pyjade
import os
import re
from templanisator import jinja_template
import files
import templanisator.abstract_template as abc_temp


class JadeTemplateProcessor:
    def __init__(self, files_):
        self.files = files_
        self.do_template_processor()

    def do_template_processor(self):
        for file in self.files:
            self.include(file)
            self.extend(file)
            file.string_version = pyjade.simple_convert(file.string_version)

        self.files = jinja_template.Jinja2TemplateProcessor(self.files).html_files

    def get_file_to_include(self, name_of_file):
        for file in self.files:
            if file.path == name_of_file:
                return file
        print('Included file %s does not exist.' % name_of_file)
        exit()

    def include(self, file):
        for include in re.findall(u'include .*?\n', file.string_version):
            included_string = str()
            include_path = include.replace('include ', '').strip()
            if os.path.basename(include_path).find("*") == -1:
                if os.path.isfile(include_path) is False:
                    include_path += '.jade'
            for path in abc_temp.AbstractTemplate.path_generator(file.path, include_path):
                if path.__str__() == file.path:
                    continue
                if os.path.isfile(path.__str__()):
                    included_file = self.get_file_to_include(path.__str__())
                    included_file.check_string_version()
                    if included_file.string_version.find('include ') > 0:
                        self.include(included_file)
                    included_string += included_file.string_version
            file.string_version = file.string_version.replace(include, included_string)

    def extend(self, file):
        if file.string_version.find('extends ') >= 0:
            extend_string = re.search(u'extends .*?\n', file.string_version).group()
            file.string_version = file.string_version.replace(extend_string,
                                        '{%s extends "%s" %s}' % ('%', extend_string.replace('extends ', "").strip() + '.jade', '%'))
            print(file.string_version)

if __name__ == '__main__':
    files3 = [
        files.JadeFile('/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/er/base.jade'),
        files.JadeFile('/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/2.jade'),
        files.JadeFile
        ('/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/Folder/4.jade'),
        files.JadeFile
        ('/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/Folder/7.html'),
        files.JadeFile
        ('/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/Folder/6.html'),
        files.JadeFile
        ('/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/Folder/5.jade'),
        files.JadeFile(
        '/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/Folder/Folder2/Folder4/qwer1.html'),
        files.JadeFile(
        '/home/incode16/Desktop/projects/incodeParsing/tests/test_jade_project/NewxFolder/Folder/Folder2/Folder3/qwe.html'),
    ]
    JadeTemplateProcessor(files3)
