#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .sqlite_database import SQLiteDatabase
from .utils import TaurusLongTask

class InterveningOpportunity(SQLiteDatabase):

    # uploading keyword arguments, if the value is missing field is filled with default value
    def __init__(self,**kwargs):
        """
        uploading keyword arguments, if the value is missing field is filled with default value
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.kwargs=kwargs
        self.sources_name=kwargs.get('sources_name','sources')
        self.destinations_name=kwargs.get('destinations_name','destinations')
        self.selectivity_name=kwargs.get('selectivity_name','selectivity')
        self.convolution_start_name=kwargs.get('convolution_start_name','conv_a')
        self.convolution_size_name=kwargs.get('convolution_size_name','conv_b')
        self.convolution_intensity_name=kwargs.get('convolution_intensity_name','conv_alpha')
    
    # importing model parameters, if the values are not given default values from function init are used
    def import_model_parameters(self):
        """
        importing model parameters, if the values are not given default values from function init are used
        :return: self
        """
        self.do('intopp/create_model_parameters')
        self.do('intopp/insert_model_parameters',{
            'sources_name':self.sources_name,
            'destinations_name':self.destinations_name,
            'selectivity_name':self.selectivity_name,
            'convolution_start_name':self.convolution_start_name,
            'convolution_size_name':self.convolution_size_name,
            'convolution_intensity_name':self.convolution_intensity_name
        })
    
    # creating selectivity, a parameter describing probability of object choosing a point as a destination,
    # taking into consideration other point placed between the object and considered point.
    # Sum of all destinations from table "model_parameters" is selected, then used to calculate selectivity value,
    # which is later updated in the "model_parameters" table.
    # Before being written in the table value of selectivity is multiplied by 1 000 000 to include its fractional part with high accuracy.
    # When selectivity value is used in calculations it is divided by the same number.
    def create_escape_fraction_selectivity(self,efs):
        """
        creating selectivity, a parameter describing probability of object choosing a point as a destination,
        taking into consideration other point placed between the object and considered point.
        Sum of all destinations from table "model_parameters" is selected, then used to calculate selectivity value,
        which is later updated in the "model_parameters" table.
        Before being written in the table value of selectivity is multiplied by 1 000 000 to include its fractional part with high accuracy.
        When selectivity value is used in calculations it is divided by the same number.
        :param efs:
        :return: self
        """
        # TODO search for selectivity in convolution
        destinations_total,=self.one('intopp/select_destinations_total')
        selectivity=-math.log(efs)/destinations_total
        self.do('intopp/update_sd_selectivity',{'selectivity':selectivity*1000000})
    
    # building specified number of rings which are written in the table "ring" containing following parameters,
    # which describe ring placement of a source-destination point in the realtion to the second source-destination point.
    # Function selects maximum value of distance from table distance then uses it to calculate a factor essential in rings creation.
    # In calculations maximum distance is multiplied by 1.0001 in order to move slightly the border of last ring so the furthest point in the network is included.
    # Table "ring" is filled using SQL script "insert_ring_uniform"
    def build_uniform_rings(self,no_of_rings):
        """
        creating selectivity, a parameter describing probability of object choosing a point as a destination,
        taking into consideration other point placed between the object and considered point.
        Sum of all destinations from table "model_parameters" is selected, then used to calculate selectivity value,
        which is later updated in the "model_parameters" table.
        Before being written in the table value of selectivity is multiplied by 1 000 000 to include its fractional part with high accuracy.
        When selectivity value is used in calculations it is divided by the same number.
        :param no_of_rings:
        :return: self
        """
        self.do('intopp/create_ring')
        max_distance,=self.one('intopp/distance_maximum')
        #I don't like solution but is mostly what we expect
        factor=no_of_rings/(max_distance*1.0001)
        #
        self.do('intopp/insert_ring_uniform',{'factor':factor})

    def build_weighted_rings(self,weight):
        self.do('intopp/create_ring')
        factor=weight
        self.do('intopp/insert_ring_weighted',{'factor':factor})

    # creating table "ring_total" containing data on number of destinations located in specified ring and sum of all the destinations from rings prior to the described ring.
    # Table is filled by SQL script which uses tables "ring" and "model_parameters"
    def ring_total(self):
        """
        function "ring_total" creates table "ring_total" containing data on number of destinations located in specified ring and sum of all destiantions from rings prior to this ring
        :return: self
        """
        self.do('intopp/create_ring_total')
        self.do('intopp/insert_ring_total')
        
    # normalization of motion exchange. All the "objects" left in te network are set to be new 100% of network population
    # ("objects" that left the network in search for destinatons aren't included). SQL script "normalization" uses tables "motion_exchange_fraction" and creates helper table "temp_motion_exchange_fraction_total". Table "motion_exchange" is then updated with normalized values.
    def normalize_motion_exchange(self):
        """
        function "normalize_motion_exchange" normalizes motion exchange, setting all the objects left in the network to be the new 100% of netwok population
        SQL script "normalization" uses tables "motion_exchange_fraction" and creates helper table "temp_motion_exchange_fraction_total".
        Table "motion_exchange" is then updated with normalized values.
        :return: self
        """
        self.do('intopp/normalization')

    def destination_shift(self):
        self.do('intopp/destination_shift')

    def general_shift(self):
        self.do('intopp/general_shift')

    def sources_shift(self):
        self.do('intopp/sources_shift')

    def save_intopp_parameters(self,suffix):
        self.do('intopp/save_parameters',{
            'sources_new_name':'sources'+suffix,
            'destinations_new_name':'destinations'+suffix,
            'selectivity_new_name':'selectivity'+suffix,
        })

    #calculating numbers of transported "objects". Results are written in the "motion_exchange" table, describing accurate quantity of transported "objects" and "motion_exchange_fraction" table, describing the same amounts in a form of fractions. Due to the model nature especially importatnt are fraction of "objects" which found destination in a chosen ring and fraction of "objects" which found destinations in the prior rings. "motion_exchange" function uses data stored in tables "ring", "ring_total" and "model_parameters".
    def motion_exchange(self):
        """
        calculates numbers of transported "objects". Results ae written in the "motion_exchange" table. which describes accurate quantity of transported "objects"
        "motion_exchange_fraction" contains the same data in a different form - quantity of transported objects is expressed as a fraction.
        Due to the model nature especially importatnt are fraction of "objects" which found destination in a chosen ring and fraction of "objects" which found destinations in the prior rings.
        "motion_exchange" function uses data stored in tables "ring", "ring_total" and "model_parameters".
        :return: self
        """
        self.do('intopp/create_motion_exchange')

        featured_points=self.do('route/select_sd_point').fetchall()
        expected_problem_size=len(featured_points)**2

        # creating a matrix which will be used to store created dictionaries and write 'motion_exchange' table in SQL
        motion_exchange=[]
        for start_id,\
            end_id,\
            ring,\
            destinations_in,\
            destinations_prior,\
            sources,\
            destinations,\
            selectivity,\
            conv_start,\
            conv_size,\
            conv_intensity in TaurusLongTask(\
                                self.do('intopp/select_for_motion_exchange'),\
                                max_value=expected_problem_size,\
                                additional_text='Intervening Opportunity',\
                                **self.kwargs\
                                ):
            
            # calculating fraction of all "objects" that found destinations prior to the currently chosen ring
            fraction_before_ring=self.convolution_mix(
                destinations_prior,
                selectivity/1000000.0,
                conv_start,
                conv_size,
                conv_intensity
            )

            # calculating fraction of "objects" that found destinations prior and in the currently chosen ring
            fraction_after_ring=self.convolution_mix(
                destinations_prior+destinations_in,
                selectivity/1000000.0,
                conv_start,
                conv_size,
                conv_intensity
            )
            if destinations_in!=0:
                fraction=(fraction_after_ring-fraction_before_ring)*destinations/destinations_in
            else:
                fraction=0

            motion_exchange.append({
                'sd_start_id':start_id,
                'sd_end_id':end_id,
                'fraction':fraction,
                'motion_exchange':(sources*fraction)
            })

            if len(motion_exchange)>10000:
                self.transaction('intopp/insert_motion_exchange',motion_exchange)
                self.transaction('intopp/insert_motion_exchange_fraction',motion_exchange)
                motion_exchange=[]

        self.transaction('intopp/insert_motion_exchange',motion_exchange)
        self.transaction('intopp/insert_motion_exchange_fraction',motion_exchange)
        self.commit()


    def convolution_cdf(self,destinations,selectivity,conv_a,conv_b):

        #For recursive calls
        if destinations<=0:
            return 0

        if conv_a<0:
            offset = self.convolution_cdf(-conv_a,selectivity,0,conv_b)

            return (self.convolution_cdf(destinations-conv_a,selectivity,0,conv_b)-offset)+\
                   (offset-self.convolution_cdf(-destinations-conv_a,selectivity,0,conv_b))
        # main integral part of convolution CDF

        #before or no convolution
        if destinations<=conv_a or conv_b==0:
            return 1.0 - math.exp(-selectivity*destinations)

        if destinations>conv_a and destinations<=conv_b+conv_a:
            return self.convolution_cdf(conv_a,selectivity,conv_a,conv_b)+\
                   (math.exp(-selectivity*(conv_a+destinations))*\
                         (math.exp(selectivity*destinations)*\
                          ((-conv_a*selectivity)+(destinations*selectivity)-1.0)+\
                          math.exp(conv_a*selectivity)))/(conv_b*selectivity)

        return self.convolution_cdf(conv_a+conv_b,selectivity,conv_a,conv_b)+\
               ((1.0-math.exp(conv_b*selectivity))*\
                    math.exp(-selectivity*(conv_a+conv_b+destinations))*\
                    (math.exp(selectivity*(conv_a+conv_b))-
                     math.exp(selectivity*destinations)))/(conv_b*selectivity)


    def convolution_mix(self,sources,selectivity,conv_a,conv_b,alpha):

        assert alpha>=0.0 and alpha<=1.0
        if alpha>0:
            return self.convolution_cdf(sources,selectivity,conv_a,conv_b)*alpha+\
                   self.convolution_cdf(sources,selectivity,0,0)*(1.0-alpha)
        return self.convolution_cdf(sources,selectivity,0,0)


    def save_model_parameters(self,parameter,saved_name):
        model_parameters=[{
            "sd_id":t[0],
            "sources":t[1],
            "destinations":t[2],
            "selectivity":t[3],
            "convolution_start":t[4],
            "convolution_size":t[5],
            "convolution_intensity":t[6]
        } for t in self.do('intopp/select_model_parameters').fetchall()]

        assert parameter in model_parameters[0].keys()

        self.do('initial/clean_value',{'name':saved_name,"new_name":saved_name})

        new_value = [{
            "sd_id": parameters['sd_id'],
            "name": saved_name,
            "value": parameters[parameter]
        } for parameters in model_parameters]

        self.transaction('initial/update_sd_values',new_value)
