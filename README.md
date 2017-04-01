# simple-web-crawler

## how to run the crawler

To run the crawler start installing the requirements through the requirements.txt file 

Initialise the CrawlManager object through: 

>block quote
     
     crawl_manager = CrawlManager("http://my-seed-url.com", 10)

The first parameter represents the seed url where you want to start crawling, the second parameter determine the URL queue size. You must pass an integer, be careful not to use a big number since the URL queue is an in memory data structure and you might end up reaching memory limit. 

You can then start crawling simply calling:

>block quote
     
     response = crawl_manager.crawl()

Response will be a JSON object of the type:

```
{"http://my-seed-url.com": 
  ["http://my-seed-url/logo.png", "http://my-seed-url/signup.js", http://my-seed-url/background.css],
"http://my-seed-url.com/prices":
  ["http://my-seed-url/prices/price.png", "http://my-seed-url/prices/calculate-price.js", http://my-seed-url/prices/price-color.css]}
```
## crawler logic

The below diagram shows the crawler logic

![Alt text](https://github.com/agastaldoDataxu/simple-web-crawler/blob/master/Simple%20Crawler.jpg "Simple Web Crawler diagram")
