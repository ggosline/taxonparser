from lxml import etree

__author__ = 'gg12kg'


def XMLFromRecord(parent, tparsed, tag=None):
    """ parent is parent element in tree; tparsed is a simple string or a list or records (see recordtype.py)
        Create etree element with tag if tag is specified; attach to parent
        create subelements from list of records; append as children """

    txel = None

    if tparsed:

        if type(tparsed) is str:
            if tag:
                txel = etree.SubElement(parent, tag)
            else:
                txel = parent
            txel.text = tparsed
        elif type(tparsed) is list:

            for pmem in tparsed:
                if tag:
                    txel = etree.SubElement(parent, tag)
                else:
                    txel = parent
                if type(pmem) is str:
                    txel.text = pmem
                else:    # a recordtype
                    txflds = [f for f in pmem if f[1]]
                    for fld in txflds:
                        el = etree.SubElement (txel, fld[0])
                        el.text = fld[1]
        else:   # a recordtype ? or a dictionary
            if tag:
                txel = etree.SubElement(parent, tag)
            else:
                txel = parent

            txflds = [f for f in tparsed if f[1]]
            for fld in txflds:
                el = etree.SubElement (txel, fld[0])
                el.text = fld[1]

    return txel

