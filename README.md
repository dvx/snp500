# snp500
JSON endpoint that returns an up-to-date list of S&amp;P 500 constituents scraped from Wikipedia.

# why doesn't Standard & Poor's have a master list somehwere?
Who knows.

# how do you generate the list?
I grab it from Wikipedia and cache it on redis. When the page revision changes, the cache is updated.

# what is `sane`?
`sane` indicates wether or not we're getting 505 symbols back, as expected. Keep in mind that Wikipedia might not always be right, so *caveat emptor*.

# what's the URL?
https://snp500.herokuapp.com/

# license
MIT
