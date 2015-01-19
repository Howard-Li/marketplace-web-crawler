# __author__ = 'HaoquanLi'
# input the keyword and the lower bound of price range (default 0)

import urllib2
import re

# this function takes the set ID and the current price in our data base as parameters
def get_ebay_price(keyword, lowerBound = 0):
    # lowerBound: the lower bound of the prices of interest. This is the major filter.

    keyword = keyword.replace(' ','+')
    url = 'http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_sop=15&_mPrRngCbx=1&_udlo='+str(lowerBound)+'&_udhi=&LH_ItemCondition=3&_nkw='+keyword+'&rt=nc&LH_FS=1'
    print (url)

    # note that the above link finds  FREE SHIPPING items only. sorted by lowest price first. condition: new.

    # start crawling....
    try:
        response = urllib2.urlopen(url)  #prices from low to high
        html = response.read()

        if re.match('.+<b>0</b> results found for <b>.+', html, re.S) is not None:  # re.S means the dot can represent every thing including the new line char
            print ('item not found')
            return

        itemgroups = html.split('h3 class="l') # split the page source
        del itemgroups[0]
        prices = [] # prices of the above items
        shop_links = []

        for iteminfo in itemgroups:
            # start to filter out unwanted results

            # if the set ID is not in title, then ignore this item.
            curr_link = re.search('title"><a href="(.+)".+class="vip"', iteminfo, re.S).group(1)
            #if not re.search(str(setid), curr_link):
            #    continue

            prices.extend(re.findall('class="g-b">.+\\$(\d+.\d{2})</span>', iteminfo, re.S))
            shop_links.append(curr_link)

        # parse the prices into floats
        # and generate shopping links

        for i in range(len(prices)):
            try:
                prices[i] = float(prices[i])
            except:
                prices[i]=-9999  #have to do this to make the list consistent. -9999 will be filtered out anyway

        if (len(prices)):
            return prices[0], shop_links[0]  # this is the lowest price and link of interest
        else:
            print('no prices found in range')

    except:
        print('no set')



# for example, if I want to search for a Lego toy set:
print (get_ebay_price('lego 10242', 99))
