import os
from datetime import timedelta, date
from scripts.sources import sources as ext_srcs
import feedparser
import requests
import json


def daterange(start_date, end_date):
    result = []
    for n in range(int((end_date - start_date).days-1)):
        result.append([start_date + timedelta(n), start_date + timedelta(n+1)])

    return result


def collect_sources(start_date, end_date):

    no_data = 0
    result = {'feed': 0, 'rss': 0, 'feed.xml': 0}
    bad_websites = []
    good_websites = []

    for date_pair in daterange(start_date, end_date):
        data = requests.get(
        'https://newsapi.org/v2/everything?apiKey=81faa42866a04f628022b1cc2ca10f8c&q=stock&sortBy=publishedAt&pagesize=100&from=' + date_pair[0].strftime("%Y-%m-%d") + '&to=' + date_pair[0].strftime("%Y-%m-%d"))
        parsed_json = (json.loads(data.content))
        articles = parsed_json['articles']

        for article in articles:
            article_parts = article['url'].split('/')
            website = article_parts[0] + '//' + article_parts[2]
            if not website in bad_websites:
                try:
                    entries_rss = feedparser.parse(website + '/rss').entries

                    if entries_rss:
                        print(website+'/rss')
                        result['rss'] += 1
                        if not website + '/rssi' in good_websites:
                            good_websites.append(website + '/rss')
                    else:
                        entries_feed = feedparser.parse(website + '/feed').entries
                        if entries_feed:
                            print(website + '/feed')
                            result['feed'] += 1
                            if not website + '/feed' in good_websites:
                                good_websites.append(website + '/feed')
                        else:
                            entries_feed_xml = feedparser.parse(website + '/feed.xml').entries
                            if entries_feed_xml:
                                print(website + '/feed.xml')
                                result['feed.xml'] += 1
                                if not website + '/feed.xml' in good_websites:
                                    good_websites.append(website + '/feed.xml')
                            else:
                                print("No data")
                                no_data += 1
                                if not website in bad_websites:
                                    bad_websites.append(website)
                except:
                    pass

    print("No data number of sites" + str(no_data))
    print(result)
    print(good_websites)
    print(len(good_websites))
    print(bad_websites)
    print(len(bad_websites))

'''
sources = ['https://www.wikihow.com/feed.xml', 'https://www.fool.com.au/rss', 'https://jp.techcrunch.com/rss', 'https://www.musicbusinessworldwide.com/rss', 'https://techcrunch.com/rss', 'https://www.stuff.co.nz/rss', 'https://variety.com/rss', 'https://uxdesign.cc/rss', 'https://www.shtfplan.com/rss', 'https://upstract.com/feed', 'https://www.ozbargain.com.au/feed', 'https://news.yahoo.com/rss', 'https://www.valuewalk.com/rss', 'http://techcrunch.com/rss', 'https://www.startribune.com/rss', 'https://www.independent.co.uk/rss', 'https://www.bloombergquint.com/feed', 'https://dailycaller.com/feed', 'https://www.gizmodo.com.au/rss', 'https://www.androidheadlines.com/rss', 'https://www.nybooks.com/rss', 'https://moz.com/feed', 'https://robbreport.com/rss', 'https://blog.adobe.com/feed', 'https://www.totaltele.com/rss', 'https://seekingalpha.com/feed', 'https://www.japantimes.co.jp/rss', 'https://www.dealabs.com/rss', 'https://www.businessinsider.com/rss', 'https://foreignpolicy.com/rss', 'https://www.digitaltrends.com/rss', 'https://kotaku.com/rss', 'https://www.kotaku.com.au/rss', 'https://www.techradar.com/rss', 'https://eundertake.com/rss', 'http://joefavorito.com/rss', 'https://www.voanews.com/feed', 'https://www.motortrend.com/rss', 'https://siliconangle.com/rss', 'https://chinadigitaltimes.net/rss', 'https://www.lifehacker.com.au/rss', 'https://www.hotukdeals.com/rss', 'https://freebeacon.com/rss', 'https://www.disneyfoodblog.com/rss', 'https://indianexpress.com/rss', 'https://wherethemoneyis.libsyn.com/rss', 'https://hip2save.com/rss', 'https://uproxx.com/rss', 'https://major.io/feed', 'https://nationalinterest.org/feed', 'https://monevator.com/rss', 'https://bringatrailer.com/rss', 'https://www.mactrast.com/rss', 'https://www.carscoops.com/rss', 'https://9to5mac.com/rss', 'https://themomedit.com/rss', 'https://kvoa.com/rss', 'https://www.nbcnews.com/rss', 'https://nypost.com/rss', 'https://awealthofcommonsense.com/rss', 'https://www.dailyreckoning.com.au/rss', 'https://time.com/rss', 'https://katalogpromosi.com/rss', 'https://draftwire.usatoday.com/rss', 'https://www.enterpreneurlifestyle.com/rss', 'https://www.dailysignal.com/rss', 'https://dailyreckoning.com/rss', 'https://www.juststartinvesting.com/rss', 'https://wattsupwiththat.com/rss', 'https://elchapuzasinformatico.com/rss', 'https://www.nrc.nl/feed', 'https://queenbeetoday.com/rss', 'https://www.notimeforflashcards.com/rss', 'https://qz.com/feed', 'https://platum.kr/rss', 'https://justcreative.com/rss', 'https://www.lesswrong.com/feed.xml', 'https://tinasendin.com/rss', 'https://www.singletracks.com/rss', 'https://www.investmentwatchblog.com/rss', 'https://www.motherjones.com/rss', 'https://bitrebels.com/rss', 'http://thegrio.com/rss', 'https://www.foxnews.com/rss', 'https://www.mcnews.com.au/rss', 'https://ca.sports.yahoo.com/rss', 'https://sports.yahoo.com/rss', 'https://www.iphoneincanada.ca/rss', 'https://www.breitbart.com/rss', 'https://news.google.com/rss', 'https://www.omgubuntu.co.uk/rss', 'https://finance.technews.tw/rss', 'https://www.redrc.net/rss', 'https://www.afaqs.com/feed', 'https://thechive.com/rss', 'https://blogs.sap.com/rss', 'https://decryptmedia.com/rss', 'https://www.southernsavers.com/rss', 'https://autoblog.com.ar/rss', 'https://decider.com/rss', 'https://www.20minutos.es/rss', 'https://www.newsweek.com/rss', 'https://www.visordown.com/rss', 'https://www.vice.com/rss', 'https://ottawacitizen.com/rss', 'https://bitcoinist.com/rss', 'https://www.ai-cio.com/rss', 'https://www.nintendolife.com/rss', 'https://talkingpointsmemo.com/feed', 'https://www.popularwoodworking.com/rss', 'https://ruhlman.com/rss', 'https://www.bookforum.com/rss']
print(len(sources))

unique_sources = []
for source in sources:
    if not (source in unique_sources):
        unique_sources.append(source)

print(len(unique_sources))
print(unique_sources)
'''
'''
for i, source in enumerate(ext_srcs):
    feed = feedparser.parse(source+'rss').entries
    if feed != []:
        ext_srcs[i] = source + 'rss'
    feed = feedparser.parse(source + 'feed').entries
    if feed != []:
        ext_srcs[i] = source + 'feed'
    else:
        print(source)

print(ext_srcs)
'''
start_date = date(2021, 1, 29)
end_date = date(2021, 2, 9)

#collect_sources(start_date, end_date)


def make_unique(sources):
    print('Initial length of sources: {}'.format(len(sources)))
    unique_sources = []
    for source in sources:
        if not (source in unique_sources):
            unique_sources.append(source)
    print('Length after removing duplicates: {}'.format(len(unique_sources)))
    print(unique_sources)
    return unique_sources


def remove_already_found(sources):
    new_sources = []
    for source in sources:
        if not source in ext_srcs:
            new_sources.append(source)
    print(new_sources)
    return new_sources


def find_repeats(ext_srcs):
    dict = {}
    for source in ext_srcs:

        try:
            dict[os.path.dirname(source)] += 1

        except KeyError:
            dict[os.path.dirname(source)] = 1

    print({k:v for (k,v) in dict.items() if v > 1})

#find_repeats(ext_srcs)

def make_dict(sources):
    dict = {}
    for source in sources:
        dict[source.replace('www.', '').replace('.com', '').split('/')[2]] = os.path.dirname(source)
    print(dict)

print(len(ext_srcs))

new_sources = ['https://www.startribune.com/rss', 'https://www.ozbargain.com.au/feed', 'https://upstract.com/feed', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.businessinsider.com/rss', 'https://9to5mac.com/rss', 'https://www.fool.com.au/rss', 'https://www.independent.co.uk/rss', 'https://www.foxnews.com/rss', 'http://www.thewrap.com/rss', 'https://gizmodo.com/rss', 'https://www.tmz.com/rss', 'https://hip2save.com/rss', 'https://www.motorcycle.com/rss', 'https://techcrunch.com/rss', 'http://techcrunch.com/rss', 'https://gizmodo.com/rss', 'https://www.gizmodo.com.au/rss', 'https://www.lewrockwell.com/rss', 'https://dailycaller.com/feed', 'https://monevator.com/rss', 'https://www.wnd.com/rss', 'https://whistleblowersblog.org/rss', 'https://www.theepochtimes.com/rss', 'https://www.businessinsider.com/rss', 'https://deadline.com/rss', 'https://toolguyd.com/rss', 'https://www.rt.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.rt.com/rss', 'https://wgntv.com/rss', 'https://observador.pt/rss', 'https://www.fool.com.au/rss', 'https://www.hotukdeals.com/rss', 'https://www.nationalreview.com/rss', 'https://www.siliconera.com/rss', 'https://www.tmz.com/rss', 'https://www.bloombergquint.com/feed', 'https://www.balloon-juice.com/rss', 'https://www.fool.com.au/rss', 'https://themomedit.com/rss', 'https://www.wnd.com/rss', 'https://www.fool.com.au/rss', 'https://www.businessinsider.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.wnd.com/rss', 'https://www.voanews.com/feed', 'https://hip2save.com/rss', 'https://www.dealabs.com/rss', 'https://www.wnd.com/rss', 'https://invezz.com/rss', 'https://news.yahoo.com/rss', 'https://www.fool.com.au/rss', 'https://nypost.com/rss', 'https://www.wkbn.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.hotukdeals.com/rss', 'https://www.fool.com.au/rss', 'https://www.rt.com/rss', 'https://www.thetruthaboutguns.com/rss', 'https://hip2save.com/rss', 'https://www.fool.com.au/rss', 'https://news.google.com/rss', 'https://seekingalpha.com/feed', 'https://www.fxstreet.com/rss', 'https://localnews8.com/rss', 'https://www.kotaku.com.au/rss', 'https://www.fool.com.au/rss', 'https://cointelegraph.com/rss', 'https://www.commonsensewithmoney.com/rss', 'https://www.fool.com.au/rss', 'https://trendfollowingradio.com/rss', 'https://www.fool.com.au/rss', 'https://www.artforum.com/rss', 'https://fstoppers.com/rss', 'https://www.investmentwatchblog.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://creditwritedowns.com/rss', 'https://pro.creditwritedowns.com/feed', 'https://www.fool.com.au/rss', 'https://www.marketingguerrilla.es/rss', 'https://iowapreps.rivals.com/feed', 'https://www.nbcnews.com/rss', 'https://hip2save.com/rss', 'https://www.fool.com.au/rss', 'http://www.rlslog.net/rss', 'https://www.kotaku.com.au/rss', 'https://nypost.com/rss', 'https://www.foxnews.com/rss', 'https://www.carscoops.com/rss', 'https://www.artforum.com/rss', 'https://news.yahoo.com/rss', 'https://www.nbcnews.com/rss', 'https://www.shtfplan.com/rss', 'https://www.datacenterknowledge.com/feed', 'https://sports.yahoo.com/rss', 'https://www.fool.com.au/rss', 'https://www.gizmodo.com.au/rss', 'https://www.lifehacker.com.au/rss', 'https://www.bestadsontv.com/feed', 'https://nypost.com/rss', 'http://imissgrantland.com/rss', 'https://hip2save.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.buzzfeed.com/feed.xml', 'https://www.kotaku.com.au/rss', 'https://nationalinterest.org/feed', 'https://kotaku.com/rss', 'https://nypost.com/rss', 'https://siliconangle.com/rss', 'https://www.bostonherald.com/rss', 'https://www.geekwire.com/rss', 'https://observador.pt/rss', 'https://www.dealabs.com/rss', 'https://www.fool.com.au/rss', 'https://om.co/rss', 'https://www.fool.com.au/rss', 'https://news.yahoo.com/rss', 'https://www.independent.co.uk/rss', 'https://therealdeal.com/rss', 'https://wccftech.com/rss', 'http://wtop.com/rss', 'https://www.androidpolice.com/rss', 'https://www.xda-developers.com/rss', 'https://effortlessgent.com/rss', 'https://www.shtfplan.com/rss', 'https://www.dealabs.com/rss', 'https://techcrunch.com/rss', 'https://www.totaltele.com/rss', 'https://www.breitbart.com/rss', 'https://www.jamierubin.net/rss', 'https://www.lifehacker.com.au/rss', 'https://www.lifehacker.com.au/rss', 'https://www.digitaltrends.com/rss', 'https://www.startribune.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.fool.com.au/rss', 'https://www.hotukdeals.com/rss', 'https://www.fool.com.au/rss', 'https://hip2save.com/rss', 'https://rocketswire.usatoday.com/rss', 'https://nypost.com/rss', 'https://www.hotukdeals.com/rss', 'https://hip2save.com/rss', 'https://blog.rstudio.com/feed', 'https://u-note.me/feed', 'https://siliconangle.com/rss', 'http://www.adexchanger.com/rss', 'https://www.wnd.com/rss', 'https://www.lifehacker.com.au/rss', 'https://www.hotukdeals.com/rss', 'https://www.geekwire.com/rss', 'https://neighborwebsj.com/rss', 'https://www.hotukdeals.com/rss', 'https://hip2save.com/rss', 'https://www.fark.com/rss', 'https://www.nbcnews.com/rss', 'https://www.techmeme.com/feed.xml', 'https://news.yahoo.com/rss', 'https://financialpost.com/rss', 'https://survivalblog.com/rss', 'https://www.fool.com.au/rss', 'https://ca.sports.yahoo.com/rss', 'https://ca.sports.yahoo.com/rss', 'https://ca.sports.yahoo.com/rss', 'https://www.fool.com.au/rss', 'https://ca.news.yahoo.com/rss', 'https://dlisted.com/rss', 'https://mediagazer.com/feed.xml', 'https://hip2save.com/rss', 'https://wccftech.com/rss', 'https://techcrunch.com/rss', 'https://www.infomoney.com.br/rss', 'https://www.startribune.com/rss', 'https://www.newsweek.com/rss', 'https://www.fool.com.au/rss', 'https://hip2save.com/rss', 'https://www.fool.com.au/rss', 'https://www.stuff.co.nz/rss', 'https://www.rt.com/rss', 'https://www.fool.com.au/rss', 'https://www.thebrewsite.com/rss', 'https://affordanything.com/rss', 'https://www.dailysignal.com/rss', 'https://news.yahoo.com/rss', 'https://monevator.com/rss', 'https://www.businessinsider.com/rss', 'https://www.fool.com.au/rss', 'https://www.thephoblographer.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.fool.com.au/rss', 'https://bringatrailer.com/rss', 'https://indianexpress.com/rss', 'https://www.bigrapidsnews.com/feed', 'http://grist.org/rss', 'https://www.fool.com.au/rss', 'https://vancouversun.com/rss', 'https://hip2save.com/rss', 'https://www.hotukdeals.com/rss', 'https://cleantechnica.com/rss', 'https://www.deccanchronicle.com/rss', 'https://www.fool.com.au/rss', 'https://tvline.com/rss', 'https://hip2save.com/rss', 'https://comicbook.com/rss', 'https://www.somosxbox.com/rss', 'https://hip2save.com/rss', 'https://www.addictivetips.com/rss', 'https://www.fool.com.au/rss', 'https://www.salon.com/feed', 'https://www.fool.com.au/rss', 'https://www.diyphotography.net/rss', 'https://www.bmwblog.com/rss', 'https://www.fool.com.au/rss', 'https://www.thetruthaboutguns.com/rss', 'https://www.fool.com.au/rss', 'https://www.bostonherald.com/rss', 'https://www.fool.com.au/rss', 'https://www.dealabs.com/rss', 'https://eliterate.us/rss', 'https://www.fool.com.au/rss', 'http://thegrio.com/rss', 'https://www.fool.com.au/rss', 'https://venturebeat.com/rss', 'https://news.yahoo.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.wane.com/rss', 'https://www.fool.com.au/rss', 'https://nypost.com/rss', 'https://hip2save.com/rss', 'https://www.fool.com.au/rss', 'https://indianexpress.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.stuff.co.nz/rss', 'https://www.lifehacker.com.au/rss', 'https://www.indiewire.com/rss', 'https://www.mlbtraderumors.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://thesportsdaily.com/rss', 'https://www.fool.com.au/rss', 'https://www.infomoney.com.br/rss', 'https://www.fool.com.au/rss', 'https://www.billboard.com/rss', 'https://kotaku.com/rss', 'https://www.kotaku.com.au/rss', 'https://www.fool.com.au/rss', 'https://www.thedailybeast.com/rss', 'https://www.newsweek.com/rss', 'https://www.fool.com.au/rss', 'https://www.dealabs.com/rss', 'https://www.fastcompany.com/rss', 'https://www.fastcompany.com/rss', 'https://www.fool.com.au/rss', 'https://www.fool.com.au/rss', 'https://hip2save.com/rss', 'https://www.lawyersgunsmoneyblog.com/rss', 'https://www.lifehacker.com.au/rss', 'https://offgridsurvival.com/rss', 'https://theradavist.com/rss', 'https://www.fool.com.au/rss', 'https://www.insider.com/rss', 'https://allears.net/rss', 'https://www.carscoops.com/rss', 'https://www.fool.com.au/rss']
#unique_sources = make_unique(new_sources)

#uniqe_new = remove_already_found(unique_sources)
#make_dict(uniqe_new)

dict = {}

for source in ext_srcs:
    print(source)
    try:
        dict[feedparser.parse(source)['feed']['language']] = 1
    except KeyError:
        pass

print(dict)
#make_dict(ext_srcs)