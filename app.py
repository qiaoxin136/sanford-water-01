import streamlit as st
import pydeck
import pandas as pd
from streamlit_option_menu import option_menu

INITIAL_VIEW_STATE = pydeck.ViewState(latitude=35.4799, longitude=-79.1803, controller=True,zoom=12, max_zoom=24, pitch=0, bearing=0)

st.set_page_config(
    page_title='Sanford Water System',
    layout='wide',
    page_icon='🌍'
)

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1


def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Home", "MDD", "Quality", "Fire",  "I-Hydrant"],  # required
                icons=["house", "shield-check", "brilliance", "water", "pass", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "MDD", "Quality", "Fire",  "I-Hydrant"],  # required
            icons=["house", "shield-check","brilliance", "water","pass", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "MDD", "Quality", "Fire",  "I-Hydrant"],  # required
            icons=["house", "shield-check","brilliance", "water","pass", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected

st.image("sanford.png")
selected = streamlit_menu(example=EXAMPLE_NO)

mdd = pd.read_csv(
    "MDD.csv",
    header=0,
    names=[
        "DEMAND",
        "HEAD",
        "PRESSURE",
        "LAT",
        "LON",
    ],
)

mdd["size"] = mdd.PRESSURE/50

tank = pd.read_csv(
    "tank.csv",
    header=0,
    names=[
        "Name",
        "Lat",
        "Lon",
        "Volume",
        "Overflow",
    ],
)

pump = pd.read_csv(
    "pump.csv",
    header=0,
    names=[
        "Name",
        "Lat",
        "Lon",
        "Capacity"
    ],
)

ihydrant=pd.read_csv("IHydrant.csv")
fireflow=pd.read_csv("fireflow.csv")
waterage=pd.read_csv("waterage.csv")
mdd_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=mdd,
    id="cities",
    get_position=["LON", "LAT"],
    get_color="[255, 75, 75]",
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

pipe_layer = pydeck.Layer(
    "MVTLayer",
    data="https://a.tiles.mapbox.com/v4/hazensawyer.cx9utjpr/{z}/{x}/{y}.vector.pbf?access_token=pk.eyJ1IjoiaGF6ZW5zYXd5ZXIiLCJhIjoiY2xmNGQ3MDgyMTE3YjQzcnE1djRpOGVtNiJ9.U06GItbSVWFTsvfg9WwQWQ",
    get_line_color=[0, 163, 108],
    get_fill_color=[155, 0, 100],
    line_width_min_pixels=2,
    pickable=True,
    id="pipe"
)

tank_layer = pydeck.Layer(
    type="ScatterplotLayer",
    data=tank,
    id="tank",
    #get_icon="https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png",
    get_position=["Lon", "Lat"],
    get_color="[4, 55, 242]",
    pickable=True,
    auto_highlight=True,
    #get_radius=50,
    radiusUnits=50, 
    radiusScale=5
)

tanktext_layer = pydeck.Layer(
    type="TextLayer",
    data=tank,
    id="tanktext",
    get_position=["Lon", "Lat"],
    get_color="[4, 55, 242]",
    getText="Name",
    pickable=True,
    auto_highlight=True,
    getPixelOffset="[5,5]", 
    get_size=12,
)


pump_layer = pydeck.Layer(
    type="ScatterplotLayer",
    data=pump,
    id="pump",
    get_position=["Lon", "Lat"],
    get_color="[191, 64, 191]",
    pickable=True,
    auto_highlight=True,
    radiusUnits=50, 
    radiusScale=5
)

pumptext_layer = pydeck.Layer(
    type="TextLayer",
    data=pump,
    id="pumptext",
    get_position=["Lon", "Lat"],
    get_color="[191, 64, 191]",
    getText="Name",
    pickable=True,
    auto_highlight=True,
    getPixelOffset="[5,5]", 
    get_size=12,
)

ihydrant_layer = pydeck.Layer(
    type="ScatterplotLayer",
    data=ihydrant,
    id="ihydrant",
    get_position=["LON", "LAT"],
    get_color="[210, 43, 43]",
    pickable=True,
    auto_highlight=True,
    radiusUnits=50, 
    radiusScale=7
)

fireflow_layer = pydeck.Layer(
    type="ScatterplotLayer",
    data=fireflow,
    id="fireflow",
    get_position=["LON", "LAT"],
    get_color="[248, 131, 121]",
    pickable=True,
    auto_highlight=True,
    radiusUnits=50, 
    radiusScale=5,
)

waterage_layer = pydeck.Layer(
    type="ScatterplotLayer",
    data=waterage,
    id="waterage",
    get_position=["LON", "LAT"],
    get_color="[227, 11, 92]",
    pickable=True,
    auto_highlight=True,
    radiusUnits=50, 
    radiusScale=5,
)


if selected == "Home":
    st.markdown(f"#### Sanford Water Distribution System")
    chart = pydeck.Deck(
    [pipe_layer, tank_layer, tanktext_layer, pump_layer, pumptext_layer],
    initial_view_state=INITIAL_VIEW_STATE,
    map_style="mapbox://styles/hazensawyer/clnlt5te9003l01p5fta3hjc8", 
    api_keys={"mapbox": "pk.eyJ1IjoiaGF6ZW5zYXd5ZXIiLCJhIjoiY2xmNGQ3MDgyMTE3YjQzcnE1djRpOGVtNiJ9.U06GItbSVWFTsvfg9WwQWQ"},
    tooltip={"text": "Diameter: {Diameter}\nMaterial: {Material}\nAge: {Age}\n Installation Year: {InstallDat}"},
)

    event = st.pydeck_chart(chart, on_select="rerun", selection_mode="single-object")

    st.write("Please hover the pipe to see the attributes")

if selected == "MDD":
    st.markdown(f"#### Maximum Day Demand Condition")
    chart = pydeck.Deck(
    [pipe_layer, tank_layer, tanktext_layer, pump_layer, pumptext_layer, mdd_layer],
    initial_view_state=INITIAL_VIEW_STATE,
    map_style="mapbox://styles/hazensawyer/clnlt5te9003l01p5fta3hjc8", 
    api_keys={"mapbox": "pk.eyJ1IjoiaGF6ZW5zYXd5ZXIiLCJhIjoiY2xmNGQ3MDgyMTE3YjQzcnE1djRpOGVtNiJ9.U06GItbSVWFTsvfg9WwQWQ"},
    tooltip={"text": "Diameter: {Diameter}\nMaterial: {Material}\nAge: {Age}\n Installation Year: {InstallDat}"},
)

    event = st.pydeck_chart(chart, on_select="rerun", selection_mode="single-object")

    st.write("Please click the node to see the pressure")
    if(len(event.selection.objects)>0):
        st.write("Head (ft): ", event.selection.objects.cities[0].get("HEAD"))
        st.write("Pressure (psi)", event.selection.objects.cities[0].get("PRESSURE"))
if selected == "Fire":
    st.markdown(f"#### Fire Flow Availability")
    chart = pydeck.Deck(
    [pipe_layer, tank_layer, tanktext_layer, pump_layer, pumptext_layer, fireflow_layer],
    initial_view_state=INITIAL_VIEW_STATE,
    map_style="mapbox://styles/hazensawyer/clnlt5te9003l01p5fta3hjc8", 
    api_keys={"mapbox": "pk.eyJ1IjoiaGF6ZW5zYXd5ZXIiLCJhIjoiY2xmNGQ3MDgyMTE3YjQzcnE1djRpOGVtNiJ9.U06GItbSVWFTsvfg9WwQWQ"},
    tooltip={"text": "Diameter: {Diameter}\nMaterial: {Material}\nAge: {Age}\n Installation Year: {InstallDat}"},
)

    event = st.pydeck_chart(chart, on_select="rerun", selection_mode="single-object")

    st.write("Please click the node to see the available fire flow")
    if(len(event.selection.objects)>0):
        st.write("Elevation (ft): ", event.selection.objects.fireflow[0].get("ELEVATION"))
        st.write("Available Fire Flow (gpm)", event.selection.objects.fireflow[0].get("FFW"))
if selected == "Quality":
    st.markdown(f"#### Water Age")
    chart = pydeck.Deck(
    [pipe_layer, tank_layer, tanktext_layer, pump_layer, pumptext_layer, waterage_layer],
    initial_view_state=INITIAL_VIEW_STATE,
    map_style="mapbox://styles/hazensawyer/clnlt5te9003l01p5fta3hjc8", 
    api_keys={"mapbox": "pk.eyJ1IjoiaGF6ZW5zYXd5ZXIiLCJhIjoiY2xmNGQ3MDgyMTE3YjQzcnE1djRpOGVtNiJ9.U06GItbSVWFTsvfg9WwQWQ"},
    tooltip={"text": "Diameter: {Diameter}\nMaterial: {Material}\nAge: {Age}\n Installation Year: {InstallDat}"},
)

    event = st.pydeck_chart(chart, on_select="rerun", selection_mode="single-object")

    st.write("Please click the node to see the water age")
    if(len(event.selection.objects)>0):
        st.write("Elevation (ft): ", event.selection.objects.waterage[0].get("ELEVATION"))
        st.write("Water Age (hr)", event.selection.objects.waterage[0].get("TRAVEL"))
if selected == "I-Hydrant":
    st.markdown(f"#### I-Hydrants")
    chart = pydeck.Deck(
    [pipe_layer, tank_layer,  pump_layer,  ihydrant_layer],
    initial_view_state=INITIAL_VIEW_STATE,
    map_style="mapbox://styles/hazensawyer/clnlt5te9003l01p5fta3hjc8", 
    api_keys={"mapbox": "pk.eyJ1IjoiaGF6ZW5zYXd5ZXIiLCJhIjoiY2xmNGQ3MDgyMTE3YjQzcnE1djRpOGVtNiJ9.U06GItbSVWFTsvfg9WwQWQ"},
    tooltip={"text": "Diameter: {Diameter}\nMaterial: {Material}\nAge: {Age}\n Installation Year: {InstallDat}"},
)

    event = st.pydeck_chart(chart, on_select="rerun", selection_mode="single-object")



