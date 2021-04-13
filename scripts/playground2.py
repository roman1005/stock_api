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


def collect_sources(start_date, end_date, keyword):

    no_data = 0
    result = {'feed': 0, 'rss': 0, 'feed.xml': 0}
    bad_websites = []
    good_websites = []

    for date_pair in daterange(start_date, end_date):
        data = requests.get(
        'https://newsapi.org/v2/everything?apiKey=81faa42866a04f628022b1cc2ca10f8c&q='+keyword+'&sortBy=publishedAt&pagesize=100&from=' + date_pair[0].strftime("%Y-%m-%d") + '&to=' + date_pair[0].strftime("%Y-%m-%d"))
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

#collect_sources(start_date, end_date, 'physics')


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

new_sources = ['https://www.gamedev.net/rss', 'https://abc17news.com/rss', 'https://localnews8.com/rss', 'http://missionlocal.org/rss', 'http://www.justjared.com/feed', 'https://www.theblaze.com/rss', 'https://rjlipton.wordpress.com/rss', 'https://actualidad.rt.com/rss', 'https://www.princeton.edu/feed', 'https://arstechnica.com/rss', 'https://uk.pcmag.com/rss', 'https://toucharcade.com/rss', 'https://www.protothema.gr/rss', 'https://www.teenvogue.com/rss', 'https://denver.cbslocal.com/rss', 'https://uploadvr.com/rss', 'https://4gravitons.com/rss', 'https://www.androidpolice.com/rss', 'https://www.androidpolice.com/rss', 'https://www.sciencedaily.com/rss', 'https://lenta.ru/rss', 'https://www.factmag.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.triplepundit.com/rss', 'https://www.gamedev.net/rss', 'https://www.gamedev.net/rss', 'https://www.futurity.org/rss', 'https://www.wallpaper.com/rss', 'https://www.independent.co.uk/rss', 'https://bikerumor.com/rss', 'https://kinjadeals.theinventory.com/rss', 'https://www.pv-tech.org/rss', 'https://antyweb.pl/rss', 'https://space.blog.gov.uk/feed', 'https://www.nme.com/rss', 'https://www.kdnuggets.com/rss', 'https://www.ozbargain.com.au/feed', 'http://www.crossingwallstreet.com/rss', 'https://www.androidcentral.com/feed', 'https://securityintelligence.com/rss', 'https://www.solidsmack.com/rss', 'https://www.lesswrong.com/feed.xml', 'https://www.slashfilm.com/rss', 'https://wattsupwiththat.com/rss', 'https://variety.com/rss', 'https://www.indiewire.com/rss', 'https://www.independent.co.uk/rss', 'https://pagesix.com/rss', 'https://wccftech.com/rss', 'https://www.wimp.com/rss', 'https://www.vanguardngr.com/rss', 'https://kinjadeals.theinventory.com/rss', 'https://uploadvr.com/rss', 'https://www.activistpost.com/rss', 'https://fee.org/feed', 'https://hackaday.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.gizmodo.com.au/rss', 'https://gizmodo.com/rss', 'https://nplus1.ru/rss', 'https://www.bloombergquint.com/feed', 'https://www.businessinsider.com/rss', 'https://www.wykop.pl/rss', 'https://www.techradar.com/rss', 'https://science.thewire.in/rss', 'https://www.japantimes.co.jp/rss', 'https://indianexpress.com/rss', 'https://indianexpress.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.hotukdeals.com/rss', 'https://dcbaseballhistory.com/rss', 'http://energyskeptic.com/rss', 'https://cleantechnica.com/rss', 'https://www.stereogum.com/rss', 'https://www.addictivetips.com/rss', 'https://www.gamedev.net/rss', 'https://www.digitaltrends.com/rss', 'https://venturebeat.com/rss', 'https://toolguyd.com/rss', 'https://www.androidauthority.com/rss', 'https://kinjadeals.theinventory.com/rss', 'http://www.the-sun.com/rss', 'https://scienceblog.com/rss', 'https://scienceblog.com/rss', 'https://www.businessinsider.com/rss', 'https://venturebeat.com/rss', 'https://www.elitedaily.com/rss', 'https://arstechnica.com/rss', 'https://www.gamedev.net/rss', 'https://bengreenfieldfitness.com/rss', 'https://mysteriousuniverse.org/rss', 'https://www.thehealthsite.com/rss', 'https://www.fark.com/rss', 'https://sports.yahoo.com/rss', 'https://habr.com/rss', 'https://www.digitaltrends.com/rss', 'https://thonyc.wordpress.com/rss', 'http://clarkesworldmagazine.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.universetoday.com/rss', 'https://arstechnica.com/rss', 'https://insidethemagic.net/rss', 'https://venturebeat.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://freethoughtblogs.com/rss', 'https://geektyrant.com/rss', 'https://freethoughtblogs.com/rss', 'https://ca.sports.yahoo.com/rss', 'https://fstoppers.com/rss', 'https://lesterbanks.com/rss', 'https://americansuburbx.com/rss', 'https://blog.argoproj.io/rss', 'https://www.leadingagile.com/rss', 'https://variety.com/rss', 'https://www.techradar.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.fairobserver.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://experimentalfrontiers.scienceblog.com/rss', 'https://lenta.ru/rss', 'https://www.independent.co.uk/rss', 'https://www.lifehack.org/rss', 'https://www.artnews.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.ilgiornale.it/feed.xml', 'https://blog.playstation.com/rss', 'https://earlyretirementextreme.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.slashgear.com/rss', 'https://www.syfy.com/feed.xml', 'http://www.rlslog.net/rss', 'https://www.indiewire.com/rss', 'https://www.rt.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://mymodernmet.com/rss', 'https://variety.com/rss', 'https://www.digitaltrends.com/rss', 'https://www.stuff.co.nz/rss', 'https://www.lifehacker.com.au/rss', 'https://survivalblog.com/rss', 'https://www.playstationlifestyle.net/rss', 'https://foreignpolicy.com/rss', 'https://golfweek.usatoday.com/rss', 'http://www.sci-news.com/rss', 'https://www.pocketgamer.com/rss', 'https://www.gematsu.com/rss', 'http://hiphopwired.com/rss', 'https://www.20minutos.es/rss', 'https://gizmodo.com/rss', 'https://www.universetoday.com/rss', 'https://nationalinterest.org/feed', 'https://bloody-disgusting.com/rss', 'https://boingboing.net/rss', 'https://nerdist.com/rss', 'https://www.kdnuggets.com/rss', 'https://brobible.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://matadornetwork.com/rss', 'http://www.searchenginewatch.com/rss', 'https://scienceblog.com/rss', 'https://in.ign.com/rss', 'https://petapixel.com/rss', 'https://news.avclub.com/rss', 'https://hollywoodlife.com/rss', 'https://www.independent.co.uk/rss', 'https://www.startribune.com/rss', 'https://aws.amazon.com/rss', 'https://www.neatorama.com/feed', 'https://www.sciencedaily.com/rss', 'https://habr.com/rss', 'https://www.nintendolife.com/rss', 'https://www.independent.co.uk/rss', 'https://www.centauri-dreams.org/rss', 'http://en.protothema.gr/rss', 'https://marker.medium.com/rss', 'https://www.vice.com/rss', 'https://appadvice.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://skepticalscience.com/feed.xml', 'https://www.studyfinds.org/rss', 'https://www.independent.co.uk/rss', 'https://www.techradar.com/rss', 'https://news.harvard.edu/rss', 'https://www.comicsbeat.com/rss', 'https://www.newsweek.com/rss', 'https://venturebeat.com/rss', 'https://winteriscoming.net/rss', 'https://thenextweb.com/rss', 'https://indianexpress.com/rss', 'https://www.hotukdeals.com/rss', 'https://scottlocklin.wordpress.com/rss', 'https://gizmodo.uol.com.br/rss', 'https://www.stuff.co.nz/rss', 'https://blogs.nasa.gov/rss', 'https://wattsupwiththat.com/rss', 'https://incrediblethings.com/rss', 'https://pjmedia.com/rss', 'https://www.playstationlifestyle.net/rss', 'https://www.futurity.org/rss', 'http://asymptotia.com/rss', 'https://www.universetoday.com/rss', 'https://www.universetoday.com/rss', 'https://jalopnik.com/rss', 'https://wkzo.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'http://rlsbb.ru/rss', 'https://www.hotukdeals.com/rss', 'https://financialpost.com/rss', 'https://www.archdaily.com/rss', 'https://www.androidauthority.com/rss', 'https://www.independent.co.uk/rss', 'https://www.excal.on.ca/rss', 'https://deadline.com/rss', 'https://www.newsweek.com/rss', 'https://www.pocketgamer.com/rss', 'https://theawesomer.com/rss', 'https://machinelearningmastery.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://sciencebasedmedicine.org/rss', 'https://venturebeat.com/rss', 'https://www.extremetech.com/rss', 'https://thenextweb.com/rss', 'https://earther.gizmodo.com/rss', 'https://www.gizmodo.com.au/rss', 'https://www.sciencedaily.com/rss', 'https://aws.amazon.com/rss', 'https://blogs.fangraphs.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.nintendolife.com/rss', 'https://plugins.jetbrains.com/rss', 'https://cleantechnica.com/rss', 'https://www.nintendolife.com/rss', 'https://wccftech.com/rss', 'https://www.stereogum.com/rss', 'http://thegrio.com/rss', 'https://ca.news.yahoo.com/rss', 'https://www.anothermag.com/rss', 'https://www.rockpapershotgun.com/feed', 'https://www.sciencedaily.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.snopes.com/rss', 'https://www.digitaltrends.com/rss', 'https://www.valuewalk.com/rss', 'https://www.activistpost.com/rss', 'https://www.hotukdeals.com/rss', 'https://physicsworld.com/rss', 'https://www.mmorpg.com/rss', 'https://www.sciencedaily.com/rss', 'https://www.nbcnews.com/rss', 'https://news.yahoo.com/rss', 'https://singularityhub.com/rss', 'https://9to5mac.com/rss', 'https://blogs.nasa.gov/rss', 'https://www.stuff.co.nz/rss', 'https://www.sciencedaily.com/rss', 'https://news.xbox.com/rss', 'https://www.gizmodo.com.au/rss', 'https://gizmodo.com/rss', 'https://www.hotukdeals.com/rss', 'https://www.popularmechanics.com/rss', 'https://indianexpress.com/rss', 'https://wattsupwiththat.com/rss', 'https://cgpersia.com/rss', 'https://www.advocate-news.com/rss', 'https://www.fredzone.org/rss', 'https://eliterate.us/rss', 'https://www.nextbigfuture.com/rss', 'https://petapixel.com/rss', 'https://petapixel.com/rss', 'https://habr.com/rss', 'https://www.digitaltrends.com/rss', 'https://www.webpronews.com/rss', 'https://deeshaa.org/rss', 'https://www.rawstory.com/feed', 'https://www.universetoday.com/rss', 'https://www.denverpost.com/rss', 'https://www.n-tv.de/rss', 'https://freethoughtblogs.com/rss', 'https://iphone.giveawayoftheday.com/feed', 'https://news.yahoo.com/rss', 'https://www.sportskeeda.com/feed', 'https://www.pocketgamer.com/rss', 'https://www.nbcnews.com/rss', 'https://news.yahoo.com/rss', 'https://writings.stephenwolfram.com/rss', 'https://www.isna.ir/rss', 'https://bylinetimes.com/rss', 'https://www.protothema.gr/rss', 'https://www.fastcompany.com/rss', 'https://www.fastcompany.com/rss', 'https://www.fastcompany.com/rss', 'https://www.japantimes.co.jp/rss', 'https://researchbuzz.me/rss', 'https://www.chem-station.com/rss', 'http://www.rlslog.net/rss', 'https://ritholtz.com/rss', 'https://www.numerama.com/rss', 'https://www.brainpickings.org/rss', 'https://www.stuff.co.nz/rss', 'https://arstechnica.com/rss', 'https://www.salon.com/feed', 'https://arstechnica.com/rss', 'https://earthsky.org/rss', 'https://www.coolbusinessideas.com/rss', 'https://indianexpress.com/rss', 'https://9to5linux.com/rss', 'https://www.inc.com/rss', 'https://johncarlosbaez.wordpress.com/rss', 'https://dailygeekshow.com/rss', 'http://www.zemtv.co/rss']
unique_sources = make_unique(new_sources)

uniqe_new = remove_already_found(unique_sources)
make_dict(uniqe_new)

dict = {}

'''
for source in ext_srcs:
    print(source)
    try:
        dict[feedparser.parse(source)['feed']['language']] = 1
    except KeyError:
        pass

print(dict)
#make_dict(ext_srcs)
'''

print(len(uniqe_new))