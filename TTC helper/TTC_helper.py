import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
import plotly.express as px
import requests
from xml.etree import ElementTree

from difflib import get_close_matches as gcm

kws = pd.read_csv('torontokws.csv')

kws_dict = kws.set_index('Short').to_dict()['Full']



class TTC_stop():
    
    
    
    def __init__(self, address_str):
        torontokws = [ y.upper() for x in list( kws_dict.items() ) for y in x  ]
        # directions = ['N', 'E', 'S', 'W', 'NORTH', 'EAST', 'SOUTH', 'WEST']
    
        self.address = address_str
        self.tokens = address_str.split()
        self.name_1 = None 
        self.name_2 = None 
        
        
        for token in self.tokens:
            # if token in directions:
            #     self.direction = token
            if (token not in torontokws) and (not self.name_1):
                self.name_1 = token
            elif (token not in torontokws) and (self.name_1) and (not self.name_2):
                self.name_2 = token
                
        # self.tokens = [self.name_1 , self.name_2, self.direction ]
        self.tokens = [self.name_1 , self.name_2 ]

    def compare(self, stop_obj):
        
        
        self_set = set( [self.name_1 , self.name_2])
        other_set = set([stop_obj.name_1, stop_obj.name_2])
        
        return self_set == other_set
        
class TTC_line():
    
    def __init__(self, route_tag):
        
        self.delay_record = {}
        
        self.route_tag = route_tag
        
        response = requests.get('https://retro.umoiq.com/service/publicXMLFeed?command=routeConfig&a=ttc&r='+self.route_tag)

        tree = ElementTree.fromstring(response.content)
        self.stops = {}

        for c in tree:
            for i in range(len(c)):
                if ('title' in c[i].attrib) and ('lat' in c[i].attrib) and ('lon' in c[i].attrib):
                    self.stops[ c[i].attrib['title'] ] = {'lat': c[i].attrib['lat'], 'lon': c[i].attrib['lon'] }
        
        
        
    def getDelayRecord(self, year):
      
        if self.delay_record[year]:
            return self.delay_record[year]
        
        else:
        
        
            if year == '2025':
                df = pd.read_excel('TTC Streetcar Delay Data since 2025.csv')
            else:
                df = pd.read_excel('ttc-streetcar-delay-data-'+year+'.xlsx')
            df_route = df.astype(str)[ df.astype(str)['Line'] == self.route_tag ]
                            
            LL_idx = {}
            for idx in df_route.index:
                loc_str = df_route.loc[idx]['Location']
                loc_obj = TTC_stop(loc_str)
                
                for key in self.stops:
                    if loc_obj.compare( TTC_stop( key.upper() )):
                        LL_idx[idx] = self.stops[key]

            locs_line = pd.DataFrame(LL_idx).T
            df_route['lat'] =  locs_line['lat']
            df_route['lon'] =  locs_line['lon']
            
            self.delay_record[year] = df_route
            
            return df_route 
    
    def displayDensityMap(self, year):
        
        fig = px.density_mapbox(
        self.delay_record[year],
        lat="lat",
        lon="lon",
        z="Min Delay",
        radius=2,
        center=dict(lat=43.6565799, lon=-79.37699),
        zoom=11,
        mapbox_style="open-street-map",
        height=800,
        width=1000
        )
        fig.show()
                        