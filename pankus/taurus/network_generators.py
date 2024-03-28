#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Wawrzyniec Zipser, Maciej Kamiński Politechnika Wrocławska'

from .sqlite_database import SQLiteDatabase
from .importer import Importer
from .utils import init_kwargs_as_parameters
from itertools import accumulate
import cmath,math

class NetworkGenerator(Importer):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    # adding new rows to tables: network_geometry and network_properties, these new rows contain data on specified segments connecting points in the network
    def _addel(self,element,elementrel,net_geometry_to_insert,net_data_to_insert,value=1):
        """
        function "addel" adds new rows to tables: network_geometry and network_properties,
        these new rows contain data on specified segments connecting points in the network
        :param element:
        :param elementrel:
        :param net_geometry_to_insert:
        :param net_data_to_insert:
        :param value:
        :return:
        """
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
            'name':'cost',
            'value':value
        })
    # normalization brings numbers of origins and destinations to a fractional form, new sums of origins and ddestinations equal 1
    def _normalize(self,points_with_data):
        """
        normalization brings numbers of origins and destinations to a fractional forms, new sums of origins and destinations equal 1
        :param points_with_data:
        :return:
        """
        dtotal=sum([point['data']['destinations'] for point in points_with_data])
        stotal=sum([point['data']['origins'] for point in points_with_data])
        for i,point in enumerate(points_with_data):
            points_with_data[i]['data']['destinations']/=dtotal
            points_with_data[i]['data']['origins']/=stotal

    # preparing points data stored in the dictionary 'points_with_data' to be inserted in the "od_geometry" (columns 'od_id' - identificational number of a origin-destination point and 'geometry' - coordinates of the point) and "od_properties" (columns 'od_id' -   identificational number of a origin-destination point, 'name' - name of a parameter describing that point and 'value' - value of the parameter) tables. The construction of "od_properties" table allows later to add new parameters to specific points without creating new columns
    def _insert_points(self,points_with_data):
        # prepare data to insert to database
        """
        function "_insert_points" prepares point data in the dictionary 'points_with_data' to be inserted in the "od_geometry" and "od_properties" tables.
        The construction of "od_properties" table allows later to add new parameters to specific points without creating new columns
        :param points_with_data:
        :return:
        """
        od_geometry_to_insert=[{
            'od_id':p['data']['od_id'],
            'point':str(p['geometry'])
        } for p in points_with_data]

        od_data_to_insert=[]
        for p in points_with_data:
            od_data_to_insert.append({
                'od_id':p['data']['od_id'],
                'name':'destinations',
                'value':p['data']['destinations']
            })
            od_data_to_insert.append({
                'od_id':p['data']['od_id'],
                'name':'origins',
                'value':p['data']['origins']
            })

        # running SQL scripts filling existing tables with the data created earlier
        self.transaction('initial/import_od_geometry',od_geometry_to_insert)
        self.transaction('initial/import_od_properties',od_data_to_insert)

    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_hexhorny_pattern_network(self,size,delta=0.0001,**kwargs):

        self.do('initial/create_network')
        self.do('initial/create_od')

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
        #ring generator at last ring init point
        to_delete_size=len(rows[-1][0])-1
        to_delete_offset=1
        for ringnumber,ring in enumerate(reversed(rows)):
            for prt_nb,prt in enumerate(ring):
                if to_delete_size>0:
                    ring[prt_nb]=ring[prt_nb][:to_delete_offset]+ring[prt_nb][to_delete_offset+to_delete_size:]
            to_delete_offset+=1
            to_delete_size-=3

        points=[]
        for row in rows:
            for part in row:
                for point in part:
                    points.append(point)


        # Let add some data to geometries
        points_with_data= [{
            'geometry':[point.real,point.imag],
            'data':{
                'od_id':i,
                'origins':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        net_geometry_to_insert=[]
        net_data_to_insert=[]

        for i,r in enumerate(rows):
            if i==0:
                continue
            for j,part in enumerate(r):
                for k,element in enumerate(part):
                    if ((size*2)//3)>=i:
                        # connections in row
                        if k==0:
                            self._addel(rows[i][j][k],rows[i][j-1][-1],net_geometry_to_insert,net_data_to_insert)
                            self._addel(rows[i][j-1][-1],rows[i][j][k],net_geometry_to_insert,net_data_to_insert)
                        else:
                            self._addel(rows[i][j][k],rows[i][j][k-1],net_geometry_to_insert,net_data_to_insert)
                            self._addel(rows[i][j][k-1],rows[i][j][k],net_geometry_to_insert,net_data_to_insert)

                    if i-1==0:
                        # connections to 00
                        self._addel(rows[i][j][k],rows[i-1][0][0],net_geometry_to_insert,net_data_to_insert)
                        self._addel(rows[i-1][0][0],rows[i][j][k],net_geometry_to_insert,net_data_to_insert)
                    elif (len(part)/2)>k and i>1:
                        self._addel(rows[i][j][k],rows[i-1][j][k],net_geometry_to_insert,net_data_to_insert)
                        self._addel(rows[i-1][j][k],rows[i][j][k],net_geometry_to_insert,net_data_to_insert)
                    elif len(part)/2<k and i>1:
                        l=len(part)-k
                        self._addel(rows[i][j][k],rows[i-1][j][-l],net_geometry_to_insert,net_data_to_insert)
                        self._addel(rows[i-1][j][-l],rows[i][j][k],net_geometry_to_insert,net_data_to_insert)
                    else:
                        pass

        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_od()


    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_trianglehex_pattern_network(self,size,delta=0.0001,**kwargs):

        self.do('initial/create_network')
        self.do('initial/create_od')


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
                'od_id':i,
                'origins':1,
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
        self.point_from_network_od()

    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_hexdiagonal_pattern_network(self,size,delta=0.0001,**kwargs):

        self.do('initial/create_network')
        self.do('initial/create_od')


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
                'od_id':i,
                'origins':1,
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
        self.point_from_network_od()



    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_hex_pattern_network(self,size,delta=0.0001,**kwargs):
        '''
        Creates hexagonal pattern network. HEXAGONS binded together by edge (like square pattern but with hexagons)
        Creates also corresponding origins - destinations points.
        origins - destinations are set in way their total sum is 1 for origins and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.
        Don't use it for

        :param size: How many lines to create on side. 1 by 1 lines create just a hexagon with point inside.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_od')

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
                'od_id':i,
                'origins':1,
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
        self.point_from_network_od()

    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_square_pattern_network(self,size,delta=0.0001,**kwargs):
        '''
        Creates square pattern network.
        Coresponding origins - destinations points are also created.
        origins - destinations are set in way their total sum is 1 for origins and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.
        Don't use it for

        :param size: How many lines to create. 1 by 1 lines create just a square.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_od')

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
                'od_id':i,
                'origins':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        # Creating network. Data from the matrix created earlier is prepared to be written in the "network_geometry" and "network_properties" tables by being written into net_geometry_to_insert and net_data_to_insert tables. Then SQL scripts use the prepared data to insert it in the network_geometry" and "network_properties" tables.
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
        self.point_from_network_od()

    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_trihexhex_pattern_network(self,size,delta=0.0001,**kwargs):
        '''
        Creates trihexhex pattern network.
        mede out of tri-hexagons layers round tri-hexagon
        Coresponding origins - destinations points are also created.
        origins - destinations are set in way their total sum is 1 for origins and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.

        :param size: How many layers to create. 1 by 1 lines create just a square.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_od')

        # main Point generator part
        points=[]
        rows=[]
        vector=cmath.rect(1,cmath.pi/6) # single vector of 1/12 circle
        v=vector
        vcon=v.conjugate()

        p=complex(0,0)

        points.append(p)

        row_starting_point=[1]
        row_starting_point+=[2,1]*size
        row_starting_point=list(accumulate(row_starting_point))
        row_starting_point=[(-vcon)*i for i in row_starting_point]

        row_type=[1]
        row_type+=[(i+1)*3+1 for i in range(size)]
        row_type+=list(reversed([1-(i+1)*3 for i in range(size)]))
        row_type=list(reversed(row_type))

        row_generator=[3]*(size+1) # not a point
        row_generator[0]-=1
        row_generator[-1]-=1
        row_generator=list(accumulate(row_generator))
        row_generator=[(-vcon)*i for i in row_generator]

        for rg_i,rg in enumerate(row_generator):
            rg=rg+complex(0,1)
            r=rg
            row=[r]
            u,d = v,v.conjugate()
            if row_type[rg_i]<0:
                u,d=d,u
            for i in range(abs(row_type[rg_i])):
                r+=u
                row.append(r)
                r+=d
                row.append(r)

            rows.append(row)
        del(row_type[0:len(row_generator)])
        u,d = v,v.conjugate()
        for rt in row_type:
            rg+=3*v
            r=rg
            row=[r]
            for i in range(rt):
                r+=u
                row.append(r)
                r+=d
                row.append(r)
            rows.append(row)


        for turn in [1,v**4,v**8]:
            for row in rows:
                for point in row:
                    points.append(turn*point*delta)
            for point in row_starting_point:
                points.append(turn*point*delta)

        # Let add some data to geometries
        points_with_data=[{
            'geometry':[point.real,point.imag],
            'data':{
                'od_id':i,
                'origins':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)

        # Creating network. Data from the matrix created earlier is prepared to be written in the "network_geometry" and "network_properties" tables by being written into net_geometry_to_insert and net_data_to_insert tables. Then SQL scripts use the prepared data to insert it in the network_geometry" and "network_properties" tables.
        net_geometry_to_insert=[]
        net_data_to_insert=[]

        for p1 in points:
            for p2 in points:
                if p1!=p2 and abs(p1-p2)<delta*1.1:
                    self._addel(p1,p2,net_geometry_to_insert,net_data_to_insert)

        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_od()


    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_octagonlike_square_pattern_network(self,size,delta=0.0001,**kwargs):
        '''
        Creates octagon looked like pattern network mede out of squares.
        Coresponding origins - destinations points are also created.
        origins - destinations are set in way their total sum is 1 for origins and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.

        :param size: How many layers to create. 1 by 1 lines create just a square.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_od')

        # main Point generator part
        points=[]
        rows=[]
        points.append(complex(0,0))
        vector=complex(0,1) # single vector of 1/12 circle
        row_type=[(i+1)*2 for i in range(size+1)]
        row_type=[(i+1)*2 for i in range(size+1)]
        row_type+=[row_type[-1]]
        for i in range(size):
            row_type+=[row_type[-1]+1,row_type[-1]+1]
        del(row_type[-1])
        row_type=list(reversed(row_type))
        row_generator=[(i+1)*vector for i in range(len(row_type))]

        while row_type!=[]:
            row=[row_generator[0]+i for i in range(row_type[0]) ]

            rows.append(row)
            del(row_generator[0])
            del(row_type[0])
        parts=[
            [
                [
                    point*part*delta
                    for point in row
                ]
                for row in rows
            ]
            for part in [1,vector,vector**2,vector**3]
        ]
        net_geometry_to_insert=[]
        net_data_to_insert=[]

        # Creating network. Data from the matrix created earlier is prepared to be written in the "network_geometry" and "network_properties" tables by being written into net_geometry_to_insert and net_data_to_insert tables. Then SQL scripts use the prepared data to insert it in the network_geometry" and "network_properties" tables.

        for part_idx,rows in enumerate(parts):
            self._addel(
                parts[part_idx][0][0],
                points[0],
                net_geometry_to_insert,net_data_to_insert)
            self._addel(
                points[0],
                parts[part_idx][0][0],
                net_geometry_to_insert,net_data_to_insert)
            for row_idx,row in enumerate(rows):
                for point_idx,point in enumerate(row):
                    if row_idx!=0:
                        self._addel(
                            parts[part_idx][row_idx][point_idx],
                            parts[part_idx][row_idx-1][point_idx],
                            net_geometry_to_insert,net_data_to_insert)
                        self._addel(
                            parts[part_idx][row_idx-1][point_idx],
                            parts[part_idx][row_idx][point_idx],
                            net_geometry_to_insert,net_data_to_insert)
                    if point_idx!=0:
                        self._addel(
                            parts[part_idx][row_idx][point_idx],
                            parts[part_idx][row_idx][point_idx-1],
                            net_geometry_to_insert,net_data_to_insert)
                        self._addel(
                            parts[part_idx][row_idx][point_idx-1],
                            parts[part_idx][row_idx][point_idx],
                            net_geometry_to_insert,net_data_to_insert)
                    if point_idx==0:
                        self._addel(
                            parts[(part_idx+1)%4][0][row_idx+1],
                            parts[part_idx][row_idx][0],
                            net_geometry_to_insert,net_data_to_insert)
                        self._addel(
                            parts[part_idx][row_idx][0],
                            parts[(part_idx+1)%4][0][row_idx+1],
                            net_geometry_to_insert,net_data_to_insert)

                    points.append(point)


        # Let add some data to geometries
        points_with_data=[{
            'geometry':[point.real,point.imag],
            'data':{
                'od_id':i,
                'origins':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)


        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_od()


    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_snowflake_pattern_network(self,size,delta=0.0001,**kwargs):
        '''
        Creates snowflake looked like pattern network.
        Coresponding origins - destinations points are also created.
        origins - destinations are set in way their total sum is 1 for origins and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.

        :param size: How many layers to create. 1 by 1 lines create just a square.
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_od')

        # main Point generator part
        points=[]
        rows=[]
        points.append(complex(0,0))
        vector=cmath.rect(1,cmath.pi/3) # single vector of 1/6 circle

        rows.append([1]) # 1 elements inner # connected to outgoing rows
        rows.append([vector+1]) # 1 elements outer
        rows.append([i+2 for i in range(size)])
        rows.append([i+2+vector for i in range(size)])
        rows.append([i+2+vector.conjugate() for i in range(size)])
        rows.append([i+2+size for i in range(size)])

        parts=[
            [
                [
                    point*part*delta
                    for point in row
                ]
                for row in rows
            ]
            for part in [1,vector,vector**2,vector**3,vector**4,vector**5]
        ]
        net_geometry_to_insert=[]
        net_data_to_insert=[]


        for part_idx,rows in enumerate(parts):
            self._addel(
                parts[part_idx][0][0],
                points[0],
                net_geometry_to_insert,net_data_to_insert)
            self._addel(
                points[0],
                parts[part_idx][0][0],
                net_geometry_to_insert,net_data_to_insert)

            self._addel(
                parts[part_idx][0][0],
                parts[part_idx][1][0],
                net_geometry_to_insert,net_data_to_insert)
            self._addel(
                parts[part_idx][1][0],
                parts[part_idx][0][0],
                net_geometry_to_insert,net_data_to_insert)

            self._addel(
                parts[part_idx][1][0],
                parts[(part_idx+1)%6][0][0],
                net_geometry_to_insert,net_data_to_insert)
            self._addel(
                parts[(part_idx+1)%6][0][0],
                parts[part_idx][1][0],
                net_geometry_to_insert,net_data_to_insert)

            for point_idx,point in enumerate(rows[2]):
                if point_idx!=0:
                    self._addel(
                        rows[2][point_idx],
                        rows[2][point_idx-1],
                        net_geometry_to_insert,net_data_to_insert)
                    self._addel(
                        rows[2][point_idx-1],
                        rows[2][point_idx],
                        net_geometry_to_insert,net_data_to_insert)
                else:
                    self._addel(
                        rows[2][0],
                        rows[0][0],
                        net_geometry_to_insert,net_data_to_insert)
                    self._addel(
                        rows[0][0],
                        rows[2][0],
                        net_geometry_to_insert,net_data_to_insert)

                self._addel(
                    rows[2][point_idx],
                    rows[3][point_idx],
                    net_geometry_to_insert,net_data_to_insert)
                self._addel(
                    rows[3][point_idx],
                    rows[2][point_idx],
                    net_geometry_to_insert,net_data_to_insert)

                self._addel(
                    rows[2][point_idx],
                    rows[4][point_idx],
                    net_geometry_to_insert,net_data_to_insert)
                self._addel(
                    rows[4][point_idx],
                    rows[2][point_idx],
                    net_geometry_to_insert,net_data_to_insert)
            for point_idx,point in enumerate(rows[5]):
                if point_idx!=0:
                    self._addel(
                        rows[5][point_idx],
                        rows[5][point_idx-1],
                        net_geometry_to_insert,net_data_to_insert)
                    self._addel(
                        rows[5][point_idx-1],
                        rows[5][point_idx],
                        net_geometry_to_insert,net_data_to_insert)
                else:
                    self._addel(
                        rows[5][0],
                        rows[2][-1],
                        net_geometry_to_insert,net_data_to_insert)
                    self._addel(
                        rows[2][-1],
                        rows[5][0],
                        net_geometry_to_insert,net_data_to_insert)

        points+=[point for part in parts for row in part for point in row]

        # Let add some data to geometries
        points_with_data=[{
            'geometry':[point.real,point.imag],
            'data':{
                'od_id':i,
                'origins':1,
                'destinations':1
            }
        } for i,point in enumerate(points)]

        # Data normalization
        self._normalize(points_with_data)

        #insert
        self._insert_points(points_with_data)


        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_od()

    @init_kwargs_as_parameters
    @Importer.log_and_stash("network_properties", "network_geometry")
    def make_triangular_catenary_pattern_network(self,size,delta=1,**kwargs):
        '''
        Creates triangular catenary (T. Zipser) pattern network.
        Coresponding origins - destinations points are also created.
        origins - destinations are set in way their total sum is 1 for origins and destinations.
        Points for abstract network are generated in WSG84 coordinate system starting at point (0,0).
        On this level we use globe WSG84 as a Carthesian coordinates system.

        :param size: Size
        :param delta: Network relative (to earth WSG84) size.
        :return:
        '''
        self.do('initial/create_network')
        self.do('initial/create_od')

        # main Point generator part
        net_geometry_to_insert=[]
        net_data_to_insert=[]
        points_with_data=[]
        
        point_geoms=set()
        od_geoms=set()
        
        def gb(c):
            return complex(int(round(c.real,10)*1024)/1024*delta,int(round(c.imag,10)*1024)/1024*delta)
        def pwd(c,o,d,i):
            gc=gb(c)
            if gc not in od_geoms:
                od_geoms.add(gc)
                points_with_data.append({
                    'data':{
                        'od_id':i,
                        'destinations':d,
                        'origins':o
                        },
                    'geometry':[gc.real,gc.imag]
                    })
        def con(x,y,w):
            gx,gy=gb(x),gb(y)
            if (gx,gy) not in point_geoms:
                point_geoms.add((gx,gy))
                point_geoms.add((gy,gx))
                self._addel(gx,gy,net_geometry_to_insert,net_data_to_insert,w)
                self._addel(gy,gx,net_geometry_to_insert,net_data_to_insert,w)



        vector=cmath.rect(1,cmath.pi/3) # single vector of 1/6 circle
        qvector=cmath.rect(1,cmath.pi/12)
        vq=complex(1,cmath.tan(cmath.phase(qvector))*1)
        vv=complex(1,cmath.tan(cmath.phase(qvector**2))*1)

        # lets create hexagons centers
        generator_points=[]
        row_generator=complex(0,0)
        for i in range(size):
            generator_points+=[row_generator + i for i in range(size)]
            if i%2==0:
                row_generator+=vector
            else:
                row_generator+=vector**2

        
        for i,g in enumerate(generator_points):
            #create centre
            c=g+(vector**(6/5))/33
            
            for j in range(6):
                base=vector**(j)*1/2
                rbase=base*1/20
                p1=g+base
                p2=g+base*vq
                p3=g+base*vv
                p4=g+base*vq*qvector**2
                p5=g+base*vector
                
                p10=g+rbase*8
                p9=g+rbase*8*qvector
                p8=g+rbase*8*qvector**2
                p7=g+rbase*8*qvector**3
                p6=g+rbase*8*qvector**4
                
                p11=g+rbase*11*qvector
                p12=g+rbase*14*qvector
                p13=g+rbase*17*qvector

                p14=g+rbase*11*qvector**3
                p15=g+rbase*14*qvector**3
                p16=g+rbase*17*qvector**3

                h1=math.tan(math.pi/12)
                h2=math.tan(math.pi/6)
                
                # connections
                con(p1,p10,12/20*0.5*100)
                con(p1,p2,h1*0.5*100)
                con(p2,p3,(h2-h1)*0.5*100)
                con(p3,p4,(h2-h1)*0.5*100)
                con(p4,p5,h1*0.5*100)
                con(p5,p6,12/20*0.5*100)
                con(c,p7,8/20*0.5*1.4*100) # 

                sr=2*cmath.pi*8/20*0.5*1/24*100

                con(p6,p7,sr)
                con(p7,p8,sr)
                con(p8,p9,sr)
                con(p9,p10,sr)

                con(p8,p3,((h2*2)-(8/20))*0.5*100)
                
                s=(1/math.cos(math.pi/6)-8/20)*1/4*0.5*1.6*100
                
                con(p2,p13,s)
                con(p12,p13,s)
                con(p12,p11,s)
                con(p10,p11,s)

                con(p4,p16,s)
                con(p15,p16,s)
                con(p15,p14,s)
                con(p6,p14,s)
                # od points
                cp=int(1000000*2/17)
                l= 900000/36
                ll=100000*2/5
                pwd(c,ll,cp,i*9*6+j*9+0)
                pwd(p2,ll/4,cp/4,i*9*6+j*9+1)
                pwd(p4,ll/4,cp/4,i*9*6+j*9+2)
                pwd(p11,l,cp/6,i*9*6+j*9+3)
                pwd(p12,l,cp/6,i*9*6+j*9+4)
                pwd(p13,l,cp/6,i*9*6+j*9+5)
                pwd(p14,l,cp/6,i*9*6+j*9+6)
                pwd(p15,l,cp/6,i*9*6+j*9+7)
                pwd(p16,l,cp/6,i*9*6+j*9+8)

        #insert
        self._insert_points(points_with_data)


        self.transaction('initial/import_network_geometry',net_geometry_to_insert)
        self.transaction('initial/import_network_properties',net_data_to_insert)
        self.point_from_network_od()
