

def elevate_tax_line_id(root):
    for tax_line_info in root.findall(".//AccountRet/TaxLineInfoRet"):
        tax_line_id = tax_line_info.find("TaxLineID")

        if tax_line_id is not None:
            parent = tax_line_info.getparent()
            parent.append(tax_line_id)

        if parent is not None:
            parent.remove(tax_line_info)

    return root