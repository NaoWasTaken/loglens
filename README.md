# LogLens

A CLI tool for analyzing Apache, Nginx, and JSON log files

## Installation

git clone https://github.com/naowastaken/loglens.git  <br>
cd loglens  <br>
pip install -e .

## Usage

loglens file --format --filter

## Formats (pick one)

--apache  <br>
--nginx  <br>
--json  <br>

## Filters (pick one)

--findcodes              Show all status codes and counts  <br>
--errorsonly             Show 4xx and 5xx errors  <br>
--successonly            Show 2xx responses  <br>
--redirectonly           Show 3xx redirects  <br>
--informationalonly      Show 1xx responses  <br>

## Options

--explain                Human description of each status code  <br>
--from-date              Start date (mm/dd/yyyy)  <br>
--to-date                End date (mm/dd/yyyy)  <br>

## Examples

loglens server.log --apache --findcodes  <br>
loglens server.log --apache --errorsonly --explain  <br>
loglens server.log --nginx --errorsonly --from-date 01/01/2026 --to-date 01/31/2026
