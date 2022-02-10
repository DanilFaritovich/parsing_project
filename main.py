import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}


class SearchStarterPages(object):
    def __init__(self):
        # find main html
        self.url = 'https://xkcd.com/'
        self.r = requests.get(self.url, headers=headers)
        self.text = html.fromstring(self.r.text)

    def search(self, orientation):
        # find start page html
        first_page = self.text.xpath('.//a[text() = "{}"]/@href'.format(orientation))
        self.url = 'https://xkcd.com{}'.format(first_page[0])
        self.r = requests.get(self.url, headers=headers)
        self.text = html.fromstring(self.r.text)
        return [self.text, self.url]


class SearchLinks(object):
    def links(self, text, url, orientation):
        list_of_links, img_link = [], None
        for len_of_list in range(0, 10):
            # find img
            img_link = [link
                        for link in text.xpath('.//a/@href')
                        if link[-4:] == ".png" or link[-4:] == ".jpg"]

            # save link and img link
            list_of_links.append([url, img_link[0]])

            # find next page
            next_page = text.xpath('.//a[text() = "{}"]/@href'.format(orientation))
            url = 'https://xkcd.com{}'.format(next_page[0])
            r = requests.get(url, headers=headers)
            text = html.fromstring(r.text)
        return list_of_links


if __name__ == '__main__':
    # search start and end url and html
    starter_page = SearchStarterPages()
    page = [starter_page.search("|<"), starter_page.search(">|")]  # [[html, url], [html, url]]

    # search start and last links of img and link
    object_links = SearchLinks()
    list_links = [object_links.links(page[0][0], page[0][-1], "Next >"),
                  object_links.links(page[-1][0], page[-1][1], "< Prev")]

    with open("result.txt", "w") as w:
        w.writelines("10 start links\n")
        for i in list_links[0]:
            w.writelines(i[0] + " " + i[-1] + "\n")
        w.writelines("10 end links\n")
        for i in reversed(list_links[1]):
            w.writelines(i[0] + " " + i[-1] + "\n")
