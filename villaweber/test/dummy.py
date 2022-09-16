from helper.init_db import CategoryTemplateTable


def create_dummy_data():
    cat_template = CategoryTemplateTable()
    cat_template.category = 'Licht'
    cat_template.template = 'light'

if __name__ == '__main__':
    create_dummy_data()