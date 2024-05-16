import asyncio
import csv
import sys
import bs4
import httpx

domain = sys.argv[1]
csv_file = sys.argv[2]
links404 = []

headers = {
    "authority": "www." + domain,
    "referer": "https://" + domain,
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-dest": "document",
    "accept-language": "en-US,en;q=0.9,tr;q=0.8",
}

async def prepare_csv_data(id, post_link, data):
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

async def generate_csv_report(csv_file, csv_data):
    if csv_data:
        with open(csv_file, "w+", encoding="utf-8") as file:
            csvwriter = csv.DictWriter(file, fieldnames=list(csv_data[0].keys()))
            csvwriter.writeheader()
            csvwriter.writerows(csv_data)
        print("Report saved in file: ", csv_file)
    else:
        print("There were no broken links!")

def getLinks(rendered_content):
    soup = bs4.BeautifulSoup(rendered_content, "html.parser")
    return [(link["href"], link.text) for link in soup("a") if "href" in link.attrs]
    
async def getStatusCode(client, link, headers, timeout=5):
    print("    checking: ", link[0])
    try:
        r = await client.head(link[0], headers=headers, timeout=timeout)
        if r.status_code in {404, 400, 403}:
            r = await client.get(link[0], headers=headers, timeout=timeout)
    except httpx.RequestError as errh:
        print("Error in URL, ", link)
        return link, errh.__class__.__name__
    else:
        return link, str(r.status_code)

async def executeBrokenLinkCheck(client, links):
    results = []
    tasks = [getStatusCode(client, link, headers) for link in links]
    for task in asyncio.as_completed(tasks):
        results.append(await task)
    return results

async def main():
    async with httpx.AsyncClient() as client:
        pages = int(
            (await client.get("https://" + domain + "/wp-json/wp/v2/posts", headers=headers)).headers[
                "X-WP-TotalPages"
            ]
        )
        for i in range(pages):
            post_data = (
                await client.get(
                    "https://" + domain + "/wp-json/wp/v2/posts?page=" + str(i + 1),
                    headers=headers,
                )
            ).json()
            for data in post_data:
                print("Checking post: ", data["link"])
                post_links = getLinks(data["content"]["rendered"])
                checked_urls = await executeBrokenLinkCheck(client, post_links)
                await prepare_csv_data(data["id"], data["link"], checked_urls)
    await generate_csv_report(csv_file, links404)

asyncio.run(main())
