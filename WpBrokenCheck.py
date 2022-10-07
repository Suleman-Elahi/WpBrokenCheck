import concurrent.futures
import csv
import sys
from concurrent.futures import as_completed

import bs4
import requests

domain = sys.argv[1]
csv_file = sys.argv[2]
sess = requests.Session()
links404 = []

headers = {
    "authority": "www." + domain,
    "referer": "https://" + domain,
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-dest": "document",
    "accept-language": "en-US,en;q=0.9,tr;q=0.8",
}
pages = int(
    sess.get("https://" + domain + "/wp-json/wp/v2/posts", headers=headers).headers[
        "X-WP-TotalPages"
    ]
)


def prepare_csv_data(id, post_link, data):
    for i in data:
        links404.append(
            {
                "Post ID": id,
                "Post Link": post_link,
                "Broken Link": i[0][0],
                "Status Code": i[1],
                "Link Text": i[0][1],
            }
        )


def generate_csv_report(csv_file, csv_data):
    with open(csv_file, "w+", encoding="utf-8") as file:
        csvwriter = csv.DictWriter(file, fieldnames=list(csv_data[0].keys()))
        csvwriter.writeheader()
        csvwriter.writerows(csv_data)


def getLinks(rendered_content):
    soup = bs4.BeautifulSoup(rendered_content, "html.parser")
    return [(link["href"], link.text) for link in soup("a") if "href" in link.attrs]


def getStatusCode(link, headers, timeout=5):
    print("	checking: ", link[0])
    try:
        r = sess.head(link[0], headers=headers, timeout=timeout)
    except (
        requests.exceptions.SSLError,
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.MissingSchema,
        requests.exceptions.Timeout,
        requests.exceptions.InvalidSchema,
    ) as errh:
        print("Error in URL, ", link)
        return link, errh.__class__.__name__
    else:
        return link, str(r.status_code)


def executeBrokenLinkCheck(links):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(getStatusCode, link, headers) for link in links]
        return [future.result() for future in as_completed(futures)]


for i in range(pages):
    post_data = sess.get(
        "https://" + domain + "/wp-json/wp/v2/posts?page=" + str(i + 1), headers=headers
    ).json()
    for data in post_data:
        print("Checking post: ", data["link"])
        post_links = getLinks(data["content"]["rendered"])
        checked_urls = executeBrokenLinkCheck(post_links)
        prepare_csv_data(data["id"], data["link"], checked_urls)

generate_csv_report(csv_file, links404)
print("Report saved in file: ", csv_file)
