import pandas as pd
from dataclasses import dataclass
from matplotlib import pyplot as plt
import numpy as np
from typing import Tuple
from typing import Dict
from math import dist, radians, cos, sin, asin, sqrt, atan2
import os

@dataclass
class Collector:
    df: pd.DataFrame
    coordinates: Dict[str, float]
    time_window: int
    mymap: np.ndarray
    BBox: Tuple[float, float, float, float]
    filter_bussines_code_class_support_acumulated: pd.DataFrame
    influence_radio: float
    business_support_into_radio_point_interest : pd.DataFrame
    def __init__(self, df, coordinates, time_window ):
        self.df = df
        self.coordinates = coordinates
        self.time_window = time_window
        # Ruta a la imagen
        self.mymap = plt.imread(os.path.join(os.path.dirname(__file__), 'static', 'images', 'map_CDNR.png'))
        self.BBox = ((-99.3686, -99.2670, 19.58, 19.65))
        self.filter_bussines_code_class_support_acumulated = self.filter_by_code_support_acumulated()
        self.influence_radio = 0.280
        self.code_poles = (465311, 812110, 463211, 461122, 722513, 467111, 461130, 461160, 311830, 311812, 722514, 461121, 464111, 722517, 561432, 467115, 811111, 722518, 722515, 722519, 621211, 332320, 461190, 813210, 465912, 466410, 468211, 531113, 713120, 811121)

    def filter_by_code_support_acumulated(self):
        codes_support = [465311, 812110, 463211, 461122, 722513, 467111, 461130, 461160, 311830, 311812, 722514, 461121, 464111, 722517, 561432, 467115, 811111, 722518, 722515, 722519, 621211, 332320, 461190, 813210, 465912, 466410, 468211, 531113, 713120, 811121]
        df_filter_general = self.df[self.df['Código de la clase de actividad SCIAN'].isin(codes_support)]
        print("INIT Time Window:", self.time_window, "  TOTAL BUSSINESS SUPPORT ACUMULATED FOUND:", len(df_filter_general))
        output_file = "./querys/distancias/reporte_distancias/filter_bussines_code_class_support_acumulated.xlsx"
        df = pd.DataFrame(df_filter_general)
        df.to_excel(output_file, index=False)
        return df

    def haversine(self, lat1, lon1, lat2, lon2):
        # Convertir grados a radianes
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Diferencias
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Fórmula de Haversine
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Radio de la Tierra en kilómetros
        radius = 6371.0

        # Distancia en kilómetros
        distance = radius * c
        return distance

    def find_business_into_radius(self):
        results = []
        negocios_dentro_radio = []
        for idx_negocio, row_negocio in self.filter_bussines_code_class_support_acumulated.iterrows():

            # Calcular la distancia entre la clase y el otro negocio
            distancia = self.haversine(self.coordinates['Latitud'], self.coordinates['Longitud'], row_negocio['Latitud'], row_negocio['Longitud'])

            # Verificar si está dentro del radio
            if distancia < self.influence_radio:
                negocios_dentro_radio.append({
                    'punto_de_interes': str(self.coordinates['Latitud'])+'_'+str(self.coordinates['Longitud']),
                    'Radio_influencia': self.influence_radio,
                    'Negocio_vecino_encontrado': row_negocio['Nombre de la Unidad Económica'],
                    'Codigo': row_negocio['Código de la clase de actividad SCIAN'],
                    'Tipo': row_negocio['Nombre de clase de la actividad'],
                    'Distancia_(m)': distancia,
                    'Longitud': row_negocio['Longitud'],
                    'Latitud': row_negocio['Latitud']
                })

        # Agregar los negocios encontrados para esta ue
        if negocios_dentro_radio:
            results.extend(negocios_dentro_radio)

        output_file = "./querys/distancias/reporte_distancias_point_interest/business_suport_acumulated_into_point_interest.xlsx"
        df = pd.DataFrame(results)
        df.to_excel(output_file, index=False)
        self.business_support_into_radio_point_interest = df

        if len(self.business_support_into_radio_point_interest) > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "businesses_support_into_radius": df.shape
            }
        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "businesses_into_radius": 'no_iter'
            }
        return response

    def plot_business_into_radius(self):
        # Cargar la imagen de fondo
        fig, ax = plt.subplots(figsize=(22, 12))

        #Plotear punto de interes
        ax.scatter(self.coordinates['Longitud'],self.coordinates['Latitud'], color='blue', label='BusinessClass',marker='o', s=20, alpha=0.99)

        #graficar radio de influencia del punto de interes
        circ = plt.Circle((self.coordinates['Longitud'], self.coordinates['Latitud']), radius=(self.influence_radio/100), color='maroon',alpha=0.2)
        ax.add_artist(circ)

        # Abrimos archivo generado de las unidades económicas base encontradas dentro del radio de influencia
        df_bussines_into_ratio = pd.read_excel('./querys/distancias/reporte_distancias_point_interest/business_suport_acumulated_into_point_interest.xlsx')

        #Plotear las unidades económicas base encontradas dentro del radio de influencia
        for idx_otros, row_f in df_bussines_into_ratio.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f, lat_f, color='red', label='BusinessClass', marker='x', s=20, alpha=0.45)

        # Configurar el gráfico
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        plt.title(f'Negocios dentro de un radio de {self.influence_radio} metros alrededor del punto de interes')
        ax.set_xlim(self.BBox[0], self.BBox[1])
        ax.set_ylim(self.BBox[2], self.BBox[3])
        ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
        plt.show()
        plt.savefig('./images_insights/plots_filter_by_code_show_plot/ratios_influence/'+str(self.coordinates['Latitud'])+'_'+str(self.coordinates['Longitud'])+'.png')

        if len(df_bussines_into_ratio):
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "plot_businesses_into_radius": df_bussines_into_ratio.shape
            }

        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "plot_businesses_into_radius": 'no_iter'
            }
        return response

    def report_accumulated_business_support(self):
        # Inicializa el DataFrame de resultados
        dfExcel = pd.DataFrame(
            columns=['Point_Latitud', 'Point_Longitud', 'Ratio_global'] + list(self.code_poles),
            index=range(len(self.filter_bussines_code_class_support_acumulated))
        )

        # Inicializa el diccionario de conteo
        types_code = {code: 0 for code in self.code_poles}
        posicion_repor = 0

        for _, iter in self.filter_bussines_code_class_support_acumulated.iterrows():
            # Crea una copia del conteo
            local_counts = types_code.copy()
            business_code = iter['Código de la clase de actividad SCIAN']

            # Verifica si el código está en los códigos de interés
            if business_code in local_counts:
                distancia = self.haversine(
                    self.coordinates['Latitud'], self.coordinates['Longitud'],
                    iter['Latitud'], iter['Longitud']
                )

                # Actualiza el conteo si está dentro del radio de influencia
                if distancia < self.influence_radio:
                    local_counts[business_code] += 1

            # Prepara la fila y la asigna en el DataFrame
            row = [self.coordinates['Latitud'], self.coordinates['Longitud'], self.influence_radio] + list(
                local_counts.values())
            dfExcel.iloc[posicion_repor] = row
            posicion_repor += 1

        # Calcula y agrega los totales
        total_counts = [self.coordinates['Latitud'], self.coordinates['Longitud'], self.influence_radio]
        total_counts.extend([dfExcel[col].sum() for col in dfExcel.columns[3:]])
        dfExcel.loc[len(dfExcel)] = total_counts

        # Guarda el DataFrame en un archivo Excel
        with pd.ExcelWriter('./querys/distancias/reporte_distancias_point_interest/report_accumulated_business_support_into_point.xlsx', engine='xlsxwriter') as writer: dfExcel.to_excel(writer, sheet_name='sheet1', index=True)

        return total_counts
