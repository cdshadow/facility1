import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# GitHub raw content URL의 data.csv 파일 경로
file_path = 'data.csv'

# Streamlit 설정
st.set_page_config(layout="wide")

# 데이터 파일 경로
shp_file_path_1f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/1f_2.shp'
shp_file_path_3f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/3f_2.shp'

# Folium 지도 생성 함수
def create_map():
    # Folium 지도 설정 (대전광역시 중심)
    map_obj = folium.Map(
        location=[36.3504, 127.3845],
        zoom_start=12,  # 줌 레벨 조정
    )

    # 1f.shp 파일 불러오기
    gdf_1f = gpd.read_file(shp_file_path_1f)

    # EPSG 5179에서 EPSG 4326으로 좌표계 변환
    gdf_1f = gdf_1f.to_crs(epsg=4326)

    # 1f 레이어 추가 (검정색 선, 두께 0.5)
    folium.GeoJson(
        gdf_1f,
        name='1f 레이어',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(map_obj)

    # 3f.shp 파일 불러오기
    gdf_3f = gpd.read_file(shp_file_path_3f)

    # EPSG 5179에서 EPSG 4326으로 좌표계 변환
    gdf_3f = gdf_3f.to_crs(epsg=4326)

    # 3f 레이어 추가 (검정색 선, 두께 0.5)
    folium.GeoJson(
        gdf_3f,
        name='3f 레이어',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(map_obj)

    # 레이어 컨트롤 추가
    folium.LayerControl(position='topleft').add_to(map_obj)

    return map_obj

# Streamlit 레이아웃 설정
#st.title('대전광역시 지리 정보 시각화')

# 지도 생성 및 출력
#st.header('대전광역시 지도')
map_display = create_map()
st_folium(map_display, width=1200, height=700)
