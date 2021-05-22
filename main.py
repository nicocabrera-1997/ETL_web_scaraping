import argparse
import logging                              # loggin permite  enviar mensajes por consola de manera automatica
logging.basicConfig(level=logging.INFO)     # asignandole un nivel (level) de importancia a cada tipo de mensaje
import re								

from requests.exceptions import HTTPError 
from urllib3.exceptions import MaxRetryError
				
import news_page_objects as news
from common import config


logger = logging.getLogger(__name__) 		#retorna una instancia que nos servira para indicar que los mensajes
											#estan siendo enviados desde este module name en particular.
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    logging.info('Finding links in homepage...')
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('Article fetched')
            articles.append(article)
            print(article.title)

    print(len(articles))

    
def _fetch_article(news_site_uid, host, link):
    logger.info('Start fetching article at {}'.format(link))

    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fechting the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid Article. There is no body')
        return None
    
    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)
