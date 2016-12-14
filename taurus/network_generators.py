#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

#from ipy_progressbar import ProgressBar
from .sqlite_database import SQLiteDatabase
from .importer import Importer
import cmath

class NetworkGenerator(Importer):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs

    def _addel(self,element,elementrel,net_geometry_to_insert,net_data_to_insert,value=1):
        start=[element.real,element.imag]
        end=[elementrel.real,elementrel.imag]
        net_geometry_to_insert.append({
            'start':str(start),
            'end':str(end),
            'linestring':str([start,end])
        })
        net_data_to_insert.append({
            'start':str(start),
            'end':str(end),
            'name':'weight',
            'value':value
        })

    def _normalize(self,points_with_data):
        dtotal=sum([point['data']['destinations'] for point in points_with_data])
        stotal=sum([point['data']['sources'] for point in points_with_data])
        for i,point in enumerate(points_with_data):
            points_with_data[i]['data']['destinations']/=dtotal
            points_with_data[i]['data']['sources']/=stotal

    def _insert_points(self,points_with_data):
        # prepare data to insert to database
        sd_geometry_to_insert=[{
            'sd_id':p['data']['sd_id'],
            'point':str(p['geometry'])
        } for p in points_with_data]

        sd_data_to_insert=[]
        for p in points_with_data:
            sd_data_to_insert.append({
                'sd_id':p['data']['sd_id'],
                'name':'destinations',
                'value':p['data']['destinations']
            })
            sd_data_to_insert.append({
                'sd_id':p['data']['sd_id'],
                'name':'sources',
                'value':p['data']['sources']
            })

        # insert data to database
        self.transaction('initial/import_sd_geometry',sd_geometry_to_insert)
        self.transaction('initial/import_sd_properties',sd_data_to_insert)

    def make_trianglehex_pattern_network(self,size,delta=0.0001):

        self.do('initial/create_network')
        self.do('initial/create_sd')


        rows=[]
        vector=cmath.rect(1,cmath.pi/3)
        p=complex(0,0)
        rows.append([[p]])
        ring_generator=p
        for ring in range(size):
            r=[]
            ring_generator+=complex(1,0)
            for prt in range(6):
                prtl=[]
                for e in range(ring+1):
                    point=(ring_generator*vector**prt+vector*vector*e*vector**prt)*delta
                    prtl.append(point)

                r.append(prtl)
            rows.append(r)

        points=[]
        for row in rows:
            for part in row:
                for point in part:
                    points.append(point)

        # Let add some data to geometries
        points_with_data= [{
            'geometry':[point.real,point.imag],
            'data':{
                'sd_id':i,
                'sources':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        net_geometry_to_insert=[]
        net_data_to_insert=[]

        for p1 in points:
            for p2 in points:
                if p1!=p2 and abs(p1-p2)<delta*1.1:
                    self._addel(p1,p2,net_geometry_to_insert,net_data_to_insert)

        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_sd()


    def make_hexdiagonal_pattern_network(self,size,delta=0.0001):

        self.do('initial/create_network')
        self.do('initial/create_sd')


        rows=[]
        vector=cmath.rect(1,cmath.pi/3)
        p=complex(0,0)
        row_generator=p
        additional=0
        for r_no in range(size*4+1):
            r=[]
            for e in range(size*2+additional+1):
                point=(row_generator+(e)*complex(1,0))*delta
                r.append(point)
            rows.append(r)
            if r_no < size*2:
                additional+=1
                row_generator+=vector**2
            else:
                additional-=1
                row_generator+=vector

        #reget points
        points=[]
        for row in rows:
            for point in row:
                points.append(point)

        # Let add some data to geometries
        points_with_data=[{
            'geometry':[point.real,point.imag],
            'data':{
                'sd_id':i,
                'sources':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        net_geometry_to_insert=[]
        net_data_to_insert=[]
        def add_edge_possibility(rows,old_row,old_elemet,new_row,new_element):
            if new_row>=0 and new_row<len(rows) and new_element>=0 and new_element<len(rows[new_row]):
                if abs(rows[old_row][old_elemet]-rows[new_row][new_element])>delta*1.1:
                    self._addel(
                        rows[old_row][old_elemet],
                        rows[new_row][new_element],
                        net_geometry_to_insert,
                        net_data_to_insert,
                        (3**0.5)/2)
                else:
                    self._addel(
                        rows[old_row][old_elemet],
                        rows[new_row][new_element],
                        net_geometry_to_insert,
                        net_data_to_insert)

        for i,r in enumerate(rows):
            downo=-1
            upo=-1
            if i<len(rows)//2:
                upo=1
            if i>len(rows)//2:
                downo=1

            for j,element in enumerate(r):

                if i%2==0 and j%2==1:
                    add_edge_possibility(rows,i,j,i+2,j+upo)
                    add_edge_possibility(rows,i,j,i-2,j+downo)
                    add_edge_possibility(rows,i,j,i,j+1)
                    add_edge_possibility(rows,i,j,i,j-1)

                if (i<len(rows)//2 and i%2!=0 and j%2!=0) or \
                    (i>len(rows)//2 and i%2!=0 and j%2==0):
                    add_edge_possibility(rows,i,j,i+1,j+(upo+1)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo-1)//2)
                    add_edge_possibility(rows,i,j,i+1,j+(upo-3)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo+3)//2)

                if (i<len(rows)//2 and i%2!=0 and j%2==0) or \
                    (i>len(rows)//2 and i%2!=0 and j%2!=0):
                    add_edge_possibility(rows,i,j,i+1,j+(upo-1)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo+1)//2)
                    add_edge_possibility(rows,i,j,i+1,j+(upo+3)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo-3)//2)

                if i%2==0 and j%2==0:
                    add_edge_possibility(rows,i,j,i+2,j+upo)
                    add_edge_possibility(rows,i,j,i-2,j+downo)
                    add_edge_possibility(rows,i,j,i,j+1)
                    add_edge_possibility(rows,i,j,i,j-1)

                    add_edge_possibility(rows,i,j,i+1,j+(upo-1)//2)
                    add_edge_possibility(rows,i,j,i+1,j+(upo-3)//2)
                    add_edge_possibility(rows,i,j,i+1,j+(upo+1)//2)
                    add_edge_possibility(rows,i,j,i+1,j+(upo+3)//2)

                    add_edge_possibility(rows,i,j,i-1,j+(downo-1)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo-3)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo+1)//2)
                    add_edge_possibility(rows,i,j,i-1,j+(downo+3)//2)

        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_sd()




    def make_hex_pattern_network(self,size,delta=0.0001):
        '''
        Creates hexagonal pattern network. HEXAGONS binded together by edge (like square pattern but with hexagons)
        Creates also corresponding sources - destinations points.
        Sources - destinations are set in way their total sum is 1 for sources and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.
        Don't use it for

        :param size: How many lines to create on side. 1 by 1 lines create just a hexagon with point inside.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_sd')

        # main Point generator part

        points=[]
        rows=[]

        vector=cmath.rect(1,cmath.pi/6)
        p=complex(0,0)
        row_generator=p
        k_top=size
        for row in range(size+1):
            r=[]
            vector=vector.conjugate()
            if row==size and size%2==0:
                row_generator+=vector
                vector=vector.conjugate()
                k_top-=1
            r.append(row_generator*delta)
            for e in range(k_top):
                point=(row_generator+e*(vector.conjugate()+vector)+vector)*delta
                r.append(point)
                point=(row_generator+(e+1)*(vector.conjugate()+vector))*delta
                r.append(point)

            rows.append(r)
            row_generator+=complex(0,1)*(1+row%2)

        for row in rows:
            for point in row:
                    points.append(point)

        # Let add some data to geometries
        points_with_data=[{
            'geometry':[point.real,point.imag],
            'data':{
                'sd_id':i,
                'sources':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        net_geometry_to_insert=[]
        net_data_to_insert=[]

        for p1 in points:
            for p2 in points:
                if p1!=p2 and abs(p1-p2)<delta*1.1:
                    self._addel(p1,p2,net_geometry_to_insert,net_data_to_insert)

        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_sd()


    def make_square_pattern_network(self,size,delta=0.0001):
        '''
        Creates square pattern network.
        Creates also corresponding sources - destinations points.
        Sources - destinations are set in way their total sum is 1 for sources and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.
        Don't use it for

        :param size: How many lines to create. 1 by 1 lines create just a square.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_sd')

        # main Point generator part

        points=[]
        rows=[]
        for y in range(size+1):
            row=[]
            for x in range(size+1):
                point=complex(x*delta,y*delta)
                row.append(point)
                points.append(point)
            rows.append(row)

        # Let add some data to geometries
        points_with_data=[{
            'geometry':[point.real,point.imag],
            'data':{
                'sd_id':i,
                'sources':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        # Part where we create network
        net_geometry_to_insert=[]
        net_data_to_insert=[]

        for y,row in enumerate(rows):
            for x,element in enumerate(row):
                if y!=0:
                    self._addel(element,rows[y-1][x],net_geometry_to_insert,net_data_to_insert)
                if y!=len(rows)-1:
                    self._addel(element,rows[y+1][x],net_geometry_to_insert,net_data_to_insert)
                if x!=0:
                    self._addel(element,rows[y][x-1],net_geometry_to_insert,net_data_to_insert)
                if x!=len(row)-1:
                    self._addel(element,rows[y][x+1],net_geometry_to_insert,net_data_to_insert)

        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_sd()






