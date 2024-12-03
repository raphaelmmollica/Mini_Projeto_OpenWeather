from pprint import pprint
import streamlit as st
import requests

from PIL import Image
from io import BytesIO

def fazer_request(url,params=None,tipo='json'):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        if tipo=='json':
            resultado = resposta.json()
        else:
            resultado = resposta.content()
    return resultado


def pegar_tempo_para_local(local):
    token = '2a91b249d4a339c025cf977866b885a6'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid': token,
        'q' : local,
        'units': 'metric',
        'lang': 'pt_br',
    }
    dados_tempo = fazer_request(url=url,params=params)
    return dados_tempo

def main():
    st.title('Web App Tempo')
    st.write('Dados do OpenWeather ()')
    local = st.text_input('Busque uma cidade:')
    if not local:
        st.stop()
    
    dados_tempo = pegar_tempo_para_local(local=local)
    if not dados_tempo:
        st.warning(f'Dados não encontrados para a cidade {local}')
        st.stop

    clima_atual = dados_tempo['weather'][0]['description']
    clima_icone = dados_tempo['weather'][0]['icon']

    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    cobertura_nuvens = dados_tempo['clouds']['all']

    coldest1, coldest2 = st.columns(2)
    with coldest1:
        st.metric(label='Tempo atual',value=clima_atual)
    with coldest2:
        st.image(f'http://openweathermap.org/img/w/{clima_icone}.png')

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Temperatura',value=f'{temperatura} ° C' )
        st.metric(label='Sensação Térmica',value=f'{sensacao_termica} ° C' )

    with col2:
        st.metric(label='Umidade',value=f'{umidade} %' )
        st.metric(label='Cobertura de Nuvens',value=f'{cobertura_nuvens} %' )


if __name__ == '__main__':
    main() 
