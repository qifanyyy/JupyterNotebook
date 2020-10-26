#!/usr/bin/env python
__doc__ = """ """;

import sys,os,re

rgxFilename = re.compile(".*/bst_(.*)\.c");

filePrefix="""
#ifndef VARIANTS_H
#define VARIANTS_H

#include"bst.h"
"""

fileSuffix="""
#endif // VARIANTS_H
"""

implArrayPrefix="""
bst_impl_t implementations[] = {
    {
        .name    = "ref/bst_ref.c",
        .alloc   = bst_alloc,
        .compute = bst_compute,
        .root    = bst_get_root,
        .free    = bst_free,
        .flops   = bst_flops
    }
""";

implArraySuffix="""
};
"""
outFilename = "variants.h"

class Implementation(object):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def getDeclarations(self):
        declStr = "void* bst_alloc_%s( size_t n );\n" % (self.name,)
        declStr += """double bst_compute_%s( void*_bst_obj, double* p, double* q,
                                   size_t n );\n""" % (self.name,)
        declStr += """size_t bst_get_root_%s( void* _bst_obj, size_t i, size_t j );\n""" % (self.name,)
        declStr += """void bst_free_%s( void* _mem );\n""" % (self.name);
        declStr += """size_t bst_flops_%s( size_t n );\n""" % (self.name);

        return declStr;

    def getImplDefinition(self):
        return """, {
        .name    = "%s",
        .alloc   = bst_alloc_%s,
        .compute = bst_compute_%s,
        .root    = bst_get_root_%s,
        .free    = bst_free_%s,
        .flops   = bst_flops_%s
        }""" % (self.filename, self.name, self.name, self.name, self.name, self.name);

def main():
    impls = []
    for s in sys.argv[1:]:
        m = rgxFilename.match(s)
        if m != None:
            impls.append( Implementation(m.group(1), m.group(0)) )
    f_out = open(outFilename, "w")
    f_out.write(filePrefix);
    for impl in impls:
        f_out.write(impl.getDeclarations())
    f_out.write(implArrayPrefix)
    for impl in impls:
        f_out.write(impl.getImplDefinition())
    f_out.write(implArraySuffix);
    f_out.write(fileSuffix);

if __name__=="__main__":
    main()
