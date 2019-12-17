#!/usr/bin/env python3

from pyknp import KNP
import sys
import re
import argparse

knp = KNP(jumanpp=True)

# get the head word from a given bnst (general method)
def get_head_word_from_bnst(bnst, compound_flag=False):
    # if we want to extract compund nouns
    if compound_flag:
        m = re.search("<正規化代表表記:([^>]+)", bnst.fstring)
        if m:
            return m.group(1);

    m = re.search("<主辞’代表表記:([^>]+)", bnst.fstring)
    if m:
        return m.group(1);
    else:
        m = re.search("<主辞代表表記:([^>]+)", bnst.fstring)
        if m:
            return m.group(1);
        else:
            return None

# get the head word from a given governor
def get_head_word_from_governor(bnst):
    # get the last tag from bnst to extract (標準)用言代表表記
    tag = bnst.tag_list()[-1]
    if "<用言:" in tag.fstring:
        m = re.search("<標準用言代表表記:([^>]+)", tag.fstring)
        if m:
            return m.group(1);
        else:
            m = re.search("<用言代表表記:([^>]+)", tag.fstring)
            if m:
                return m.group(1);
    return get_head_word_from_bnst(bnst)

# get the dependency type from a given bnst
def get_dpnd_type(bnst, parent):
    m = re.search("<係:([^>]+)", bnst.fstring)
    if m:
        dpnd_type = m.group(1)
        # distinguish ga in passive voice from ga in active voice
        if dpnd_type == 'ガ格' and parent and '<〜られる>' in parent.fstring:
            return 'ガ格受動'
        else:
            return dpnd_type
    else:
        return None

# get the dependency type for 複合辞
def get_dpnd_type_for_compound_case(bnst):
    # get the last tag from bnst to extract 解析格
    tag = bnst.tag_list()[-1]
    # a normalized form of 複合辞 is stored in 解析格 (needs case analysis)
    m = re.search("<解析格:([^>]+)", tag.fstring)
    if m:
        return m.group(1)
    else:
        return "複合辞連用"


parser = argparse.ArgumentParser(description='Extract triples for DCS2Vec from KNP parses')
parser.add_argument('--compound', '-c', action='store_true',
                    help='extract compound nouns as modifiers')
args = parser.parse_args()

data = ""
for line in iter(sys.stdin.readline, ""):
    data += line
    if line.strip() == "EOS":
        result = knp.result(data)
        for bnst in result.bnst_list():
            # skip 複合辞 as a modifier
            if "複合辞" in bnst.fstring:
                continue
            modifier_str = get_head_word_from_bnst(bnst, args.compound)
            if not modifier_str:
                continue
            parent = bnst.parent
            if parent:
                if "複合辞" in parent.fstring:
                    dpnd_type = get_dpnd_type_for_compound_case(bnst)
                    # grandparent is the predicate for 複合辞
                    parent = parent.parent
                    if not parent:
                        continue
                else:
                    dpnd_type = get_dpnd_type(bnst, parent)
                    # NONE is exceptional
                    if dpnd_type == "NONE":
                        continue
                governor_str = get_head_word_from_governor(parent)
                if not governor_str:
                    continue
                print("\t".join((modifier_str, dpnd_type, governor_str)))
        data = ""
