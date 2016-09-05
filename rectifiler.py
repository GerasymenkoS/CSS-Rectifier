# -*- coding: utf-8 -*-
# !/home/incode7/PycharmProjects/incodeParsing/venv/bin/python

from css_selectors import CSSSelector
from files import MyFile, CSSFile, HTMLFile
from static_classes import Finder
from rectifiler_report import RectifilerReport
import sys
import os
import re
import time

start_time = time.time()


class CSSRectifier:
    def __init__(self):
        self.ignore = list()
        self.files = list()
        self.css_files, self.html_files = list(), list()
        self.css_selectors = list()
        self.percent_of_usage = str()

    def get_css_files(self):
        files = list()
        for file in self.files:
            if file.extention == 'css':
                files.append(file)
        return files

    def get_html_files(self):
        files = list()
        for file in self.files:
            if file.extention == 'html' or file.extention == 'htm':
                files.append(file)
        return files

    def add_selector(self, _selector, css_file):
        if len(self.css_selectors) > 0:
            tmp = list()
            for i in self.css_selectors:
                tmp.append(i.name)
            if _selector not in tmp:
                new_selector = CSSSelector(_selector, css_file)
                new_selector.add_line(css_file)
                self.css_selectors.append(new_selector)
            else:
                i = tmp.index(_selector)
                self.css_selectors[i].add_file(css_file)
                self.css_selectors[i].add_line(css_file)
        else:
            self.css_selectors.append(CSSSelector(_selector, css_file))

    def load_custom_ignore_files(self, dir_to_project):
        try:
            with open(dir_to_project+'/rectifiler_ignore.txt', 'r+') as f:
                for line in f:
                    if line[0] != '#':
                        self.ignore.append(line.rstrip())
        except FileNotFoundError:
            pass

    def load_ignore_files(self, dir_to_project):
        try:
            self.load_custom_ignore_files(dir_to_project)
            with open('files to ignore.txt', 'r+') as f:
                for line in f:
                    if line.rstrip() not in self.ignore:
                        self.ignore.append(line.rstrip())
        except FileNotFoundError:
            with open('files to ignore.txt', 'w') as f:
                for line in ['bootstrap.css', 'bootstrap.min.css', 'bootstrap-responsive.css',
                             'bootstrap-responsive.min.css', 'font-awesome.css',
                             'node_modules', 'venv', 'tmp']:
                    f.write(line+'\n')
            self.load_ignore_files(dir_to_project)

    def do_rectifier(self, home_directory, start=True, iteration=2, home='', old_dir=-1):
        if start:
            print('Start rectifiler....')
            home = home_directory.replace("/" + home_directory.split('/')[-1], "")
            self.load_ignore_files(dir_to_project=home_directory)
            Finder.load_ignore_pseudo()

            return self.do_rectifier(
                os.chdir(home_directory),
                start=False,
                home=home,
            )
        else:
            if home_directory != home:
                directory = os.listdir(os.getcwd())
                for item in directory:
                    if directory.index(item) <= old_dir:
                        continue
                    if os.path.isfile(os.getcwd() + '/' + item) and item[-3:] == 'css':
                        if item not in self.ignore:
                            # print(item)
                            self.files.append(MyFile(path=(os.getcwd() + '/' + item)))
                        # else:
                        #     print('IGNORE: ' + item)

                    elif os.path.isfile(os.getcwd() + '/' + item) and (item[-4:] == 'html' or item[-3:] == 'htm'):
                        self.files.append(MyFile(path=(os.getcwd() + '/' + item)))

                    if os.path.isdir(os.getcwd() + '/' + item) and item not in self.ignore:
                        os.chdir(os.getcwd() + '/' + item)
                        iteration += 2

                        return self.do_rectifier(
                            os.getcwd(),
                            start=False,
                            iteration=iteration,
                            home=home,
                        )
                os.chdir('../')

                if home_directory is None:
                    return self.css_minification()
                else:
                    old_dir = os.listdir(os.getcwd()).index(home_directory.split('/')[-1])
                    iteration -= 2

                return self.do_rectifier(
                    os.getcwd(),
                    start=False,
                    iteration=iteration,
                    home=home,
                    old_dir=old_dir,
                )

            else:
                return self.css_minification()

    def css_minification(self):
        print('Start minification....')
        for file in self.get_css_files():
            with open(file.path, 'r+') as f:
                css_file = f.read()
                css_file = css_file.replace("\t", "").replace("\n", "")

            for match in re.finditer(u"/*[^/]+\*/", css_file):
                css_file = css_file.replace(match.group(), "")

            space, media = False, False
            final_css = str()
            for i in range(len(css_file)):
                if css_file[i].isspace() is True and css_file[i + 1] == '{' or \
                        css_file[i].isspace() is True and css_file[i - 1] == ':'\
                        or css_file[i].isspace() is True and css_file[i + 1] == '+' \
                        or css_file[i].isspace() is True and css_file[i + 1] == '~' \
                        or css_file[i].isspace() is True and css_file[i + 1] == '>' \
                        or css_file[i].isspace() is True and css_file[i - 1] == ',':
                    continue
                elif css_file[i] == '@' and css_file[i:i + 6] == '@media':
                    media = True
                elif css_file[i] == '{' and media is False:
                    space = True
                elif css_file[i] == '}':
                    space = False

                if space is True:
                    final_css += css_file[i].rstrip()
                else:
                    final_css += css_file[i]

            self.css_files.append(CSSFile(file.path, final_css))
        self.css_separation()

    def css_separation(self):
        print('Start separation....')
        for css_file in self.css_files:
            only_classes = []
            minified_version = css_file.minified_version
            for match in re.finditer(u"{[^}]+}", minified_version):
                if match.group().count('{') > 1:
                    only_classes.append(str(match.group()).split('{')[1])
                    minified_version = minified_version.replace(match.group(), "¿")
                else:
                    minified_version = minified_version.replace(match.group(), '¿')

            minified_version = only_classes + minified_version.replace("}", '')[:-1].split('¿')
            media_count = [i for i in minified_version if i.find('@') >= 0]

            for i in media_count:
                minified_version.pop(minified_version.index(i))

            clean_css_classes = []
            for i in minified_version:
                if i not in clean_css_classes:
                    clean_css_classes.append(i)

            for clean_selector in clean_css_classes:
                self.add_selector(clean_selector, css_file)

            for clean_selector in self.css_selectors:
                clean_selector.parsing_alone_selectors()

        self.find_selectors_in_html()

    def create_html_files(self):
        self.html_files = [HTMLFile(file.path) for file in self.get_html_files()]
        return self.html_files

    def find_selectors_in_html(self):
        print('Start find selectors....')
        for html_file in self.create_html_files():
            with open(html_file.path) as html:
                html = html.read().replace('\t', '').replace('\n', '')
                html_file.check_tags(html)

                # html = html.replace(re.search(u'<head>(.+?)</head>', html).group(), '')
                for combo_selector in self.css_selectors:
                    Finder.find_selectors_in_html(html, combo_selector)
                    if combo_selector.usage is False and combo_selector.kind_usage is True:
                        for alone_selector in combo_selector.alone_selectors:
                            if alone_selector.alone_usage_for_file is True:
                                alone_selector.usage_files.append(html_file)
                                alone_selector.alone_usage_for_file = False

        self.calculate_percent_of_usage()

    def do_report(self):
        not_used_selectors = list()
        for not_used_selector in self.css_selectors:
            if not_used_selector.usage is False:
                not_used_selectors.append(not_used_selector)

        html = False
        html_files = list()

        for html_file in self.html_files:
            if html_file.opened_and_closed_tags_check is False:
                html_files.append(html_file)
                html = True

        RectifilerReport(
            percent=self.percent_of_usage,
            selectors=not_used_selectors,
            html=html,
            html_files=html_files
        )

    def calculate_percent_of_usage(self):
        usage_selectors = list()
        for selector_ in self.css_selectors:
            if selector_.usage:
                usage_selectors.append(selector_)

        self.percent_of_usage = 'Percent of usage: %s' \
                                % str(round(len(usage_selectors)/len(self.css_selectors) * 100, 2)) \
                                + '%'


if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    BASEDIR = os.path.dirname(
        os.path.realpath(sys.argv[0])
    )
    report_path, project_dir = BASEDIR, os.getcwd()
    report = False

    args = sys.argv[1:]
    if '--path' in args:
        try:
            project_dir = os.path.realpath(args[args.index('--path')+1])
        except IndexError:
            pass
    if '--report' in args:
        report = True
        try:
            report_path = os.path.realpath(args[args.index('--report') + 1])
        except IndexError:
            pass

    if project_dir == '/home/incode7/PycharmProjects/incodeParsing':
        project_dir = '/home/incode7/Desktop/testdir'
    list_to_output = list()

    rectifier = CSSRectifier()
    rectifier.do_rectifier(project_dir)

    if report:
        rectifier.do_report()
    else:
        for css_selector in rectifier.css_selectors:
            if not css_selector.usage:
                print(css_selector)
    print("--- %s seconds ---" % (time.time() - start_time))
