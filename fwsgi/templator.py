from jinja2 import Template, Environment, FileSystemLoader


# def render(tempate_name, **kwargs):
#     with open(tempate_name, 'r', encoding='utf-8') as f:
#         tempate = Template(f.read())
#
#     return tempate.render(**kwargs)


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)

if __name__ == '__main__':
    # output_test = render('templates/index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    output_test = render('contacts.html', title='Контакты')
    print(output_test)
