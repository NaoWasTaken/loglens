# LogLens

A CLI tool for analyzing Apache, Nging, and JSON log files

## Installation

git clone https://github.com/naowastaken/loglens.git
cd loglens
pip install -e .

## Usage

loglens <file> --<format> --<filter>

## Formats (pick one)

--apache
--nginx
--json

## Filters (pick one)

--findcodes              Show all status codes and counts
--errorsonly             Show 4xx and 5xx errors
--successonly            Show 2xx responses
--redirectonly           Show 3xx redirects
--informationalonly      Show 1xx responses

## Options

--explain                Human description of each status code
--from-date              Start date (mm/dd/yyyy)
--to-date                End date (mm/dd/yyyy)

## Examples

loglens server.log --apache --findcodes
loglens server.log --apache --errorsonly --explain
loglens server.log --nginx --errorsonly --from-date 01/01/2026 --to-date 01/31/2026