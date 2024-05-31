import streamlit as st
import tensorflow as tf
import numpy as np
import pickle as pk
import warnings
import plotly.express as px

# Desactivar advertencias
warnings.filterwarnings("ignore")
# Definir usuario y contraseña
USERNAME = 'admin'
PASSWORD = 'password'

# Definir el nombre de la aplicación
st.set_page_config(page_title="CiphraGuard 🤖")

# Cargar el modelo
cnn_model_1d = tf.keras.models.load_model('model\cnn_model_1d.h5')
# Lista de variables con su tipo de dato correspondiente
variables = {
    'pslist.nproc': int,
    'pslist.nppid': int,
    'pslist.avg_threads': float,
    'pslist.avg_handlers': float,
    'dlllist.ndlls': int,
    'dlllist.avg_dlls_per_proc': float,
    'handles.nhandles': int,
    'handles.avg_handles_per_proc': float,
    'handles.nfile': int,
    'handles.nevent': int,
    'handles.ndesktop': int,
    'handles.nkey': int,
    'handles.nthread': int,
    'handles.ndirectory': int,
    'handles.nsemaphore': int,
    'handles.ntimer': int,
    'handles.nsection': int,
    'handles.nmutant': int,
    'ldrmodules.not_in_load': int,
    'ldrmodules.not_in_init': int,
    'ldrmodules.not_in_mem': int,
    'ldrmodules.not_in_load_avg': float,
    'ldrmodules.not_in_init_avg': float,
    'ldrmodules.not_in_mem_avg': float,
    'malfind.ninjections': int,
    'malfind.commitCharge': int,
    'malfind.protection': int,
    'malfind.uniqueInjections': float,
    'psxview.not_in_pslist': int,
    'psxview.not_in_eprocess_pool': int,
    'psxview.not_in_ethread_pool': int,
    'psxview.not_in_pspcid_list': int,
    'psxview.not_in_csrss_handles': int,
    'psxview.not_in_session': int,
    'psxview.not_in_deskthrd': int,
    'psxview.not_in_pslist_false_avg': float,
    'psxview.not_in_eprocess_pool_false_avg': float,
    'psxview.not_in_ethread_pool_false_avg': float,
    'psxview.not_in_pspcid_list_false_avg': float,
    'psxview.not_in_csrss_handles_false_avg': float,
    'psxview.not_in_session_false_avg': float,
    'psxview.not_in_deskthrd_false_avg': float,
    'modules.nmodules': int,
    'svcscan.nservices': int,
    'svcscan.kernel_drivers': int,
    'svcscan.fs_drivers': int,
    'svcscan.process_services': int,
    'svcscan.shared_process_services': int,
    'svcscan.nactive': int,
    'callbacks.ncallbacks': int,
    'callbacks.nanonymous': int,
    'callbacks.ngeneric': int
}
# Función de autenticación
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

# Inicializar st.session_state['logged_in']
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False


# Página de login
def login_page():
    st.title("Ingreso de usuario")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar", type = 'primary'):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# Página principal
def main_page():
    st.title("Predicción de Clase")
    st.write("Ingrese los datos para la predicción:")

    # Entradas del usuario para cada característica
    # Recopilación de las características ingresadas por el usuario
    # Recopilación de las características ingresadas por el usuario
    user_input = {variable: 0 for variable in variables.keys()}  # Inicializar con valores predeterminados de 0
    for variable, dtype in variables.items():
        if dtype == int:
            value = st.number_input(f"{variable} ({dtype.__name__})", step=1)
        else:
            value = st.number_input(f"{variable} ({dtype.__name__})", step=0.01)
        if value is not None:
            user_input[variable] = value

    # Convertir las características ingresadas a una matriz
    features_matrix = np.array(list(user_input.values())).reshape(1, -1)
    
    # Aplicar PCA
    pca = pk.load(open("model\pca_data.pkl",'rb'))
    features_pca = pca.transform(features_matrix)
    # Estandarizar las características
    scaler = pk.load(open("model\scaler.pkl",'rb'))
    features_scaled = scaler.transform(features_pca)
    features_scaled_reshaped = features_scaled.reshape(-1, 2, 1)

    if st.button("Predecir"):
        # Hacer la predicción
        predictions = cnn_model_1d.predict(features_scaled_reshaped)
        predicted_class = np.argmax(predictions)
        class_probabilities = predictions[0]
        class_labels = ["Petición no maliciosa", "Ransomware", "Spyware", "Trojan"]

        # Mostrar los resultados
        st.write(f"La petición es {class_labels[predicted_class]}")        
        if predicted_class == 0:
            st.info('La petición está limpia')
        else:
            st.warning('La petición es malisiosa, por favor revise los datos', icon = "🚨")
                
        # Mostrar un desplegable con la gráfica de las probabilidades de cada clase
        with st.expander("Ver Probabilidades de Clase"):
            # Definir las etiquetas de las clases
            

            # Verificar si class_probabilities es None antes de usarlo
            if class_probabilities is not None:
                # Crear el gráfico con Plotly Express
                fig = px.bar(x=class_labels, y=[i*100 for i in class_probabilities], 
                            labels={'y': 'Probabilidad (%)'}, 
                            title='Probabilidades de Clase', 
                            height=400, 
                            width=600)
                st.plotly_chart(fig)
            else:
                st.write("Presiona el botón 'Predecir' para calcular las probabilidades primero.")
        
        
# Control de la interfaz
if st.session_state['logged_in']:
    main_page()
else:
    login_page()
