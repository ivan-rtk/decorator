import json
import hashlib
from decorator import get_log


class CountryLinks:
    WIKI_URL = 'https://en.wikipedia.org/wiki/'

    def __init__(self, countrys_file_path: str):
        with open(countrys_file_path, encoding='utf8') as file:
            countries_data = json.load(file)
            country_names = (country['name']['common'] for country in countries_data)
            self.country_names_iter = iter(country_names)

    def __iter__(self):
        return self

    @get_log
    def make_link(self, country_name: str):
        country_name = country_name.replace(' ', '_')
        return f'{self.WIKI_URL}{country_name}'

    def __next__(self):
        country_name = next(self.country_names_iter)  # получаем имя страны.
        return f'{country_name} - {self.make_link(country_name)}'


@get_log
def get_hash(path: str):
    with open(path, 'rb') as file:
        for line in file:
            yield hashlib.md5(line).hexdigest()


if __name__ == '__main__':
    with open('country_names.txt', 'w', encoding='utf8') as country_names_file:
        for country_link in CountryLinks('countries.json'):  # итерируемя по ссылкам
            country_names_file.write(f'{country_link}\n')  # и пишем их в файл

    for hash_string in get_hash('country_names.txt'):
        print(hash_string)
