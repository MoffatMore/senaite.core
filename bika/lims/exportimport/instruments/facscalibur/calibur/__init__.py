# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

""" Facs Calibur
"""
from datetime import datetime
from bika.lims.exportimport.instruments.resultsimport import \
    AnalysisResultsImporter, InstrumentCSVResultsFileParser


class FacsCaliburCSVParser(InstrumentCSVResultsFileParser):
    def __init__(self, csv):
        InstrumentCSVResultsFileParser.__init__(self, csv)
        self._columns = []  # The different columns names
        self._values = {}  # The analysis services from the same resid
        self._rownum = None
        self._end_header = False
        # self._includedcolumns =['Ca', 'Cu',
        #                         'Fe', 'Mg']
        self._includedcolumns = ['CD3+CD4+ %Lymph', 'CD3+CD4+ Abs Cnt',
                                  'CD3+CD8+ %Lymph', 'CD3+CD8+ Abs Cnt']

    def _parseline(self, line):
        sline = line.split(',')
        if len(sline) > 0 and not self._end_header:
            self._columns = sline
            for column in self._columns:
                self._columns = column.split('\t')
            print(self._columns)
            self._end_header = True

            for i, j in enumerate(self._columns):
                if j.startswith('(Average)'):
                    j = j[len('(Average)')+1::]
                    self._columns[i] = j
                    print(str(i)+' '+j)
            return 0
        elif sline > 0 and self._end_header:
            self.parse_data_line(sline)
        else:
            self.err("Unexpected data format", numline=self._numline)
            return -1


    def parse_data_line(self, sline):
        """
                Parse the data line. If an AS was selected it can distinguish between data rows and information rows.
                :param sline: a split data line to parse
                :returns: the number of rows to jump and parse the next data line or return the code error -1
                """

        temp_line = sline
        sline_ = ''.join(temp_line)
        sline_ = sline_.split('\t')
        headerdict = {}
        datadict = {}
        for idx, result in enumerate(sline_):
            if self._columns[idx] in self._includedcolumns:
                datadict[self._columns[idx]] = {'Result': result, 'DefaultResult': 'Result'}
            else:
                headerdict[self._columns[idx]] = result
        resid = headerdict['Sample ID']
        print(datadict)
        self._addRawResult(resid, datadict, False)
        self._header = headerdict
        return 0


class FacsCaliburImporter(AnalysisResultsImporter):
    def __init__(self, parser, context, idsearchcriteria, override,
                 allowed_ar_states=None, allowed_analysis_states=None,
                 instrument_uid=None):
        AnalysisResultsImporter.__init__(self, parser, context,
                                         idsearchcriteria, override,
                                         allowed_ar_states,
                                         allowed_analysis_states,
instrument_uid)