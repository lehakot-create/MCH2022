from celery import shared_task
from ..prj.celery import app


@shared_task
def parser_msk(page=226, output_file='urls_moscow.txt'):
    from ..parser.URL_parse import url_parse
    from ..parser.producersMO_parse import producers_parse
    url_parse(page, output_file)
    producers_parse(output_file)


@app.task
def start_fill_coords():
    print('hello/ i am start_fill_coords function!')
    return 'hello/ i am returned!'
