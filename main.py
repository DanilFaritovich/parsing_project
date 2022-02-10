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
    def __init__(self, text, url):
        self.list_of_links = []
        self.text = text
        self.url = url
        self.img_link = None

    def start_links(self):
        for len_of_list in range(0, 10):
            # find img
            for link in self.text.xpath('.//a/@href'):
                if link[-4:] == ".png" or link[-4:] == ".jpg":
                    self.img_link = link
                    break

            # save link and img link
            self.list_of_links.append([self.url, self.img_link])

            # find next page
            next_page = self.text.xpath('.//a[text() = "Next >"]/@href')
            self.url = 'https://xkcd.com{}'.format(next_page[0])
            r = requests.get(self.url, headers=headers)
            self.text = html.fromstring(r.text)

        return self.list_of_links

    def end_links(self):
        for len_of_list in range(0, 10):
            # find img
            for link in self.text.xpath('.//a/@href'):
                if link[-4:] == ".png" or link[-4:] == ".jpg":
                    self.img_link = link
                    break

            # save link and img link
            self.list_of_links.append([self.url, self.img_link])

            # find next page
            next_page = self.text.xpath('.//a[text() = "< Prev"]/@href')
            self.url = 'https://xkcd.com{}'.format(next_page[0])
            r = requests.get(self.url, headers=headers)
            self.text = html.fromstring(r.text)
        return self.list_of_links


if __name__ == '__main__':
    # search start and end url and html
    starter_page = SearchStarterPages()
    start_page, end_page = starter_page.search("|<"), starter_page.search(">|")  # (html, url)

    # search start and last links of img and link
    object_start_links = SearchLinks(start_page[0], start_page[1])
    object_end_links = SearchLinks(end_page[0], end_page[1])
    list_start_links = object_start_links.start_links()
    list_end_links = object_end_links.end_links()

    with open("result.txt", "w") as w:
        w.writelines("10 start links\n")
        for i in list_start_links:
            w.writelines(i[0] + " " + i[-1] + "\n")
        w.writelines("10 end links\n")
        for i in list_end_links:
            w.writelines(i[0] + " " + i[-1] + "\n")