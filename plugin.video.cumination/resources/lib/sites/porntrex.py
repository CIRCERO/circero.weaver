"""
    Cumination
    Copyright (C) 2018 Whitecream, holisticdioxide
    Copyright (C) 2020 Team Cumination

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
from six.moves import urllib_parse
from random import randint
import xbmc
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('porntrex', '[COLOR yellow]PornTrex[/COLOR]', 'https://www.porntrex.com/', 'pt.gif', 'porntrex')

getinput = utils._get_keyboard
ptlogged = 'true' in utils.addon.getSetting('ptlogged')
lengthChoices = {'All': '', '0-10 min': 'ten-min/', '10-30 min': 'ten-thirty-min/', '30+': 'thirty-all-min/'}
ptlength = utils.addon.getSetting("ptlength") or 'All'


@site.register(default_mode=True)
def PTMain():
    site.add_dir('[COLOR yellow]Length: [/COLOR] [COLOR orange]{0}[/COLOR]'.format(ptlength), '', 'PTLength', '', Folder=False)
    site.add_dir('[COLOR yellow]Categories[/COLOR]', '{0}categories/'.format(site.url), 'PTCat', site.img_cat)
    site.add_dir('[COLOR yellow]Search[/COLOR]', '{0}search/'.format(site.url), 'PTSearch', site.img_search)
    site.add_dir('[COLOR yellow]Models[/COLOR]', '', 'PTModelsAZ', site.img_cat)
    if not ptlogged:
        site.add_dir('[COLOR yellow]Login[/COLOR]', '', 'PTLogin', '', Folder=False)
    elif ptlogged:
        ptuser = utils.addon.getSetting('ptuser')
        site.add_dir('[COLOR yellow]Subscription videos[/COLOR]', '{0}my/subscriptions/?mode=async&function=get_block&block_id=list_videos_videos_from_my_subscriptions&sort_by=&from_my_subscriptions_videos=1'.format(site.url), 'PTList', page=1)
        site.add_dir('[COLOR yellow]Manage subscriptions[/COLOR]', '{0}my/subscriptions/?mode=async&function=get_block&block_id=list_members_subscriptions_my_subscriptions'.format(site.url), 'PTSubscriptions')
        site.add_dir('[COLOR violet]PT Favorites[/COLOR]', site.url + 'my/favourites/videos/?mode=async&function=get_block&block_id=list_videos_my_favourite_videos&fav_type=0&playlist_id=0&sort_by=&from_my_fav_videos=01', 'PTList', site.img_cat)
        site.add_dir('[COLOR yellow]Logout {0}[/COLOR]'.format(ptuser), '', 'PTLogin', '', Folder=False)
    ptlist = PTList('{0}latest-updates/{1}'.format(site.url, lengthChoices[ptlength]), 1)
    if not ptlist:
        utils.eod()


@site.register()
def PTLength():
    input = utils.selector('Select Length', lengthChoices.keys())
    if input:
        ptlength = input
        utils.addon.setSetting('ptlength', ptlength)
        xbmc.executebuiltin('Container.Refresh')


@site.register()
def PTList(url, page=1):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    listhtml = utils.getHtml(url, site.url, headers=hdr)
    if ptlogged and ('>Log in<' in listhtml):
        if PTLogin(False):
            hdr['Cookie'] = get_cookies()
            listhtml = utils.getHtml(url, site.url, headers=hdr)
        else:
            return None

    match = re.compile(r'class="video-.+?data-src="([^"]+)".+?/ul>(.+?)title.+?class="quality">([^<]+).+?clock-o"></i>\s*([^<]+).+?href="([^"]+).+?>([^<]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, private, hd, duration, videopage, name in match:
        name = utils.cleantext(name)
        if 'private' in private.lower():
            if not ptlogged:
                continue
            private = "[COLOR blue][PV][/COLOR] "
        else:
            private = ""
        if any(x in hd for x in ['720', '1080']):
            hd = "[COLOR orange]HD[/COLOR] "
        elif any(x in hd for x in ['1440', '2160']):
            hd = "[COLOR yellow]4K[/COLOR] "
        else:
            hd = ""
        name = "{0}{1}".format(private, name)  # , hd, duration)
        if img.startswith('//'):
            img = 'https:' + img
        elif img.startswith('/'):
            img = site.url[:-1] + img
        img = re.sub(r"http:", "https:", img)
        imgint = randint(1, 10)
        newimg = str(imgint) + '.jpg'
        img = img.replace('1.jpg', newimg)
        img = img.replace(' ', '%20')
        img = img + '|Referer=' + url
        contextmenu = []
        if ptlogged:
            contexturl = (utils.addon_sys
                          + "?mode=" + str('porntrex.PTCheck_pornstars')
                          + "&url=" + urllib_parse.quote_plus(videopage))
            contextmenu.append(('[COLOR crimson]Add pornstar to subscriptions[/COLOR]', 'RunPlugin(' + contexturl + ')'))
            if 'my_favourite_videos' in url:
                contextdel = (utils.addon_sys
                              + "?mode=" + str('porntrex.ContextMenu')
                              + "&url=" + urllib_parse.quote_plus(videopage)
                              + "&fav=del")
                contextmenu.append(('[COLOR violet]Delete from PT favorites[/COLOR]', 'RunPlugin(' + contextdel + ')'))
            else:
                contextadd = (utils.addon_sys
                              + "?mode=" + str('porntrex.ContextMenu')
                              + "&url=" + urllib_parse.quote_plus(videopage)
                              + "&fav=add")
                contextmenu.append(('[COLOR violet]Add to PT favorites[/COLOR]', 'RunPlugin(' + contextadd + ')'))

        contexturl = (utils.addon_sys
                      + "?mode=" + str('porntrex.PTCheck_tags')
                      + "&url=" + urllib_parse.quote_plus(videopage))
        contextmenu.append(('[COLOR crimson]Lookup tags[/COLOR]', 'RunPlugin(' + contexturl + ')'))
        site.add_download_link(name, videopage, 'PTPlayvid', img, name, contextm=contextmenu, duration=duration, quality=hd)
    if re.search('<li class="next">', listhtml, re.DOTALL | re.IGNORECASE):
        search = False
        if not page:
            page = 1
        npage = page + 1

        if url.endswith('/latest-updates/'):
            url += '{}/'.format(str(npage))
            search = True
        elif url.endswith('/{}/'.format(str(page))):
            url = url.replace('/{}/'.format(str(page)), '/{}/'.format(str(npage)))
            search = True
        elif 'list_videos_latest_videos_list' in url:
            url = url.replace('from=' + str(page), 'from=' + str(npage))
            search = True
        elif '/categories/' in url:
            url = url.replace('from=' + str(page), 'from=' + str(npage))
            search = True
        elif 'list_videos_common_videos_list_norm' in url:
            if len(match) == 120:
                url = url.replace('from4=' + str(page), 'from4=' + str(npage))
                search = True
        elif '/search/' in url:
            url = url.replace('from_videos=' + str(page), 'from_videos=' + str(npage)).replace('from_albums=' + str(page), 'from_albums=' + str(npage))
            search = True
        elif 'from_my_subscriptions_videos' in url:
            if len(match) == 10:
                url = url.replace('from_my_subscriptions_videos=' + str(page), 'from_my_subscriptions_videos=' + str(npage))
                search = True
        elif '/favourites/' in url:
            if 'from_my_fav_videos={0:02d}'.format(page) in url:
                url = url.replace('from_my_fav_videos={0:02d}'.format(page), 'from_my_fav_videos={0:02d}'.format(npage))
                search = True
            else:
                utils.kodilog(' favorites pagination error')
        else:
            url = url.replace('/' + str(page) + '/', '/' + str(npage) + '/')
            search = True

        lastp = re.compile(r'class="pagination".+data-max="(\d+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        if lastp:
            lastp = '/{}'.format(lastp[0])
            if npage > int(lastp[1:]):
                search = False
        else:
            lastp = ''

        if search:
            site.add_dir('Next Page (' + str(npage) + lastp + ')', url, 'PTList', site.img_next, npage)
    utils.eod()
    return True


@site.register()
def PTPlayvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download)
    vp.progress.update(25, "[CR]Loading video page[CR]")

    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    videopage = utils.getHtml(url, site.url, headers=hdr)

    if 'video_url_text' not in videopage:
        videourl = re.compile("video_url: '([^']+)'", re.DOTALL | re.IGNORECASE).search(videopage).group(1)
    else:
        sources = {}
        srcs = re.compile("video(?:_alt_|_)url(?:[0-9]|): '([^']+)'.*?video(?:_alt_|_)url(?:[0-9]|)_text: '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)
        for src, quality in srcs:
            sources[quality] = src
        videourl = utils.prefquality(sources, sort_by=lambda x: int(''.join([y for y in x if y.isdigit()])), reverse=True)
    if not videourl:
        vp.progress.close()
        return
    vp.progress.update(75, "[CR]Video found[CR]")
    vp.play_from_direct_link(videourl)


@site.register()
def PTCat(url):
    cathtml = utils.getHtml(url, '')
    cat_block = re.compile('<span class="icon type-video">(.*?)<div class="footer-margin">', re.DOTALL | re.IGNORECASE).search(cathtml).group(1)
    match = re.compile('<a class="item" href="([^"]+)" title="([^"]+)".*?src="([^"]+)".+?class="videos">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cat_block)
    for catpage, name, img, videos in sorted(match, key=lambda x: x[1]):
        if img.startswith('//'):
            img = 'https:' + img
        catpage += lengthChoices[ptlength]
        catpage += '?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=post_date&from=1'
        name = name + '[COLOR crimson] ' + videos + '[/COLOR]'
        site.add_dir(name, catpage, 'PTList', img, 1)
    utils.eod()


@site.register()
def PTSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        site.search_dir(url, 'PTSearch')
    else:
        searchUrl += keyword.replace(' ', '%20')
        searchUrl += '/latest-updates/'
        searchUrl += lengthChoices[ptlength]
        PTList(searchUrl, 1)


@site.register()
def PTLogin(logged=True):
    ptlogged = utils.addon.getSetting('ptlogged')
    if not logged:
        ptlogged = False
        utils.addon.setSetting('ptlogged', 'false')

    if not ptlogged or 'false' in ptlogged:
        ptuser = utils.addon.getSetting('ptuser') if utils.addon.getSetting('ptuser') else ''
        ptpass = utils.addon.getSetting('ptpass') if utils.addon.getSetting('ptpass') else ''
        if ptuser == '':
            ptuser = getinput(default=ptuser, heading='Input your Porntrex username')
            ptpass = getinput(default=ptpass, heading='Input your Porntrex password', hidden=True)

        loginurl = '{0}ajax-login/'.format(site.url)
        postRequest = {'action': 'login',
                       'email_link': '{0}email/'.format(site.url),
                       'format': 'json',
                       'mode': 'async',
                       'pass': ptpass,
                       'remember_me': '1',
                       'username': ptuser}
        response = utils._postHtml(loginurl, form_data=postRequest)
        if 'success' in response.lower():
            utils.addon.setSetting('ptlogged', 'true')
            utils.addon.setSetting('ptuser', ptuser)
            utils.addon.setSetting('ptpass', ptpass)
            success = True
        else:
            utils.notify('Failure logging in', 'Failure, please check your username or password')
            utils.addon.setSetting('ptuser', '')
            utils.addon.setSetting('ptpass', '')
            success = False
    elif ptlogged:
        clear = utils.selector('Clear stored user & password?', ['Yes', 'No'], reverse=True)
        if clear:
            if clear == 'Yes':
                utils.addon.setSetting('ptuser', '')
                utils.addon.setSetting('ptpass', '')
            utils.addon.setSetting('ptlogged', 'false')
            utils._getHtml(site.url + 'logout/')
    if logged:
        xbmc.executebuiltin('Container.Refresh')
    else:
        return success


@site.register()
def PTSubscriptions(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    listhtml = utils._getHtml(url, site.url, headers=hdr)

    results = re.findall('(?si)href="([^"]+)".*?data-original="([^"]+)" alt="([^"]+)', listhtml)
    for url, img, name in results:
        if img.startswith('//'):
            img = 'https:' + img
            img = img.replace(' ', '%20')
        id = img.split('/')[5]
        if ptlogged:
            contexturl = (utils.addon_sys
                          + "?mode=" + str('porntrex.PTSubscribe_pornstar')
                          + "&url=" + urllib_parse.quote_plus(url)
                          + "&id=" + str(id)
                          + "&what=" + str('unsubscribe'))
            contextmenu = ('[COLOR crimson]Unsubscribe[/COLOR]', 'RunPlugin(' + contexturl + ')')
        url = url + '?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'
        site.add_dir(name, url, 'PTList', img, 1, contextm=contextmenu)
    utils.eod()


@site.register()
def PTCheck_tags(url):
    try:
        listhtml = utils.getHtml(url)
    except:
        return None
    tags = {}
    matches = re.compile('<a href="([^"]+tags[^"]+)">([^<]+)</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    if matches:
        for url, tag in matches:
            tag = tag.strip()
            tags[tag] = url
        selected_tag = utils.selector('Pick a tag to look up videos', tags, show_on_one=True)
        if not selected_tag:
            return

        tagurl = selected_tag + '?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'
        contexturl = (utils.addon_sys
                      + "?mode=" + str('porntrex.PTList')
                      + "&url=" + urllib_parse.quote_plus(tagurl))
        xbmc.executebuiltin('Container.Update(' + contexturl + ')')
    else:
        utils.notify('Notify', 'No tags found at this video')
        return


@site.register()
def PTCheck_pornstars(url):
    try:
        listhtml = utils.getHtml(url)
    except:
        return None
    pornstars = {}
    matches = re.compile('<a href="([^"]+models[^"]+)"><i class="fa fa-star"></i>([^<]+)</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    if matches:
        for url, model in matches:
            model = model.strip()
            pornstars[model] = url
        selected_model = utils.selector('Choose model to add', pornstars, sort_by=lambda x: x[1], show_on_one=True)
        if not selected_model:
            return

        try:
            modelhtml = utils.getHtml(selected_model)
        except:
            return None
        id = re.findall(r'(?si)data-subscribe-to="model" data-id="(\d+)"', modelhtml)[0]
        if id:
            success = PTSubscribe_pornstar(selected_model, id)
            if success:
                utils.notify('Success', 'Pornstar added successfull to your subscriptions')
    else:
        utils.notify('Notify', 'No tagged pornstars found in this video')
    return


@site.register()
def PTSubscribe_pornstar(url, id, what='subscribe'):
    url = url + '/' if not url.endswith('/') else url
    suburl = '%s?mode=async&format=json&action=subscribe&subscribe_model_id=%s' % (url, id)
    if what == 'unsubscribe':
        suburl = suburl.replace('subscribe', 'unsubscribe')
    response = utils._getHtml(suburl, url)
    if 'success' in response.lower():
        success = True
    else:
        if what == 'unsubscribe':
            utils.notify('Failure', 'Failure removing the pornstar from your subscriptions')
        else:
            utils.notify('Failure', 'Failure adding the pornstar to your subscriptions')
        success = False
    if what == 'unsubscribe':
        utils.notify('Success', 'Pornstar removed successfull from your subscriptions')
        xbmc.executebuiltin('Container.Refresh')
    return success


@site.register()
def ContextMenu(url, fav):
    id = url.split("/")[4]
    fav_addurl = url + '?mode=async&format=json&action=add_to_favourites&video_id=' + id + '&album_id=&fav_type=0&playlist_id=0'
    fav_delurl = url + '?mode=async&format=json&action=delete_from_favourites&video_id=' + id + '&album_id=&fav_type=0&playlist_id=0'
    fav_url = fav_addurl if fav == 'add' else fav_delurl

    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    resp = utils._getHtml(fav_url, site.url, headers=hdr)

    if fav == 'add':
        if ('success') in resp:
            utils.notify('Favorites', 'Added to PT Favorites')
        else:
            msg = re.findall('message":"([^"]+)"', resp)[0]
            utils.notify('Favorites', msg)
        return
    if fav == 'del':
        if ('success') in resp:
            utils.notify('Deleted from PT Favorites')
            xbmc.executebuiltin('Container.Refresh')
        else:
            msg = re.findall('message":"([^"]+)"', resp)[0]
            utils.notify(msg)
        return


def get_cookies():
    domain = site.url.split('www')[-1][:-1]
    cookiestr = 'kt_tcookie=1'
    for cookie in utils.cj:
        if cookie.domain == domain and cookie.name == 'PHPSESSID':
            cookiestr += '; PHPSESSID=' + cookie.value
        if cookie.domain == domain and cookie.name == 'kt_ips':
            cookiestr += '; kt_ips=' + cookie.value
        if cookie.domain == domain and cookie.name == 'kt_member':
            cookiestr += '; kt_member=' + cookie.value
    if ptlogged and 'kt_member' not in cookiestr:
        PTLogin(False)
    return cookiestr


@site.register()
def PTModelsAZ():
    for i in range(65, 91):
        url = '{0}/models/?mode=async&function=get_block&block_id=list_models_models_list&section={1}&sort_by=title&from=1'.format(site.url, chr(i))
        site.add_dir(chr(i), url, 'PTModels', '', 1)
    utils.eod()


@site.register()
def PTModels(url, page=1):
    listhtml = utils.getHtml(url, site.url)
    results = re.findall('(?si)href="([^"]+)" title="([^"]+).*?src="([^"]+)".*?videos">([^<]+)<', listhtml)
    for modelurl, name, img, videos in results:
        url2 = modelurl + '?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'
        if img.startswith('//'):
            img = 'https:' + img
            img = img.replace(' ', '%20')
        id = img.split('/')[5] if 'no-image-model' not in img else None
        name = name + '[COLOR crimson] ' + videos + '[/COLOR]'
        if ptlogged and id:
            contexturl = (utils.addon_sys
                          + "?mode=" + str('porntrex.PTSubscribe_pornstar')
                          + "&url=" + urllib_parse.quote_plus(modelurl)
                          + "&id=" + str(id)
                          + "&what=" + str('subscribe'))
            contextmenu = ('[COLOR crimson]Subscribe[/COLOR]', 'RunPlugin(' + contexturl + ')')
            site.add_dir(name, url2, 'PTList', img, 1, contextm=contextmenu)
        else:
            site.add_dir(name, url2, 'PTList', img, 1)
    if len(results) == 160:
        if not page:
            page = 1
        npage = page + 1
        url = url.replace('from=' + str(page), 'from=' + str(npage))
        site.add_dir('Next Page', url, 'PTModels', site.img_next, npage)
    utils.eod()