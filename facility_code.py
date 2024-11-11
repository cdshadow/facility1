import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

# 데이터 경로
file_paths = {
    "헬스장": 'https://raw.githubusercontent.com/cdshadow/facility/main/health.shp',
    "필라테스/요가": 'https://raw.githubusercontent.com/cdshadow/facility/main/philites_yoga.shp',
    "수영장": 'https://raw.githubusercontent.com/cdshadow/facility/main/swim.shp',
    "댄스학원": 'https://raw.githubusercontent.com/cdshadow/facility/main/dancd_academy.shp',
}

# 마커 색상 설정
marker_colors = {
    "헬스장": "red",
    "필라테스/요가": "green",
    "수영장": "blue",
    "댄스학원": "purple",
}

# Streamlit 설정
st.set_page_config(layout="wide")

# Folium 지도 생성 함수
def create_map():
    # Folium 지도 설정 (대전광역시 중심)
    map_obj = folium.Map(
        location=[36.3504, 127.3845],
        zoom_start=12,  # 줌 레벨 조정
    )

    # 파일 추가
    for name, path in file_paths.items():
        try:
            if path.endswith('.shp'):
                # 쉐이프파일 처리
                gdf = gpd.read_file(path)
                gdf = gdf.to_crs(epsg=4326)  # 좌표계 변환

                # 각 포인트를 Folium 마커로 추가
                for _, row in gdf.iterrows():
                    folium.Marker(
                        location=[row.geometry.y, row.geometry.x],
                        popup=f"{name}<br>위도: {row.geometry.y}<br>경도: {row.geometry.x}",
                        icon=folium.Icon(color=marker_colors.get(name, "gray"), icon="info-sign"),
                    ).add_to(map_obj)
            else:
                st.error(f"지원되지 않는 파일 형식입니다: {path}")
        except Exception as e:
            st.error(f"{name} 데이터를 불러오는 중 오류가 발생했습니다: {e}")

    # 레이어 컨트롤 추가
    folium.LayerControl(position='topleft').add_to(map_obj)

    return map_obj

# Streamlit 레이아웃 설정
st.title('대전광역시 체육시설 시각화')

# 지도 생성 및 출력
st.header('대전광역시 체육시설 지도')
map_display = create_map()
st_folium(map_display, width=1200, height=700)
