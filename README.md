# WpBrokenCheck
This is a simple Python script you can use to find out broken links on a WordPress website. It uses WordPress's API v2 to get all the published posts and scans all the links inside including internal links, external links, attachments, images, etc.

At the end, it saves a CSV file in the current working directory. By default, all the links are stored in the CSV file. Later, you can filter them using Excel or LibreOffice.

## Running:
1. Install Python
2. Run `pip install requests bs4`
3. Run as `python WpBrokenCheck.py [Domain] [CSV_FileName]`
4. Example: `python WpBrokenCheck.py example.com example.csv`
<p align="center">
  <img src="https://res.cloudinary.com/suleman/image/upload/v1665055858/WpBrokenCheck.png">
</p>

**Note** : Only type domain without http:// or https://

### To Do:
- Make it filter specific codes.
- Make it run on customized WP sites
- Push binary releases

PRs and suggestions are welcome :)
