import re
import os
import templanisator.abstract_template as abc_temp


class Jinja2TemplateProcessor(abc_temp.AbstractTemplate):
    def __init__(self):
        pass

    def do_template_processor(self, html_files):
        base_names = list()
        includes = dict()
        for html_file in html_files:
            for find in re.findall(u'{[^}]+}', html_file.string_version):
                if find.find('extends') > 0:
                    base_names.append(self.template_check_helper(find))
                elif find.find('include') > 0:
                    if html_file.name in includes.keys():
                        includes[html_file.name] = includes[html_file.name] \
                                                   + ', ' + self.template_check_helper(find)
                    else:
                        includes[html_file.name] = self.template_check_helper(find)

        for html_file in html_files:
            if html_file.name in base_names:
                html_file.base = True
            elif html_file.name in includes.keys():
                html_file.includes += includes[html_file.name]
        return self.template_build(html_files)

    def template_build(self, html_files):
        for html_file in html_files:
            if html_file.includes:
                for include_html_file in html_file.includes.split(', '):
                    for find in re.findall(u'{%.*?%}', html_file.string_version):
                        if find.find('include') > 0 and find.find(include_html_file) > 0:
                            html_file.string_version = html_file.string_version.replace(
                                find, self.get_file_to_include(
                                    html_files, include_html_file
                                ).string_version)
        return_list = list()
        for html_file in html_files:
            if html_file.base is False:
                if html_file.string_version.find('{% extends') >= 0:
                    base_file = self\
                        .get_file_to_include(html_files, os.path.basename(re.search(u'".*?"',
                                             re.search(u'{%.*?%}', html_file.string_version)
                                             .group()).group().replace('"', '')))
                    tmp = base_file.string_version
                    for find in re.findall(u'{%.*?%}', html_file.string_version):
                        if find.find('block') > 0 and find.find('endblock') == -1:
                            block_content = html_file.string_version[
                                  html_file.string_version.find(find)+len(find):
                                  html_file.string_version.find('{% endblock %}')
                                  ]
                            html_file.string_version = html_file.string_version.replace('{% endblock %}', '', 1)
                            tmp = tmp.replace(find, block_content)
                    html_file.string_version = tmp
                return_list.append(html_file)

        return return_list

    def get_file_to_include(self, html_files, name_of_file):
        for html_file in html_files:
            if html_file.path == name_of_file:
                return html_file
        raise FileExistsError

    def template_check_helper(self, find):
        try:
            base_name = re.search(u'".*?"', find).group().replace('"', '')
            return os.path.basename(base_name)
        except Exception as e:
            print(e)
            return
