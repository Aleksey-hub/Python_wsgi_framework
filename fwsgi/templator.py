from jinja2 import Template


def render(tempate_name, **kwargs):
    with open(tempate_name, 'r', encoding='utf-8') as f:
        tempate = Template(f.read())

    return tempate.render(**kwargs)


if __name__ == '__main__':
    # output_test = render('templates/index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    output_test = render('templates/index.html')
    print(output_test)
