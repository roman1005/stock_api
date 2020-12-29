'''
from apscheduler.schedulers.background import BackgroundScheduler
from .latest_news import get_latest_articles
from .sources import sources

job_interval=30

def save_latest_articles(category):

    get_latest_articles(category)

def start():

    scheduler = BackgroundScheduler()

    for website in sources['crypto']:
        scheduler.add_job(save_latest_articles, "interval", [website], seconds=job_interval)

    scheduler.start()
'''
