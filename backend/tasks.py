from celery import shared_task
from ..parser.URL_parse import url_parse
from ..parser.producersMO_parse import producers_parse


@shared_task
def parser_msk(page, output_file, producers_txt):
    url_parse(page, output_file)
    producers_parse(producers_txt)
