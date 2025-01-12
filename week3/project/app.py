from jinja2 import Template

table_data = [
    {"id": 1, "first": "Mark", "last": "Otto", "handle": "@mdo"},
    {"id": 2, "first": "Jacob", "last": "Thornton", "handle": "@fat"},
    {"id": 3, "first": "Larry the Bird", "last": "", "handle": "@twitter"},
]


def main():
    template_file = open(r"week3\project\me.html.jinja2")
    TEMPLATE = template_file.read()
    template_file.close()
    
    template = Template(TEMPLATE)
    content = template.render(data = table_data)
    
    my_html_file = open("week3/project/me.html",'w')
    my_html_file.write(content)
    my_html_file.close()
    

if __name__=="__main__":
    main()