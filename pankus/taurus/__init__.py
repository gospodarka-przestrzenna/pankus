#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Wawrzyniec Zipser, Maciej Kamiński Politechnika Wrocławska'
__all__ = [
    'Taurus'
]
__taurus_version__="4.0"
from .importer import Importer
from .route import Route
from .intervening_opportunities import InterveningOpportunities
from .mst import MST
from .network_generators import NetworkGenerator
from .analysis import Analysis
from .data_journal import DataJournal
from .exporter import Exporter
from .path import Path
from .load import Load

class Taurus(Route,InterveningOpportunities,MST,NetworkGenerator,Analysis,Exporter,Path,Load):

    def __init__(self,**kwargs):
        self.kwargs=kwargs
        super().__init__(**kwargs)
