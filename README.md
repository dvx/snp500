## snp500
JSON endpoint that returns an up-to-date list of S&amp;P500 constituents scraped from Wikipedia. I got tired of writing (or finding) code that gets the S&P500 symbols every time I needed them, so I threw together this endpoint. It should be around as long as Heroku and Wikipedia are around.

## why doesn't Standard & Poor's have a master list somehwere?
Beats me.

## how do you generate the list?
I grab it from Wikipedia and cache it on redis. When the page revision changes, the cache is updated.

## what is `sane`?
`sane` indicates whether or not we're getting 505 symbols back, as expected. Keep in mind that Wikipedia might not always be right, so *caveat emptor*.

## what's the URL?
https://snp500.herokuapp.com/

## license
MIT
