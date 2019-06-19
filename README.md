# knp2dcsvec

A tool to convert a KNP output to triples for DCSVec.

## Requirements

* [pyknp](https://github.com/ku-nlp/pyknp)
* [Juman++](https://github.com/ku-nlp/jumanpp)
* [KNP](http://nlp.ist.i.kyoto-u.ac.jp/index.php?KNP)

## Usage

```
% jumanpp < samples/sample1.txt | knp -tab > samples/sample1.knp
% python3 scripts/extract-triples-from-knp.py < samples/sample1.knp > samples/sample1.tsv
```
