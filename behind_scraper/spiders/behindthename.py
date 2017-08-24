# -*- coding: utf-8 -*-
import scrapy


def get_name_info(response, value, links_only=True):
    xpath = "//div[contains(@class, 'nameinfo')]//span[contains(text(), '{value}')]/following-sibling::span{link}//text()"
    name_info_xpath = xpath.format(value=value,
                                   link='/a' if links_only else '')

    return response.xpath(name_info_xpath)


def get_other_scripts(response):
    xpath = "//div[contains(@class, 'nameinfo')]//span[contains(text(), 'OTHER SCRIPTS')]/following-sibling::span//a/text()"
    return response.xpath(xpath)

def get_name(response):
    name = response.xpath(
        "//div[contains(@class, 'namemain') and contains(text(), 'Given Name')]//text()"
    ).extract_first()
    if not name:
        return
    name = name.replace('Given Name ', '').capitalize()
    return name


class BehindthenameSpider(scrapy.Spider):
    name = 'behindthename'
    allowed_domains = ['www.behindthename.com']
    start_urls = ['https://www.behindthename.com/names/']

    def parse(self, response):
        name_links = response.xpath(
            "//div[contains(@class, 'browsename')]//a[contains(@href, 'name/')]/@href"
        ).extract()

        if name_links:
            for l in name_links:
                yield response.follow(l, callback=self.parse_name)

        next_page = response.xpath("//a[contains(text(), 'Next Page')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_name(self, response):
        name = get_name(response)
        gender = get_name_info(response, 'GENDER', links_only=False).extract_first()
        usage = get_name_info(response, 'USAGE').extract()
        other_scripts = get_name_info(response, 'OTHER SCRIPTS').extract()

        other_names = response.xpath(
            "//a[contains(@class, 'ngl') or contains(@class, 'nl') and starts-with(@href, '/name/') and not(contains(@href, 'submitted'))]/@href"
        ).extract()
        for n in other_names:
            if 'submitted' or 'tag' not in n:
                yield response.follow(n, callback=self.parse_name)
