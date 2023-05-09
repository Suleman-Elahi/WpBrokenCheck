# WpBrokenCheck

[![HitCount](https://hits.dwyl.com/suleman-elahi/WpBrokenCheck.svg?style=flat)](http://hits.dwyl.com/suleman-elahi/WpBrokenCheck)

![](https://komarev.com/ghpvc/?username=WpBrokenCheck&color=green&label=VIEWS)

This is a simple Python script you can use to find out broken links on a WordPress website. It uses WordPress's API v2 to get all the published posts and scans all the links inside including internal links, external links, attachments, images, etc.

At the end, it saves a CSV file in the current working directory. By default, all the links are stored in the CSV file. Later, you can filter them using Excel or LibreOffice.

## Running:
1. Install Python
2. Install [Poetry](https://python-poetry.org/docs/#installation)
3. Run `poetry install`
4. Run as `poetry run python WpBrokenCheck.py [Domain] [CSV_FileName]`
5. Example: `poetry run python WpBrokenCheck.py example.com example.csv`
<p align="center">
  <img src="https://res.cloudinary.com/suleman/image/upload/v1665055858/WpBrokenCheck.png">
</p>

**Note** : Only type domain without http:// or https://

**Tip** : If target website has large number of posts then change `max_workers` from 5 to 10 at line 60.

## Linters:

There are the following Python linters:
- black for code formatting
- flake8 code formatting and line brakes (PEP8)
- isort for reordering imports

They are run via pre-commit as you commit the code to the repository. You can also run it manually on all files by:
`pre-commit run --all-files`

### To Do:
- Make it filter specific codes.
- Make it run on customized WP sites
- ~~Push binary releases~~

PRs and suggestions are welcome :)
