
import streamlit as st
import gspread
from datetime import datetime

# Función para conectar con Google Sheets
def conectar_bd():
    try:
        # Lee el archivo que acabas de subir
        gc = gspread.service_account(filename='credenciales.json')
        # Abre tu hoja exacta
        sh = gc.open('Base_Datos_Blindaje')
        worksheet = sh.worksheet('Usuarios')
        return worksheet
    except Exception as e:
        st.error(f"Error de conexión. Asegúrate de que el archivo se llame 'credenciales.json' y la hoja 'Base_Datos_Blindaje'. Detalle: {e}")
        return None

def app_blindaje():
    st.title("🛡️ Sistema Blindaje")
    st.info("Tu armadura contra la pérdida muscular y el envejecimiento.")

    st.subheader("1. Captura de Perfil Biológico")

    col_edad, col_peso = st.columns(2)
    with col_edad:
        edad = st.number_input("Edad:", min_value=15, max_value=100, value=45)
    with col_peso:
        peso = st.number_input("Peso actual (kg):", min_value=40.0, max_value=150.0, value=78.0)

    objetivo = st.selectbox("Meta principal:", ["Aumentar / Volumen", "Perder Grasa / Marcar", "Mantener / Tonificar"])

    # ¡LA CLAVE DEL EMBUDO! Capturar el email
    email = st.text_input("Tu Correo Electrónico (Aquí enviaremos tu acceso):", placeholder="ejemplo@correo.com")

    # Botón de acción que detona el guardado
    if st.button("Analizar mi Perfil y Ver Planes", type="primary"):
        if email == "":
            st.warning("⚠️ Por favor ingresa tu correo para continuar.")
        else:
            # 1. Analizar Sarcopenia
            alerta_sarcopenia = "SÍ" if edad >= 45 else "NO"
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 2. Guardar en Base de Datos
            worksheet = conectar_bd()
            if worksheet:
                # El orden debe coincidir con tus columnas en Google Sheets
                fila_datos = [fecha_actual, email, edad, peso, objetivo, alerta_sarcopenia, "Pendiente de Elegir", "Pendiente de Pago"]
                worksheet.append_row(fila_datos)
                st.success("✅ Perfil analizado y guardado exitosamente.")

                # 3. Mostrar Diagnóstico
                st.write("---")
                st.subheader("2. Diagnóstico de la IA")
                if alerta_sarcopenia == "SÍ":
                    st.warning("🔒 **Alerta de Prevención (+45 años):** Riesgo natural de sarcopenia detectado. Requiere plan de alta densidad proteica y fuerza.")
                else:
                    st.success("✅ **Fase Anabólica Óptima.**")

                # 4. Mostrar Muro de Pago
                st.write("---")
                st.subheader("3. Desbloquea tu Plan Personalizado")
                col1, col2 = st.columns(2)

                with col1:
                    st.container(border=True)
                    st.write("### Plan Mensual")
                    st.metric(label="Inversión", value="$180 MXN / mes")
                    st.link_button("💳 Suscribirse Mensual", "https://mpago.la/1fBb4uk", use_container_width=True)

                with col2:
                    st.container(border=True)
                    st.write("### ⭐ Plan Anual (Fundadores)")
                    st.metric(label="Inversión Única", value="$1,080 MXN / año", delta="-50% OFF")
                    st.link_button("🔥 Quiero el Descuento (Aplica MSI)", "https://mpago.la/2NNimKG", type="primary", use_container_width=True)

if __name__ == "__main__":
    app_blindaje()
