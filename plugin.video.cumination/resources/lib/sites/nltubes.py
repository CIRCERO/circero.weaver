"""
    Cumination
    Copyright (C) 2015 Whitecream

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('poldertube', '[COLOR yellow]Poldertube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]', 'https://www.poldertube.nl/', 'poldertube.gif', 'poldertube')
site2 = AdultSite('sextube', '[COLOR yellow]Sextube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]', 'https://www.sextube.nl/', 'sextube.gif', 'sextube')
site3 = AdultSite('12milf', '[COLOR yellow]12Milf[/COLOR] [COLOR orange](Dutch)[/COLOR]', 'https://www.12milf.com/nl/', '12milf.gif', '12milf')
site4 = AdultSite('porntubenl', '[COLOR yellow]PornTube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]', 'https://www.porntube.nl/', 'porntubenl.gif', 'porntubenl')


def getBaselink(url):
    if 'poldertube.nl' in url:
        siteurl = 'https://www.poldertube.nl/'
    elif 'sextube.nl' in url:
        siteurl = 'https://www.sextube.nl/'
    elif '12milf.com' in url:
        siteurl = 'https://www.12milf.com/nl/'
    elif 'porntube.nl' in url:
        siteurl = 'https://www.porntube.nl/'
    return siteurl


@site.register(default_mode=True)
@site2.register(default_mode=True)
@site3.register(default_mode=True)
@site4.register(default_mode=True)
def NLTUBES(url):
    siteurl = getBaselink(url)
    site.add_dir('[COLOR yellow]Categories[/COLOR]', siteurl + ('categories/' if '/us/' in siteurl else 'categorieen/'), 'NLCAT', site.img_cat)
    site.add_dir('[COLOR yellow]Search[/COLOR]', siteurl + '?s=', 'NLSEARCH', site.img_search)
    NLVIDEOLIST(url + '?filter=latest')


@site.register()
def NLVIDEOLIST(url):
    siteurl = getBaselink(url)
    link = utils.getHtml(url, '')
    if "0 video found" in link or "Nothing found" in link:
        return
    match = re.compile(r'<article(.+?)href="([^"]+)"\s*title="([^"]+)".+?src="([^"]+)(.+?)tion"\D*?([\d:]+)', re.DOTALL | re.IGNORECASE).findall(link)
    for hd1, surl, name, img, hd2, duration in match:
        surl = surl if surl.startswith('http') else siteurl + surl
        if 'tag-hd-porno' in hd1 or '>HD<' in hd2:
            hd = "HD"
        else:
            hd = ""
        name = utils.cleantext(name)
        site.add_download_link(name, surl, 'NLPLAYVID', img, name, duration=duration, quality=hd)
    nextp = re.compile(r'''class="pagination.+?class="current".+?href=['"]([^"']+)''', re.DOTALL | re.IGNORECASE).search(link)
    if nextp:
        nextp = nextp.group(1)
        page_nr = re.findall(r'\d+', nextp)[-1]
        nextp = nextp if nextp.startswith('http') else siteurl + nextp
        site.add_dir('Next Page (' + page_nr + ')', nextp, 'NLVIDEOLIST', site.img_next)
    utils.eod()


@site.register()
def NLPLAYVID(url, name, download=None):
    siteurl = getBaselink(url)
    vp = utils.VideoPlayer(name, download)
    vp.progress.update(25, "[CR]Loading video page[CR]")
    hdr = utils.base_hdrs
    hdr['Cookie'] = 'pageviews=1; postviews=1'
    videopage = utils.getHtml(url, siteurl, hdr)
    videourl = re.compile(r'contentURL"\s*content="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videourl[0] + '|Referer={}'.format(siteurl)
    vp.play_from_direct_link(videourl)


@site.register()
def NLSEARCH(url, keyword=None):
    searchUrl = url
    if not keyword:
        site.search_dir(url, 'NLSEARCH')
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        NLVIDEOLIST(searchUrl)


@site.register()
def NLCAT(url):
    siteurl = getBaselink(url)
    link = utils.getHtml(url, '')
    tags = re.compile(r'<article.+?href="([^"]+).+?src="([^"]+).+?le">([^<]+)', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catimg, catname in tags:
        catimg = catimg if catimg.startswith('http') else siteurl + catimg
        site.add_dir(catname, caturl, 'NLVIDEOLIST', catimg)
    utils.eod()
