from celery import shared_task


@shared_task
def parser_msk(page=226, output_file='urls_moscow.txt'):
    from ..parser.URL_parse import url_parse
    from ..parser.producersMO_parse import producers_parse
    url_parse(page, output_file)
    producers_parse(output_file)
