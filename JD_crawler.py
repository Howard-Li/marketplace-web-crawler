# -*- coding: utf-8 -*-
# __author__ = 'HaoquanLi'

import urllib2
import re

# input the keyword and the lower bound of price range (default 0)
def get_jingdong_price(keyword, lowerBound = 0):
    #lowerBound: the lower bound of the prices of interest. This is the major filter.
    keyword = keyword.replace(' ','+')

    url0 = 'http://search.jd.com/Search?keyword=lego%20'+keyword+'&enc=utf-8&qr=&qrst=UNEXPAND&rt=1&click=&psort=2'
    try:
        html0 = urllib2.urlopen(url0).read()

        if re.match('.+抱歉，没有找到.+', html0, re.S) is not None:  # re.S means the dot can represent every thing including the new line char
            print ('item not found')
            return

        items = []
        items.extend(re.findall('<li sku="(\d+)" >',html0))

        prices = []
        for item_id in items:
            url = 'http://p.3.cn/prices/get?skuid=J_' + str(item_id)
            html = urllib2.urlopen(url).read().decode('utf-8')
            prices.append(re.search(r'"p":"(.*?)"', html).group(1))

        # parse the prices into floats
        # and generate shopping links
        shop_links = []
        for i in range(len(prices)):
            try:
                prices[i] = float(prices[i])
                shop_links.append('http://item.jd.com/'+item_id+'.html')
            except:
                prices[i]=-9999  #have to do this to make the list consistent. -9999 will be filtered out anyway
                shop_links[i].append('not found')

        #final check of prices
        result_prices = []
        result_links = []
        for i in range(len(prices)):
            if lowerBound <= prices[i]:
                 result_prices.append(prices[i])
                 result_links.append(shop_links[i])

        if (len(result_prices)):
            return result_prices[0], result_links[0]  # this is the lowest price and link of interest
        else:
            print('no prices found in range')

    except:
        print ('cannot open webpage')


# for example, if I want to search for a Lego toy set:
print(get_jingdong_price('lego 42009',2000))
